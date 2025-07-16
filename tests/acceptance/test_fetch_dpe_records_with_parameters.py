from typing import Any

import pandas as pd
import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from dpetools.api_client import DPEApiClient
from dpetools.exceptions import InvalidDPERecordsLimitError, NonExistingColumnError

# Link the .feature file
scenarios("../../docs/features/fetch_dpe_records_with_parameters.feature")

# ███████╗██╗██╗  ██╗████████╗██╗   ██╗██████╗ ███████╗███████╗
# ██╔════╝██║╚██╗██╔╝╚══██╔══╝██║   ██║██╔══██╗██╔════╝██╔════╝
# █████╗  ██║ ╚███╔╝    ██║   ██║   ██║██████╔╝█████╗  ███████╗
# ██╔══╝  ██║ ██╔██╗    ██║   ██║   ██║██╔══██╗██╔══╝  ╚════██║
# ██║     ██║██╔╝ ██╗   ██║   ╚██████╔╝██║  ██║███████╗███████║
# ╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝


@pytest.fixture(scope="session")
def dpe_api_client() -> DPEApiClient:
    """
    Fixture to create a DPEAPIClient instance for testing.
    """
    return DPEApiClient()


#  ██████╗ ██╗██╗   ██╗███████╗███╗   ██╗    ███████╗████████╗███████╗██████╗ ███████╗
# ██╔════╝ ██║██║   ██║██╔════╝████╗  ██║    ██╔════╝╚══██╔══╝██╔════╝██╔══██╗██╔════╝
# ██║  ███╗██║██║   ██║█████╗  ██╔██╗ ██║    ███████╗   ██║   █████╗  ██████╔╝███████╗
# ██║   ██║██║╚██╗ ██╔╝██╔══╝  ██║╚██╗██║    ╚════██║   ██║   ██╔══╝  ██╔═══╝ ╚════██║
# ╚██████╔╝██║ ╚████╔╝ ███████╗██║ ╚████║    ███████║   ██║   ███████╗██║     ███████║
#  ╚═════╝ ╚═╝  ╚═══╝  ╚══════╝╚═╝  ╚═══╝    ╚══════╝   ╚═╝   ╚══════╝╚═╝     ╚══════╝


@given("the ADEME DPE API is reachable")
def given_api_is_reachable(dpe_api_client: DPEApiClient) -> None:
    """
    Ensure that the DPE API is reachable before running tests.
    This step is crucial to avoid running tests against an unreachable API.
    """
    assert dpe_api_client.is_api_reachable()


# ██╗    ██╗██╗  ██╗███████╗███╗   ██╗    ███████╗████████╗███████╗██████╗ ███████╗
# ██║    ██║██║  ██║██╔════╝████╗  ██║    ██╔════╝╚══██╔══╝██╔════╝██╔══██╗██╔════╝
# ██║ █╗ ██║███████║█████╗  ██╔██╗ ██║    ███████╗   ██║   █████╗  ██████╔╝███████╗
# ██║███╗██║██╔══██║██╔══╝  ██║╚██╗██║    ╚════██║   ██║   ██╔══╝  ██╔═══╝ ╚════██║
# ╚███╔███╔╝██║  ██║███████╗██║ ╚████║    ███████║   ██║   ███████╗██║     ███████║
#  ╚══╝╚══╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝    ╚══════╝   ╚═╝   ╚══════╝╚═╝     ╚══════╝


@when(parsers.parse("I fetch DPE records with a limit of {nbrecords:d}"), target_fixture="dpe_records_dataframe")
@when("I fetch DPE records without specifying a limit", target_fixture="dpe_records_dataframe")
def when_fetch_with_limit(dpe_api_client: DPEApiClient, nbrecords: int | None = None) -> pd.DataFrame:
    """
    Fetch DPE records from the API with an optional limit.
    If no limit is specified, it defaults to the API's default number of records.
    """
    if nbrecords is None:
        dpe_records_dataframe = dpe_api_client.fetch_dpe_records()
    else:
        dpe_records_dataframe = dpe_api_client.fetch_dpe_records(nbrecords=nbrecords)

    return dpe_records_dataframe


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


@when(parsers.parse('I fetch DPE records sorted by "{field}" in {order} order'), target_fixture="dpe_records_dataframe")
def when_fetch_sorted_element(dpe_api_client: DPEApiClient, field: str, order: str) -> pd.DataFrame:
    """
    Fetch DPE records sorted by a specified field in either ascending or descending order.

    Args:
        dpe_api_client (DPEApiClient): The API client to fetch records.
        field (str): The field by which to sort the records.
        order (str): The order of sorting, either "ascending" or "descending".
    """
    sort_order = "asc" if order == "ascending" else "desc"
    dpe_records_dataframe = dpe_api_client.fetch_dpe_records(sort_by=field, order=sort_order, nbrecords=10)

    return dpe_records_dataframe


@when(parsers.parse('I fetch DPE records sorted by "{field}"'), target_fixture="fetch_error")
def when_fetch_sorted_by_invalid_field(dpe_api_client: DPEApiClient, field: str) -> pytest.ExceptionInfo:
    """
    Attempt to fetch DPE records sorted by a non-existent field and capture the exception.

    Args:
        dpe_api_client (DPEApiClient): The API client to fetch records.
        field (str): The field by which to sort the records, which does not exist.

    Returns:
        pytest.ExceptionInfo: The exception information captured during the fetch attempt.
    """
    with pytest.raises(NonExistingColumnError) as exc_info:
        dpe_api_client.fetch_dpe_records(sort_by=field, nbrecords=10)
    return {"exc_info": exc_info, "field": field}


@when(
    parsers.parse('I fetch DPE records selecting columns "{col_name_1}" and "{col_name_2}"'),
    target_fixture="run_info",
)
def when_fetch_selecting_columns(dpe_api_client: DPEApiClient, col_name_1: str, col_name_2: str) -> dict[str, Any]:
    """
    Fetch DPE records selecting specific columns.

    Args:
        dpe_api_client (DPEApiClient): The API client to fetch records.
        col_name_1 (str): The first column to select.
        col_name_2 (str): The second column to select.

    Returns:
        dict[str, Any]: A dictionary containing the DataFrame and any exception information and the selected column names.
        If an exception occurs, the DataFrame will be None and the exception information will be captured
    """
    try:
        dpe_records_dataframe = dpe_api_client.fetch_dpe_records(select_columns=[col_name_1, col_name_2])
        exception_info = None
    except NonExistingColumnError as excinfo:
        dpe_records_dataframe = None
        exception_info = excinfo
        
    return {"dataframe": dpe_records_dataframe, "exc_info": exception_info, "col_names": [col_name_1, col_name_2]}

@when("I fetch DPE records without specifying columns to select", target_fixture="dpe_records_dataframe")
def when_fetch_all_columns(dpe_api_client: DPEApiClient) -> pd.DataFrame:
    """
    Fetch all DPE records without specifying any columns to select.
    This will return all available columns in the DataFrame.
    
    Args:
        dpe_api_client (DPEApiClient): The API client to fetch records.
    """
    return dpe_api_client.fetch_dpe_records(select_columns=None)

@when(parsers.parse('I fetch DPE records filtering where "{field_1}" is "{value_1}" and "{field_2}" is "{value_2}"'), target_fixture="dpe_records_dataframe")
def when_fetch_filtered_records(dpe_api_client: DPEApiClient, field_1: str, value_1: str, field_2: str, value_2: str) -> pd.DataFrame:
    """
    Fetch DPE records filtered by specific field values.

    Args:
        dpe_api_client (DPEApiClient): The API client to fetch records.
        field_1 (str): The first field to filter by.
        value_1 (str): The value for the first field.
        field_2 (str): The second field to filter by.
        value_2 (str): The value for the second field.

    Returns:
        pd.DataFrame: A DataFrame containing the filtered DPE records.
    """
    filter_with = {field_1: value_1, field_2: value_2}
    return dpe_api_client.fetch_dpe_records(filter_with=filter_with)


# ████████╗██╗  ██╗███████╗███╗   ██╗    ███████╗████████╗███████╗██████╗ ███████╗
# ╚══██╔══╝██║  ██║██╔════╝████╗  ██║    ██╔════╝╚══██╔══╝██╔════╝██╔══██╗██╔════╝
#    ██║   ███████║█████╗  ██╔██╗ ██║    ███████╗   ██║   █████╗  ██████╔╝███████╗
#    ██║   ██╔══██║██╔══╝  ██║╚██╗██║    ╚════██║   ██║   ██╔══╝  ██╔═══╝ ╚════██║
#    ██║   ██║  ██║███████╗██║ ╚████║    ███████║   ██║   ███████╗██║     ███████║
#    ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝    ╚══════╝   ╚═╝   ╚══════╝╚═╝     ╚══════╝


@then(parsers.parse("exactly {nbrecords:d} records are returned"))
@then(parsers.parse("exactly {nbrecords:d} records are returned by default"))
def then_receive_exactly_n_records(nbrecords: int, dpe_records_dataframe: pd.DataFrame) -> None:
    """
    Assert that the number of records received matches the expected count.
    """
    assert len(dpe_records_dataframe) == nbrecords, (
        f"Expected {nbrecords} records, but received {len(dpe_records_dataframe)}"
    )


@then("I should receive an error indicating the limit must be a positive integer")
def then_error_limit_positive_integer(fetch_error):
    """
    Assert that the error message indicates the limit must be a positive integer.

    Args:
        fetch_error (pytest.ExceptionInfo): The exception information captured during the fetch attempt.

    """
    assert "positive integer" in str(fetch_error.value)


@then(parsers.parse('the records are ordered from oldest to newest by "{field}"'))
def then_records_ordered_oldest_to_newest(dpe_records_dataframe: pd.DataFrame, field: str) -> None:
    """
    Assert that the records are ordered from oldest to newest by the specified field.

    Args:
        dpe_records_dataframe (pd.DataFrame): The DataFrame containing the fetched DPE records.
        field (str): The field by which to check the order of records.
    """
    assert dpe_records_dataframe[field].is_monotonic_increasing, (
        f"The records are not ordered by '{field}' in ascending order."
    )


@then(parsers.parse('the records are ordered from newest to oldest by "{field}"'))
def then_records_ordered_newest_to_oldest(dpe_records_dataframe: pd.DataFrame, field: str) -> None:
    """
    Assert that the records are ordered from newest to oldest by the specified field.

    Args:
        dpe_records_dataframe (pd.DataFrame): The DataFrame containing the fetched DPE records.
        field (str): The field by which to check the order of records.
    """
    assert dpe_records_dataframe[field].is_monotonic_decreasing, (
        f"The records are not ordered by '{field}' in descending order."
    )


@then("an error is returned indicating the sort field is invalid")
def then_error_sort_field_invalid(fetch_error: dict[str, Any]) -> None:
    """
    Assert that the error message indicates the sort field is invalid.

    Args:
        fetch_error (pytest.ExceptionInfo): The exception information captured during the fetch attempt.
    """
    error: pytest.ExceptionInfo = fetch_error["exc_info"]
    field_name = fetch_error["field"]

    assert str(error.value).startswith(
        f"The requested column(s) ['{field_name}'] do not exist in the available columns:"
    ), f"Expected error message to indicate non-existing columns, but got: {error.value}"


@then(parsers.parse('each returned record contains only the fields "{col_name_1}" and "{col_name_2}"'))
def then_only_selected_fields(col_name_1: str, col_name_2: str, run_info: dict[str, Any]) -> None:
    """
    Assert that each record in the DataFrame contains only the specified fields.

    Args:
        run_info (dict[str, Any]): The dictionary containing the DataFrame and any exception information.
        col_name_1 (str): The first column to check.
        col_name_2 (str): The second column to check.
    """
    expected_columns = [col_name_1, col_name_2]
    actual_columns = list(run_info["dataframe"].columns)

    assert set(expected_columns) - set(actual_columns) == set(), (
        f"Expected columns {expected_columns} not found in the DataFrame. Actual columns: {actual_columns}."
    )

@then("each returned record contains all available fields")
def then_all_fields_present(dpe_records_dataframe: pd.DataFrame, dpe_api_client: DPEApiClient) -> None:
    """
    Assert that each record in the DataFrame contains all available fields.

    Args:
        dpe_records_dataframe (pd.DataFrame): The DataFrame containing the fetched DPE records.
        dpe_api_client (DPEApiClient): The API client to fetch available columns.
    """
    actual_columns = list(dpe_records_dataframe.columns)

    assert len(actual_columns) > 0, "The DataFrame should not be empty."

@then("an error is returned indicating the selected columns are invalid")
def then_error_selected_columns_invalid(run_info: dict[str, Any]) -> None:
    """
    Assert that the error message indicates the sort field is invalid.

    Args:
        run_info (dict[str, Any]): The dictionary containing the DataFrame and any exception information and the selected column names.
    """
    error: pytest.ExceptionInfo = run_info["exc_info"]
    field_name = run_info["col_names"][1]

    assert isinstance(error, NonExistingColumnError), (
        f"Expected NonExistingColumnError, but got {type(error.value)}: {error}"
    )

    assert str(error).startswith(
        f"The requested column(s) ['{field_name}'] do not exist in the available columns:"
    ), f"Expected error message to indicate non-existing columns, but got: {error}"


# Then all returned records have "code_insee_ban" equal to "77014"
# And all returned records have "etiquette_dpe" equal to "B"
@then(parsers.parse('all returned records have "{field}" equal to "{value}"'))
def then_all_records_have_field_value(dpe_records_dataframe: pd.DataFrame, field: str, value: str) -> None:
    """
    Assert that all returned records have a specific field equal to a given value.

    Args:
        dpe_records_dataframe (pd.DataFrame): The DataFrame containing the fetched DPE records.
        field (str): The field to check.
        value (str): The expected value for the field.
    """
    assert all(dpe_records_dataframe[field] == value), (
        f"Not all records have '{field}' equal to '{value}'."
    )