import requests

import pandas as pd

from dpetools.exceptions import DPEApiClientException


class DPEApiClient:
    def __init__(self, api_data_url: str):
        self.__api_endpoint = api_data_url

    def fetch_dpe_records(self) -> pd.DataFrame:
        """
        Fetch DPE records from the API endpoint.
        
        Returns:
            pd.DataFrame: A DataFrame containing the DPE records.
        """
        params = {}
        response = requests.get(self.__api_endpoint, params=params)
    
        if response.status_code == 200:
            data = response.json()
            dpe_records_dataframe = pd.DataFrame(data['results'])
            return dpe_records_dataframe
        else:
            raise DPEApiClientException(f"Failed to fetch data: {response.status_code} - {response.text}")
       

    def is_api_reachable(self) -> bool:
        """
        Check if the API endpoint is reachable.
        
        Returns:
            bool: True if the API is reachable, False otherwise.
        """
        try:
            response = requests.get(self.__api_endpoint)
            return response.status_code == 200
        except requests.RequestException:
            return False