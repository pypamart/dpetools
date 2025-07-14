from unittest.mock import MagicMock, patch

import pandas as pd
import pytest
import requests

from dpetools.api_client import DPEApiClient
from dpetools.config.container import Container
from dpetools.exceptions import DPEApiClientException, InvalidDPERecordsLimitError, NonExistingColumnError


class MockServerErrorResponse:
    """
    Mock response class to simulate a server error (500 Internal Server Error).
    This is used to test the behavior of the DPEApiClient when the API returns an error.
    """

    def __init__(self):
        self.status_code = 500
        self.text = "Internal Server Error"

    def json(self): ...


@pytest.fixture
def dpe_api_client():
    """
    Fixture to create a DPEAPIClient instance for testing.
    """
    return DPEApiClient()


@pytest.mark.happy
def test_should_retun_true_when_api_is_reachable(dpe_api_client: DPEApiClient):
    # Act
    is_reachable = dpe_api_client.is_api_reachable()

    # Assert
    assert is_reachable is True


@pytest.mark.sad
def test_should_return_false_when_api_is_not_reachable(dpe_api_client: DPEApiClient, monkeypatch):
    # Arrange
    # Mock the requests.get method to raise a RequestException
    monkeypatch.setattr(
        "requests.get",
        lambda *args, **kwargs: (_ for _ in ()).throw(requests.RequestException),
    )

    # Act
    is_reachable = dpe_api_client.is_api_reachable()

    # Assert
    assert is_reachable is False


@pytest.mark.happy
def test_should_return_dataframe_when_fetching_dpe_records(
    dpe_api_client: DPEApiClient,
):
    # Act
    dpe_records_dataframe = dpe_api_client.fetch_dpe_records()

    # Assert
    assert isinstance(dpe_records_dataframe, pd.DataFrame)
    assert not dpe_records_dataframe.empty
    assert "numero_dpe" in dpe_records_dataframe.columns


@pytest.mark.sad
def test_should_raise_error_when_fetching_dpe_records_fails(dpe_api_client: DPEApiClient, monkeypatch):
    # Arrange
    # Mock the requests.get method to return a response with a non-200 status code
    monkeypatch.setattr(
        "requests.get",
        lambda *args, **kwargs: MockServerErrorResponse(),
    )

    # Act & Assert
    with pytest.raises(DPEApiClientException) as exc_info:
        dpe_api_client.fetch_dpe_records()

    assert "Failed to fetch data" in str(exc_info.value)


@pytest.mark.sad
def test_should_raise_timeout_error_when_api_request_times_out(dpe_api_client: DPEApiClient, monkeypatch):
    # Arrange
    # Mock the requests.get method to raise a Timeout exception
    monkeypatch.setattr(
        "requests.get",
        lambda *args, **kwargs: (_ for _ in ()).throw(requests.Timeout),
    )
    # Act & Assert
    with pytest.raises(DPEApiClientException) as exc_info:
        dpe_api_client.fetch_dpe_records()

    assert "An error occurred while fetching data" in str(exc_info.value)


@pytest.mark.happy
@pytest.mark.parametrize(
    "nbrecords, expected_count",
    [
        (None, Container.NB_RECORDS_DEFAULT),  # Default limit
        (1, 1),
        (10, 10),
        (100, 100),
        (1000, 1000),
    ],
)
def test_should_return_dataframe_with_good_number_of_records(
    dpe_api_client: DPEApiClient, nbrecords: int, expected_count: int
):
    # Act
    if nbrecords is None:
        dpe_records_dataframe = dpe_api_client.fetch_dpe_records()
    else:
        dpe_records_dataframe = dpe_api_client.fetch_dpe_records(nbrecords=nbrecords)

    # Assert
    assert len(dpe_records_dataframe) == expected_count, (
        f"Expected {expected_count} records, but got {len(dpe_records_dataframe)}"
    )
    assert "numero_dpe" in dpe_records_dataframe.columns


@pytest.mark.sad
@pytest.mark.edge
@pytest.mark.parametrize("nbrecords", [0, -1, -10])
def test_should_raise_error_when_fetching_dpe_records_with_invalid_limit(dpe_api_client: DPEApiClient, nbrecords: int):
    # Act & Assert
    with pytest.raises(InvalidDPERecordsLimitError) as exc_info:
        dpe_api_client.fetch_dpe_records(nbrecords=nbrecords)

    assert str(exc_info.value) == f"The limit must be a positive integer >= 1, got {nbrecords}."


@pytest.mark.happy
@pytest.mark.parametrize(
    "sort_by, order",
    [
        (None, None),  # Default sorting (no specific field)
        (None, "asc"),  # Default sorting order
        (None, "desc"),  # Default sorting order
        (None, "dummy_order"),  # Invalid order, should default to "asc"
        ("date_etablissement_dpe", None),  # Default sorting order
        ("date_etablissement_dpe", "asc"),  # Ascending order by establishment date
        ("date_etablissement_dpe", "desc"),  # Descending order by establishment date
        ("numero_dpe", "asc"),  # Ascending order by DPE number
        ("numero_dpe", "desc"),  # Descending order by DPE number
    ],
)
def test_should_return_sorted_dataframe_when_fetching_dpe_records(
    dpe_api_client: DPEApiClient, sort_by: str, order: str
):
    """
    Test that the DPE records are returned sorted by the specified field and order.

    Args:
        dpe_api_client (DPEApiClient): The API client to fetch records.
        sort_by (str): The field by which to sort the records.
        order (str): The order of sorting, either "asc" or "desc".
    """
    # Act
    if order is None and sort_by is None:
        dpe_records_dataframe = dpe_api_client.fetch_dpe_records(nbrecords=10)
    elif order is None:
        dpe_records_dataframe = dpe_api_client.fetch_dpe_records(sort_by=sort_by, nbrecords=10)
    elif sort_by is None:
        dpe_records_dataframe = dpe_api_client.fetch_dpe_records(order=order, nbrecords=10)
    else:
        dpe_records_dataframe = dpe_api_client.fetch_dpe_records(sort_by=sort_by, order=order, nbrecords=10)

    # Assert
    assert isinstance(dpe_records_dataframe, pd.DataFrame)
    assert not dpe_records_dataframe.empty

    # Check if the records are sorted by the specified field
    if sort_by is None:
        sort_by = "date_etablissement_dpe"

    assert sort_by in dpe_records_dataframe.columns

    if order == "desc":
        assert dpe_records_dataframe[sort_by].is_monotonic_decreasing, (
            f"The records are not ordered by '{sort_by}' in descending order."
        )
    else:
        assert dpe_records_dataframe[sort_by].is_monotonic_increasing, (
            f"The records are not ordered by '{sort_by}' in ascending order."
        )


@pytest.mark.happy
@patch("dpetools.api_client.requests.get")
def test_should_return_available_columns(mock_get: MagicMock, dpe_api_client: DPEApiClient):
    """
    Test that the available columns are returned correctly from the API.

    Args:
        dpe_api_client (DPEApiClient): The API client to fetch available columns.
    """
    # Arrange
    mock_response = MagicMock()
    mock_response.status_code = Container.SUCCESS_STATUS_CODE
    mock_response.json.return_value = [{"key": "col1", "type": "string"}, {"key": "col2", "type": "int"}]
    mock_get.return_value = mock_response

    # Act
    available_columns = dpe_api_client.available_columns()

    # Assert
    assert "col1" in available_columns
    assert "col2" in available_columns
    assert isinstance(available_columns, list)


@pytest.mark.happy
@patch("dpetools.api_client.requests.get")
def test_should_cache_available_columns_result(mock_get: MagicMock, dpe_api_client: DPEApiClient):
    """
    Test that the available columns are cached after the first call.

    Args:
        mock_get (MagicMock): Mock for the requests.get method.
        dpe_api_client (DPEApiClient): The API client to fetch available columns.
    """
    # Arrange
    mock_response = MagicMock()
    mock_response.status_code = Container.SUCCESS_STATUS_CODE
    mock_response.json.return_value = [{"key": "col1", "type": "string"}]
    mock_get.return_value = mock_response

    # Act
    dpe_api_client.available_columns()
    available_columns = dpe_api_client.available_columns()

    # Assert
    assert "col1" in available_columns
    mock_get.assert_called_once()


@pytest.mark.sad
@patch("dpetools.api_client.requests.get")
def test_available_columns_api_error_raises(mock_get: MagicMock, dpe_api_client: DPEApiClient):
    """
    Test that an error is raised when the API call for available columns fails.

    Args:
        mock_get (MagicMock): Mock for the requests.get method.
        dpe_api_client (DPEApiClient): The API client to fetch available columns.
    """
    # Arrange
    mock_response = MagicMock()
    mock_response.status_code = Container.INTERNAL_SERVER_ERROR_STATUS_CODE
    mock_response.text = "Internal Server Error"
    mock_get.return_value = mock_response

    # Act
    with pytest.raises(DPEApiClientException) as exc_info:
        dpe_api_client.available_columns()

    # Assert
    assert "Failed to fetch schema" in str(exc_info.value)


@pytest.mark.happy
@patch("dpetools.api_client.requests.get")
def test_should_return_dataframe_with_selected_columns(mock_get: MagicMock, dpe_api_client: DPEApiClient):
    """
    Test that fetch_dpe_records returns a DataFrame with only the selected columns.

    Args:
        mock_get (MagicMock): Mock for the requests.get method.
        dpe_api_client (DPEApiClient): The API client to fetch records.
    """
    # Arrange
    # First call: schema endpoint
    mock_schema_response = MagicMock()
    mock_schema_response.status_code = Container.SUCCESS_STATUS_CODE
    mock_schema_response.json.return_value = [
        {"key": "col1", "type": "string"},
        {"key": "col2", "type": "int"},
        {"key": "col3", "type": "string"},
    ]
    # Second call: data endpoint
    mock_data_response = MagicMock()
    mock_data_response.status_code = Container.SUCCESS_STATUS_CODE
    mock_data_response.json.return_value = {"results": [{"col1": "a", "col2": 1}, {"col1": "b", "col2": 2}]}
    mock_get.side_effect = [mock_schema_response, mock_data_response]

    # Act
    dpe_records_dataframe = dpe_api_client.fetch_dpe_records(select_columns=["col1", "col2"], nbrecords=2)

    # Assert
    assert isinstance(dpe_records_dataframe, pd.DataFrame)
    assert set(dpe_records_dataframe.columns) == {"col1", "col2"}


@pytest.mark.sad
@patch("dpetools.api_client.requests.get")
def test_should_raise_error_when_selecting_nonexistent_column(mock_get: MagicMock, dpe_api_client: DPEApiClient):
    """
    Test that fetch_dpe_records raises an error if a non-existent column is requested.

    Args:
        mock_get (MagicMock): Mock for the requests.get method.
        dpe_api_client (DPEApiClient): The API client to fetch records.
    """
    # Arrange
    mock_response = MagicMock()
    mock_response.status_code = Container.SUCCESS_STATUS_CODE
    mock_response.json.return_value = [
        {"key": "col1", "type": "string"},
        {"key": "col2", "type": "int"},
    ]
    mock_get.return_value = mock_response

    # Act
    with pytest.raises(NonExistingColumnError) as exc_info:
        dpe_api_client.fetch_dpe_records(select_columns=["col1", "unexisting_column"], nbrecords=1)

    assert (
        str(exc_info.value)
        == "The requested column(s) ['unexisting_column'] do not exist in the available columns: ['col1', 'col2']."
    ), f"Expected error message to indicate non-existing columns, but got: {exc_info.value}"


@pytest.mark.happy
@patch("dpetools.api_client.requests.get")
def test_should_return_all_columns_when_select_columns_is_none(mock_get: MagicMock, dpe_api_client: DPEApiClient):
    """
    Test that fetch_dpe_records returns all columns when select_columns is None.

    Args:
        mock_get (MagicMock): Mock for the requests.get method.
        dpe_api_client (DPEApiClient): The API client to fetch records.
    """
    # Arrange
    mock_response = MagicMock()
    mock_response.status_code = Container.SUCCESS_STATUS_CODE
    mock_response.json.return_value = {
        "schema": [
            {"key": "col1", "type": "string"},
            {"key": "col2", "type": "int"},
            {"key": "col3", "type": "string"},
        ],
        "results": [{"col1": "a", "col2": 1, "col3": "x"}, {"col1": "b", "col2": 2, "col3": "y"}],
    }
    mock_get.return_value = mock_response

    # Act
    df = dpe_api_client.fetch_dpe_records(select_columns=None, nbrecords=2)

    # Assert
    assert set(df.columns) == {"col1", "col2", "col3"}


@pytest.mark.sad
@patch("dpetools.api_client.requests.get")
def test_should_raise_error_when_sort_by_nonexistent_field(mock_get: MagicMock, dpe_api_client: DPEApiClient):
    """
    Test that fetch_dpe_records raises an error if a non-existent column is used for sorting.

    Args:
        mock_get (MagicMock): Mock for the requests.get method.
        dpe_api_client (DPEApiClient): The API client to fetch records.
    """
    # Arrange
    mock_response = MagicMock()
    mock_response.status_code = Container.SUCCESS_STATUS_CODE
    mock_response.json.return_value = [
        {"key": "col1", "type": "string"},
        {"key": "col2", "type": "int"},
    ]
    mock_get.return_value = mock_response

    # Act
    with pytest.raises(NonExistingColumnError) as exc_info:
        dpe_api_client.fetch_dpe_records(sort_by="unexisting_column", nbrecords=1)

    assert (
        str(exc_info.value)
        == "The requested column(s) ['unexisting_column'] do not exist in the available columns: ['col1', 'col2']."
    ), f"Expected error message to indicate non-existing columns, but got: {exc_info.value}"
