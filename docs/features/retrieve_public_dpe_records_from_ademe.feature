Feature: Query DPE data without specifying query parameters

  As a user of the DPE Tools library
  I want to query the ADEME API without specifying any query parameters
  So that I can retrieve a default list of available DPE records

  Rule: R1 - Retrieve DPE data using default API behavior

    @happy
    Example: R1E1 - Get a list of DPE records with default query
      Given the ADEME DPE API is reachable at "https://data.ademe.fr/data-fair/api/v1/datasets/dpe03existant/lines"
      When I query the DPE data endpoint without specifying any parameters
      Then I should receive a response with HTTP status code 200
      And the response should contain at least 1 record
      And each record should contain a non-empty field "numero_dpe"

  Rule: R2 - Handle API unavailability

    @sad
    Example: R2E1 - Gracefully handle API connectivity failure
      Given the ADEME DPE API is not reachable
      When I query the DPE data endpoint
      Then I should receive an error indicating the API is unavailable
      And the error message should mention "connectivity" or "unreachable"
