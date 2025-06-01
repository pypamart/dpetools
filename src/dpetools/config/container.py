from typing import Callable

from dpetools.api_client import DPEApiClient

class Container:
    """
    A class to represent a container for configuration settings.
    """
    api_data_url: str = "https://data.ademe.fr/data-fair/api/v1/datasets/dpe03existant/lines"
    
    @staticmethod
    def dpe_client_factory() -> DPEApiClient:
        """Factory method to create a DPEAPIClient instance."""
        return DPEApiClient(Container.api_data_url)