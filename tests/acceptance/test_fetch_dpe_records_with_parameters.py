import pytest
from pytest_bdd import scenarios, given, when, then, parsers

# Link the .feature file
scenarios('../../docs/features/fetch_dpe_records_with_parameters.feature')

@given("the ADEME DPE API is reachable")
def given_api_is_reachable(_=None): ...

@when(parsers.parse('I fetch DPE records with limit {limit:d}'))
def when_fetch_with_limit(_=None): ...

@when("I fetch DPE records without specifying a limit")
def when_fetch_with_default_limit(_=None): ...

@then(parsers.parse('I should receive exactly {n:d} records'))
def then_receive_exactly_n_records(_=None): 
    assert False

@then(parsers.parse('I should receive {n:d} records'))
def then_receive_n_records(_=None): 
    assert False

@when(parsers.parse('I fetch DPE records sorted by "{field}" in ascending order'))
def when_fetch_sorted_ascending(_=None): ...

@when(parsers.parse('I fetch DPE records sorted by "{field}" in descending order'))
def when_fetch_sorted_descending(_=None): ...

@then(parsers.parse('the records should be ordered from oldest to newest by "{field}"'))
def then_records_ordered_oldest_to_newest(_=None): 
    assert False

then(parsers.parse('the records should be ordered from newest to oldest by "{field}"'))
def then_records_ordered_newest_to_oldest(_=None): 
    assert False

@when(parsers.parse('I fetch DPE records selecting columns "{col1}" and "{col2}"'))
def when_fetch_selecting_columns(_=None): ...

@when("I fetch DPE records without specifying columns to select")
def when_fetch_all_columns(_=None): ...

@then(parsers.parse('each record should only contain the fields "{col1}" and "{col2}"'))
def then_only_selected_fields(_=None): 
    assert False

@then("each record should contain all available fields")
def then_all_fields_present(_=None): 
    assert False

@when(parsers.parse('I fetch DPE records filtering where "{field1}" is "{value1}" and "{field2}" is "{value2}"'))
def when_fetch_with_filters(_=None): ...

@then(parsers.parse('all returned records should have "{field}" equal to "{value}"'))
def then_all_records_have_field_value(_=None): 
    assert False

@when(parsers.parse('I fetch DPE records searching for "{search_term}" in fields "{field1}" and "{field2}"'))
def when_fetch_full_text_search(_=None): ...

@then(parsers.parse('all returned records should contain "{search_term}" in either "{field1}" or "{field2}"'))
def then_all_records_contain_search_term(_=None): 
    assert False

@when(parsers.parse('I fetch DPE records sorted by "{field}" in ascending order'))
def when_fetch_sorted_by_invalid_field(_=None): ...

@then("I should receive an error indicating the sort field is invalid")
def then_error_sort_field_invalid(_=None): 
    assert False

@when(parsers.parse('I fetch DPE records selecting columns "{col1}" and "{col2}"'))
def when_fetch_selecting_invalid_columns(_=None): ...

@then("I should receive an error indicating one or more selected columns are invalid")
def then_error_selected_columns_invalid(_=None): 
    assert False

@when(parsers.parse('I fetch DPE records filtering where "{field}" is "{value}"'))
def when_fetch_with_invalid_filter(_=None): ...

@then("I should receive an error indicating the filter field is invalid")
def then_error_filter_field_invalid(_=None): 
    assert False

@when(parsers.parse('I fetch DPE records with limit {limit:d}'))
def when_fetch_with_negative_limit(_=None): ...

@then("I should receive an error indicating the limit must be a positive integer")
def then_error_limit_positive_integer(_=None): 
    assert False
