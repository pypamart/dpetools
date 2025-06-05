class DPEApiClientException(Exception):
    """Custom exception for errors in the DPE API client."""


class InvalidDPERecordsLimitError(ValueError):
    """
    Exception raised when the limit for fetching records is not a strict positive integer.
    """

    def __init__(self, limit: int):
        super().__init__(f"The limit must be a positive integer >= 1, got {limit}.")
