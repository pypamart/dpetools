import pandas as pd
import pytest
import requests

from dpetools.api_client import NB_RECORDS_DEFAULT, DPEApiClient
from dpetools.config.container import Container
from dpetools.exceptions import DPEApiClientException, InvalidDPERecordsLimitError


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
    api_data_url = Container.api_data_url
    return DPEApiClient(api_data_url=api_data_url)


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
        (None, NB_RECORDS_DEFAULT),  # Default limit
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
