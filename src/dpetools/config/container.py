"""
Container class for configuration settings.
"""


class Container:
    """
    A class to represent a container for configuration settings and dependencies injection.
    """

    api_data_url: str = "https://data.ademe.fr/data-fair/api/v1/datasets/dpe03existant/lines"

    requests_timeout: int = 10
