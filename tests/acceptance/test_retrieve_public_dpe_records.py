import pandas as pd
import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from dpetools.api_client import DPEApiClient
from dpetools.config.container import Container
from dpetools.exceptions import DPEApiClientException

# Link the .feature file
scenarios("../../docs/features/retrieve_public_dpe_records_from_ademe.feature")


# Shared variables
@pytest.fixture
def dpe_api_client():
    """
    Fixture to create a DPEAPIClient instance for testing.
    """
    api_data_url = Container.api_data_url
    return DPEApiClient(api_data_url=api_data_url)


@pytest.fixture
def context() -> dict[str, str]:
    """
    Fixture to provide a context dictionary for storing shared data between steps.
    """
    return {}


# Steps for Rule: Retrieve DPE data using default API behavior


@given(parsers.cfparse('the ADEME DPE API is reachable at "{url}"'))
def ademe_api_reachable(dpe_api_client: DPEApiClient, url: str):
    assert Container.api_data_url == url
    assert dpe_api_client.is_api_reachable()


@when(
    "I query the DPE data endpoint without specifying any parameters",
    target_fixture="dpe_records_dataframe",
)
def query_dpe_data(dpe_api_client: DPEApiClient) -> pd.DataFrame:
    dpe_records_dataframe = dpe_api_client.fetch_dpe_records()
    return dpe_records_dataframe


@then("I should receive a response with HTTP status code 200")
def check_http_200(dpe_records_dataframe: pd.DataFrame):
    assert isinstance(dpe_records_dataframe, pd.DataFrame)


@then("the response should contain at least 1 record")
def check_non_empty_response(dpe_records_dataframe: pd.DataFrame):
    assert not dpe_records_dataframe.empty, (
        "The response should contain at least one record"
    )


@then(parsers.cfparse('each record should contain a non-empty field "{field}"'))
def check_field_present(dpe_records_dataframe, field):
    assert field in dpe_records_dataframe.columns, (
        f"The field '{field}' should be present in the records"
    )
    assert not dpe_records_dataframe[field].isnull().all(), (
        f"The field '{field}' should not be empty in all records"
    )
    assert (
        not dpe_records_dataframe[field].apply(lambda x: str(x).strip() == "").all()
    ), f"The field '{field}' should not be empty in all records"


# Steps for Rule: Handle API unavailability


@given("the ADEME DPE API is not reachable")
def api_unreachable(monkeypatch):
    # Monkeypatch requests.get to always raise a RequestException
    import requests

    monkeypatch.setattr(
        "requests.get",
        lambda *args, **kwargs: (_ for _ in ()).throw(
            requests.RequestException("API connectivity error")
        ),
    )


@when("I query the DPE data endpoint")
def query_dpe_data_unreachable(dpe_api_client: DPEApiClient, context: dict[str, str]):
    with pytest.raises(DPEApiClientException) as exc_info:
        dpe_api_client.fetch_dpe_records()

    context["error"] = str(exc_info.value)


@then("I should receive an error indicating the API is unavailable")
def check_error_received(context: dict[str, str]):
    assert context.get("error") is not None, "Expected an error but none was raised."
    assert (
        "unavailable" in context["error"].lower()
        or "error" in context["error"].lower()
        or "connectivity" in context["error"].lower()
    ), f"Error message should indicate unavailability, got: {context['error']}"


@then(parsers.parse('the error message should mention "{keyword}"'))
def check_error_message(context: dict[str, str], keyword: str):
    assert context.get("error") is not None, "No error message captured."
    # Accept if any of the keywords (split by ' or ') are present in the error message
    keywords = [keyword_item.strip('" ') for keyword_item in keyword.split("or")]
    error_msg = context["error"].lower()
    assert any(
        expected_keyword.lower() in error_msg for expected_keyword in keywords
    ), f"Expected one of {keywords} in error message, got: {context['error']}"
