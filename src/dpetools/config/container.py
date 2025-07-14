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

    SUCCESS_STATUS_CODE = 200
    BAD_REQUEST_STATUS_CODE = 400
    INTERNAL_SERVER_ERROR_STATUS_CODE = 500

    NB_RECORDS_DEFAULT = 50
    SORT_BY_DEFAULT = "date_etablissement_dpe"
    ORDER_DEFAULT = "asc"
