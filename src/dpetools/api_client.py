"""
Module for interacting with the DPE API.
"""

from typing import Any

import pandas as pd
import requests

from dpetools.exceptions import DPEApiClientException, InvalidDPERecordsLimitError, NonExistingColumnError

SUCCESS_STATUS_CODE = 200
BAD_REQUEST_STATUS_CODE = 400
NB_RECORDS_DEFAULT = 50
SORT_BY_DEFAULT = "date_etablissement_dpe"
ORDER_DEFAULT = "desc"


class DPEApiClient:
    """
    Client for fetching DPE records from the ADEME API.
    """

    def __init__(self, api_data_url: str, api_schema_url: str, timeout: int = 10):
        """
        Initialize the DPEApiClient with the API endpoint and timeout.

        Args:
            api_data_url (str): The URL of the API endpoint to fetch DPE records.
            api_schema_url (str): The URL of the API schema endpoint.
            timeout (int): The timeout for API requests in seconds. Defaults to 10 seconds.
        """
        self.__api_endpoint = api_data_url
        self.__api_schema_endpoint = api_schema_url
        self.__timeout = timeout
        self.__available_columns: list[str] | None = None

    def fetch_dpe_records(
        self,
        select_columns: list[str] | None = None,
        sort_by: str = SORT_BY_DEFAULT,
        nbrecords: int = NB_RECORDS_DEFAULT,
        order: str = "asc",
    ) -> pd.DataFrame:
        """
        Fetch DPE records from the API endpoint.

        Args:
            select_columns (list[str] | None): List of columns to select from the DataFrame. If None, all columns are returned.
            sort_by (str): The field by which to sort the records. Defaults to SORT_BY_DEFAULT.
            nbrecords (int): The maximum number of records to fetch. Defaults to NB_RECORDS_DEFAULT.
            order (str): The order of sorting, either "asc" or "desc", for "ascending" and "descending". Defaults to "asc". If not "asc" or "desc", it will be ignored and set to "asc".

        Returns:
            pd.DataFrame: A DataFrame containing the DPE records.
            If select_columns is specified, it filters the DataFrame to include only those columns. Else, all columns are included.
            If nbrecords is specified, it limits the number of records returned.


        Raises:
            DPEApiClientException: If the API request fails or returns an error.
        """
        params = self.__prepare_params(select_columns, sort_by, nbrecords, order)

        try:
            response = requests.get(self.__api_endpoint, timeout=self.__timeout, params=params)

            if response.status_code == SUCCESS_STATUS_CODE:
                data = response.json()
                dpe_records_dataframe = pd.DataFrame(data["results"])
                return dpe_records_dataframe
            elif response.status_code == BAD_REQUEST_STATUS_CODE:
                raise DPEApiClientException(f"Bad request: {response.status_code} - {response.text}")
            else:
                raise DPEApiClientException(f"Failed to fetch data: {response.status_code} - {response.text}")
        except requests.RequestException as e:
            raise DPEApiClientException(f"An error occurred while fetching data: {str(e)}") from e

    def __prepare_params(
        self,
        select_columns: list[str] | None,
        sort_by: str,
        nbrecords: int,
        order: str,
    ) -> dict[str, Any]:
        """
        Prepare the parameters for the API request.
        Args:
            select_columns (list[str] | None): List of columns to select from the DataFrame. If None, all columns are returned.
            sort_by (str): The field by which to sort the records. Defaults to SORT_BY_DEFAULT.
            nbrecords (int): The maximum number of records to fetch. Defaults to NB_RECORDS_DEFAULT.
            order (str): The order of sorting, either "asc" or "desc". Defaults to "asc".
        Returns:
            dict[str, Any]: A dictionary of parameters to be used in the API request.
        Raises:
            InvalidDPERecordsLimitError: If nbrecords is not a strict positive integer.
            NonExistingColumnError: If select_columns contains columns that do not exist in the available columns.
        """
        if nbrecords is not None and nbrecords <= 0 or not isinstance(nbrecords, int):
            raise InvalidDPERecordsLimitError(nbrecords)

        params: dict[str, Any] = {"sort": f"{'-' if order == 'desc' else ''}{sort_by}", "size": nbrecords}

        if select_columns is None and sort_by == SORT_BY_DEFAULT:
            return params

        available_columns = self.available_columns()

        if select_columns:
            if set(select_columns).issubset(available_columns):
                params["select"] = ",".join(map(str, set(select_columns)))
            else:
                raise NonExistingColumnError(select_columns, available_columns)

        if sort_by != SORT_BY_DEFAULT:
            if sort_by in available_columns:
                params["sort"] = f"{'-' if order == 'desc' else ''}{sort_by}"
            else:
                raise NonExistingColumnError([sort_by], available_columns)

        return params

    def is_api_reachable(self) -> bool:
        """
        Check if the API endpoint is reachable.

        Returns:
            bool: True if the API is reachable, False otherwise.
        """
        params = {"size": 0}

        try:
            response = requests.get(self.__api_endpoint, timeout=self.__timeout, params=params)
            return response.status_code == SUCCESS_STATUS_CODE
        except requests.RequestException:
            return False

    def available_columns(self) -> list[str]:
        """
        Get the list of available columns in the DPE records.

        Returns:
            list[str]: A list of available columns.
        """
        if self.__available_columns is None:
            schema = requests.get(self.__api_schema_endpoint, timeout=self.__timeout)

            if schema.status_code == SUCCESS_STATUS_CODE:
                schema_data = schema.json()
                self.__available_columns = [column["key"] for column in schema_data]
            else:
                raise DPEApiClientException(f"Failed to fetch schema: {schema.status_code} - {schema.text}")

        return self.__available_columns
