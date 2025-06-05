import pandas as pd
import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from dpetools.api_client import DPEApiClient
from dpetools.config.container import Container
from dpetools.exceptions import InvalidDPERecordsLimitError

# Link the .feature file
scenarios("../../docs/features/fetch_dpe_records_with_parameters.feature")


@pytest.fixture
def dpe_api_client() -> DPEApiClient:
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


@given("the ADEME DPE API is reachable")
def given_api_is_reachable(dpe_api_client: DPEApiClient) -> None:
    """
    Ensure that the DPE API is reachable before running tests.
    This step is crucial to avoid running tests against an unreachable API.
    """
    assert dpe_api_client.is_api_reachable()


@when(parsers.parse("I fetch DPE records with limit {nbrecords:d}"), target_fixture="dpe_records_dataframe")
@when("I fetch DPE records without specifying a limit", target_fixture="dpe_records_dataframe")
def when_fetch_with_limit(dpe_api_client: DPEApiClient, nbrecords: int | None = None) -> pd.DataFrame:
    """
    Fetch DPE records from the API with an optional limit.
    If no limit is specified, it defaults to the API's default number of records.
    """
    dpe_records_dataframe = dpe_api_client.fetch_dpe_records(nbrecords=nbrecords)
    return dpe_records_dataframe


@then(parsers.parse("I should receive exactly {nbrecords:d} records"))
@then(parsers.parse("I should receive {nbrecords:d} records"))
def then_receive_exactly_n_records(nbrecords: int, dpe_records_dataframe: pd.DataFrame) -> None:
    """
    Assert that the number of records received matches the expected count.
    """
    assert len(dpe_records_dataframe) == nbrecords, (
        f"Expected {nbrecords} records, but received {len(dpe_records_dataframe)}"
    )


@when(
    parsers.parse("I fetch DPE records with a non strict positive limit equals to {nbrecords:d}"),
    target_fixture="fetch_error",
)
def when_fetch_with_negative_limit(dpe_api_client: DPEApiClient, nbrecords: int) -> pytest.ExceptionInfo:
    """
    Attempt to fetch DPE records with a negative limit and capture the exception.
    """
    with pytest.raises(InvalidDPERecordsLimitError) as exc_info:
        dpe_api_client.fetch_dpe_records(nbrecords=nbrecords)
    return exc_info


@then("I should receive an error indicating the limit must be a positive integer")
def then_error_limit_positive_integer(fetch_error):
    """
    Assert that the error message indicates the limit must be a positive integer.
    """
    assert "positive integer" in str(fetch_error.value)


def then_receive_n_records(_=None):
    raise AssertionError()


@when(parsers.parse('I fetch DPE records sorted by "{field}" in ascending order'))
def when_fetch_sorted_ascending(_=None): ...


@when(parsers.parse('I fetch DPE records sorted by "{field}" in descending order'))
def when_fetch_sorted_descending(_=None): ...


@then(parsers.parse('the records should be ordered from oldest to newest by "{field}"'))
def then_records_ordered_oldest_to_newest(_=None):
    raise AssertionError()


then(parsers.parse('the records should be ordered from newest to oldest by "{field}"'))


def then_records_ordered_newest_to_oldest(_=None):
    raise AssertionError()


@when(parsers.parse('I fetch DPE records selecting columns "{col1}" and "{col2}"'))
def when_fetch_selecting_columns(_=None): ...


@when("I fetch DPE records without specifying columns to select")
def when_fetch_all_columns(_=None): ...


@then(parsers.parse('each record should only contain the fields "{col1}" and "{col2}"'))
def then_only_selected_fields(_=None):
    raise AssertionError()


@then("each record should contain all available fields")
def then_all_fields_present(_=None):
    raise AssertionError()


@when(parsers.parse('I fetch DPE records filtering where "{field1}" is "{value1}" and "{field2}" is "{value2}"'))
def when_fetch_with_filters(_=None): ...


@then(parsers.parse('all returned records should have "{field}" equal to "{value}"'))
def then_all_records_have_field_value(_=None):
    raise AssertionError()


@when(parsers.parse('I fetch DPE records searching for "{search_term}" in fields "{field1}" and "{field2}"'))
def when_fetch_full_text_search(_=None): ...


@then(parsers.parse('all returned records should contain "{search_term}" in either "{field1}" or "{field2}"'))
def then_all_records_contain_search_term(_=None):
    raise AssertionError()


@when(parsers.parse('I fetch DPE records sorted by "{field}" in ascending order'))
def when_fetch_sorted_by_invalid_field(_=None): ...


@then("I should receive an error indicating the sort field is invalid")
def then_error_sort_field_invalid(_=None):
    raise AssertionError()


@when(parsers.parse('I fetch DPE records selecting columns "{col1}" and "{col2}"'))
def when_fetch_selecting_invalid_columns(_=None): ...


@then("I should receive an error indicating one or more selected columns are invalid")
def then_error_selected_columns_invalid(_=None):
    raise AssertionError()


@when(parsers.parse('I fetch DPE records filtering where "{field}" is "{value}"'))
def when_fetch_with_invalid_filter(_=None): ...


@then("I should receive an error indicating the filter field is invalid")
def then_error_filter_field_invalid(_=None):
    raise AssertionError()
