"""
Module for interacting with the DPE API.
"""

from typing import Any

import pandas as pd
import requests

from dpetools.exceptions import DPEApiClientException, InvalidDPERecordsLimitError

SUCCESS_STATUS_CODE = 200
BAD_REQUEST_STATUS_CODE = 400
NB_RECORDS_DEFAULT = 50
SORT_BY_DEFAULT = "date_etablissement_dpe"
ORDER_DEFAULT = "desc"


class DPEApiClient:
    """
    Client for fetching DPE records from the ADEME API.
    """

    def __init__(self, api_data_url: str, timeout: int = 10):
        self.__api_endpoint = api_data_url
        self.__timeout = timeout

    def fetch_dpe_records(
        self, sort_by: str = SORT_BY_DEFAULT, nbrecords: int = NB_RECORDS_DEFAULT, order: str = "asc"
    ) -> pd.DataFrame:
        """
        Fetch DPE records from the API endpoint.

        Args:
            sort_by (str): The field by which to sort the records. Defaults to SORT_BY_DEFAULT.
            nbrecords (int): The maximum number of records to fetch. Defaults to NB_RECORDS_DEFAULT.
            order (str): The order of sorting, either "asc" or "desc", for "ascending" and "descending". Defaults to "asc". If not "asc" or "desc", it will be ignored and set to "asc".

        Returns:
            pd.DataFrame: A DataFrame containing the DPE records.
            If nbrecords is specified, it limits the number of records returned.

        Raises:
            DPEApiClientException: If the API request fails or returns an error.
            InvalidDPERecordsLimitError: If nbrecords is not a strict positive integer.
        """
        if nbrecords is not None and nbrecords <= 0 or not isinstance(nbrecords, int):
            raise InvalidDPERecordsLimitError(nbrecords)

        params: dict[str, Any] = {
            "sort": f"{'-' if order == 'desc' else ''}{sort_by}", 
            "size": nbrecords
            }

        try:
            response = requests.get(self.__api_endpoint, timeout=self.__timeout, params=params)

            if response.status_code == SUCCESS_STATUS_CODE:
                data = response.json()
                dpe_records_dataframe = pd.DataFrame(data["results"])
                return dpe_records_dataframe
            elif response.status_code == BAD_REQUEST_STATUS_CODE:
                raise InvalidDPERecordsLimitError(f"Bad request: {response.status_code} - {response.text}")
            else:
                raise DPEApiClientException(f"Failed to fetch data: {response.status_code} - {response.text}")
        except requests.RequestException as e:
            raise DPEApiClientException(f"An error occurred while fetching data: {str(e)}") from e

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
