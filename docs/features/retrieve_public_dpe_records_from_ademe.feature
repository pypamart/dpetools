Feature: Retrieve DPE records from ADEME API without query parameters
  In order to access energy performance data for existing housing
  As a user of the DPE Tools library
  I want to query the ADEME API without specifying parameters to get a default list of DPE records

  This feature covers the default API behavior and error handling for connectivity issues.

  Rule: R1 - Default API query returns DPE records
    @happy
    Example: R1E1 - Successful retrieval with default query
      Given the ADEME DPE API is reachable at "https://data.ademe.fr/data-fair/api/v1/datasets/dpe03existant/lines"
      When I query the DPE data endpoint without specifying any parameters
      Then I should receive a response with HTTP status code 200
      And the response should contain at least 1 DPE record
      And each DPE record should have a non-empty "numero_dpe" field

  Rule: R2 - API connectivity errors are handled gracefully
    @sad
    Example: R2E1 - API is unavailable
      Given the ADEME DPE API is not reachable
      When I query the DPE data endpoint
      Then I should receive an error indicating the API is unavailable
      And the error message should mention "connectivity" or "unreachable"