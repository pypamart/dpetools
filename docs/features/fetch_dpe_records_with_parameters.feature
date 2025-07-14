Feature: Fetch DPE records with advanced query parameters

  In order to analyze and process DPE data efficiently
  As a user of the DPE Tools library using the DPE Tools library
  I want to fetch DPE records with control over quantity, sorting, selection, and filtering


  Background:
    Given the ADEME DPE API is reachable

  Rule: R1 - The user can control the number of DPE records returned per request

    @happy
    Example: R1E1 - The user requests a specific number of records
      When I fetch DPE records with a limit of 10
      Then exactly 10 records are returned

    @happy
    Example: R1E2 - The user omits the limit parameter
      When I fetch DPE records without specifying a limit
      Then exactly 50 records are returned by default

    @sad @edge
    Scenario Outline: R1E3 - The user provides an invalid limit
      When I fetch DPE records with a non strict positive limit equals to <nbrecords>
      Then I should receive an error indicating the limit must be a positive integer

      Examples:
        | nbrecords |
        | 0         |
        | -1        |
        | -10       |

  Rule: R2 - The user can sort DPE records by a valid field

    @happy
    Example: R2E1 - Sort records by 'date_etablissement_dpe' ascending
      When I fetch DPE records sorted by "date_etablissement_dpe" in ascending order
      Then the records are ordered from oldest to newest by "date_etablissement_dpe"

    @happy
    Example: R2E2 - Sort records by 'date_etablissement_dpe' descending
      When I fetch DPE records sorted by "date_etablissement_dpe" in descending order
      Then the records are ordered from newest to oldest by "date_etablissement_dpe"

    @sad
    Example: R2E3 - Sort by an invalid field
      When I fetch DPE records sorted by "not_a_field"
      Then an error is returned indicating the sort field is invalid

  Rule: R3 - The user can select which fields to include in the returned records

    @happy
    Example: R3E1 - Select only 'adresse_ban' and 'date_etablissement_dpe'
      When I fetch DPE records selecting columns "adresse_ban" and "date_etablissement_dpe"
      Then each returned record contains only the fields "adresse_ban" and "date_etablissement_dpe"

    @happy
    Example: R3E2 - Select all columns by default
      When I fetch DPE records without specifying columns to select
      Then each returned record contains all available fields

    @sad
    Example: R3E3 - Select a non-existent column
      When I fetch DPE records selecting columns "adresse_ban" and "not_a_column"
      Then an error is returned indicating the selected columns are invalid

  Rule: R4 - The user can filter DPE records by valid field values

    @happy
    Example: R4E1 - Filter records by 'code_insee_ban' and 'etiquette_dpe'
      When I fetch DPE records filtering where "code_insee_ban" is "77014" and "etiquette_dpe" is "B"
      Then all returned records have "code_insee_ban" equal to "77014"
      And all returned records have "etiquette_dpe" equal to "B"

    @sad
    Example: R4E2 - Filter by an invalid field
      When I fetch DPE records filtering where "not_a_field" is "value"
      Then an error is returned indicating the filter field is invalid