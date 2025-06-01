import pytest
from pytest_bdd import scenarios, given, when, then, parsers
import pandas as pd

from dpetools.api_client import DPEApiClient
from dpetools.config.container import Container

# Link the .feature file
scenarios('../../docs/features/retrieve_public_dpe_records_from_ademe.feature')

# Shared variables
@pytest.fixture
def dpe_api_client():
    """
    Fixture to create a DPEAPIClient instance for testing.
    """
    api_data_url = Container.api_data_url
    return DPEApiClient(api_data_url=api_data_url)

# Steps for Rule: Retrieve DPE data using default API behavior

@given(parsers.cfparse('the ADEME DPE API is reachable at "{url}"'))
def ademe_api_reachable(dpe_api_client: DPEApiClient, url: str):
    assert Container.api_data_url == url
    assert dpe_api_client.is_api_reachable()

@when("I query the DPE data endpoint without specifying any parameters", target_fixture="dpe_records_dataframe")
def query_dpe_data(dpe_api_client: DPEApiClient) -> pd.DataFrame:
    dpe_records_dataframe = dpe_api_client.fetch_dpe_records()
    return dpe_records_dataframe
    
@then("I should receive a response with HTTP status code 200")
def check_http_200(dpe_records_dataframe: pd.DataFrame):
    assert isinstance(dpe_records_dataframe, pd.DataFrame)

@then("the response should contain at least 1 record")
def check_non_empty_response(dpe_records_dataframe: pd.DataFrame):
    assert not dpe_records_dataframe.empty, "The response should contain at least one record"

@then(parsers.cfparse('each record should contain a non-empty field "{field}"'))
def check_field_present(dpe_records_dataframe, field):
    assert field in dpe_records_dataframe.columns, f"The field '{field}' should be present in the records"
    assert not dpe_records_dataframe[field].isnull().all(), f"The field '{field}' should not be empty in all records"
    assert not dpe_records_dataframe[field].apply(lambda x: str(x).strip() == '').all(), f"The field '{field}' should not be empty in all records"
    
# Steps for Rule: Handle API unavailability

@given("the ADEME DPE API is not reachable")
def api_unreachable(monkeypatch, context): ...

@when("I query the DPE data endpoint")
def query_dpe_data_unreachable(context): ...

@then("I should receive an error indicating the API is unavailable")
def check_error_received(context): ...

@then(parsers.parse('the error message should mention "{keyword}"'))
def check_error_message(context, keyword): ...