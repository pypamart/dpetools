"""
Module for interacting with the DPE API.
"""

from typing import Any

import pandas as pd
import requests

from dpetools.exceptions import DPEApiClientException, InvalidDPERecordsLimitError

SUCCESS_STATUS_CODE = 200
NB_RECORDS_DEFAULT = 50


class DPEApiClient:
    """
    Client for fetching DPE records from the ADEME API.
    """

    def __init__(self, api_data_url: str, timeout: int = 10):
        self.__api_endpoint = api_data_url
        self.__timeout = timeout

    def fetch_dpe_records(self, nbrecords: int | None = None, **kwargs):
        """
        Fetch DPE records from the API endpoint.

        Args:
            nbrecords (int | None): The number of records to fetch. If None, fetches all available records.

        Returns:
            pd.DataFrame: A DataFrame containing the DPE records.
            If nbrecords is specified, it limits the number of records returned.

        Raises:
            DPEApiClientException: If the API request fails or returns an error.
            InvalidDPERecordsLimitError: If nbrecords is not a strict positive integer.
        """
        if nbrecords is not None and nbrecords <= 0:
            raise InvalidDPERecordsLimitError(nbrecords)

        params: dict[str, Any] = {"size": nbrecords if nbrecords is not None else NB_RECORDS_DEFAULT}

        try:
            response = requests.get(self.__api_endpoint, timeout=self.__timeout, params=params)

            if response.status_code == SUCCESS_STATUS_CODE:
                data = response.json()
                dpe_records_dataframe = pd.DataFrame(data["results"])
                return dpe_records_dataframe
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
