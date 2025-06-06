Feature: Fetch DPE data with query parameters

  As a user of the DPE Tools library
  I want to fetch DPE records with advanced query parameters
  So that I can control the number, order, and content of the records returned

  Background:
    Given the ADEME DPE API is reachable

  Rule: R1 - Limit the number of records returned

    @happy
    Example: R1E1 - Get a custom number of DPE records
      When I fetch DPE records with limit 10
      Then I should receive exactly 10 records

    @happy
    Example: R1E2 - Use the default number of records
      When I fetch DPE records without specifying a limit
      Then I should receive exactly 50 records
    
    @sad @edge
    Scenario Outline: R1E3 - Use a negative limit
    When I fetch DPE records with a non strict positive limit equals to <nbrecords>
    Then I should receive an error indicating the limit must be a positive integer

    Examples:
      | nbrecords |
      | 0         |
      | -1        |
      | -10       |

  Rule: R2 - Sort records by a specific field

    @happy
    Example: R2E1 - Sort records by 'date_etablissement_dpe' ascending
      When I fetch DPE records sorted by "date_etablissement_dpe" in ascending order
      Then the records should be ordered from oldest to newest by "date_etablissement_dpe"

    @happy
    Example: R2E2 - Sort records by 'date_etablissement_dpe' descending
      When I fetch DPE records sorted by "date_etablissement_dpe" in descending order
      Then the records should be ordered from newest to oldest by "date_etablissement_dpe"

    @sad
    Example: R2E3 - Sort by a non-existent field
      When I fetch DPE records sorted by "not_a_field" that does not exists
      Then I should receive an error indicating the sort field is invalid

  Rule: R3 - Select specific columns

    @happy
    Example: R3E1 - Select only 'adresse_ban' and 'date_etablissement_dpe'
      When I fetch DPE records selecting columns "adresse_ban" and "date_etablissement_dpe"
      Then each record should only contain the fields "adresse_ban" and "date_etablissement_dpe"

    @happy
    Example: R3E2 - Select all columns by default
      When I fetch DPE records without specifying columns to select
      Then each record should contain all available fields

    @sad
    Example: R3E3 - Select a non-existent column
      When I fetch DPE records selecting columns "adresse_ban" and "not_a_column"
      Then I should receive an error indicating one or more selected columns are invalid

  Rule: R4 - Filter records by field values

    @happy
    Example: R4E1 - Filter records by 'code_insee_ban' and 'etiquette_dpe'

      When I fetch DPE records filtering where "code_insee_ban" is "77014" and "etiquette_dpe" is "B"
      Then all returned records should have "code_insee_ban" equal to "77014"
      And all returned records should have "etiquette_dpe" equal to "B"
      
    @sad
    Example: R4E2 - Filter by a non-existent field
        When I fetch DPE records filtering where "not_a_field" is "value"
        Then I should receive an error indicating the filter field is invalid

