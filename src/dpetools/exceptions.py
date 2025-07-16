class DPEApiClientException(Exception):
    """Custom exception for errors in the DPE API client."""


class InvalidDPERecordsLimitError(ValueError):
    """
    Exception raised when the limit for fetching records is not a strict positive integer.
    """

    def __init__(self, limit: int):
        super().__init__(f"The limit must be a positive integer >= 1, got {limit}.")


class NonExistingColumnError(Exception):
    """
    Exception raised when a specified column does not exist in the DataFrame.
    """

    def __init__(self, requested_columns: list[str], available_columns: list[str]):
        non_existing_columns = set(requested_columns) - set(available_columns)
        super().__init__(
            f"The requested column(s) {list(non_existing_columns)} do not exist in the available columns: {available_columns}."
        )

class InvalidParameterError(Exception):
    """
    Exception raised for invalid parameters in the DPE API client.
    """

    def __init__(self, message: str):
        super().__init__(message)