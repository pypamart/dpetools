"""
Container class for configuration settings.
"""


class Container:
    """
    A class to represent a container for configuration settings and dependencies injection.
    """

    API_DATA_URL: str = "https://data.ademe.fr/data-fair/api/v1/datasets/dpe03existant/lines"
    API_SCHEMA_URL: str = "https://data.ademe.fr/data-fair/api/v1/datasets/dpe03existant/schema"

    REQUESTS_TIMEOUT: int = 10
