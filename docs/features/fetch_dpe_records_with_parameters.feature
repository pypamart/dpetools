Feature: Fetch DPE data with query parameters

  As a user of the DPE Tools library
  I want to fetch DPE records with advanced query parameters
  So that I can control the number, order, and content of the records returned

  Background:
    Given the ADEME DPE API is reachable

  Rule: Limit the number of records returned

    @happy
    Example: Get a custom number of DPE records
      When I fetch DPE records with limit 10
      Then I should receive exactly 10 records

    @happy
    Example: Use the default number of records
      When I fetch DPE records without specifying a limit
      Then I should receive 50 records
    
    @sad
    Example: Use a negative limit
    When I fetch DPE records with limit -5
    Then I should receive an error indicating the limit must be a positive integer

  Rule: Sort records by a specific field

    @happy
    Example: Sort records by 'date_etablissement_dpe' ascending
      When I fetch DPE records sorted by "date_etablissement_dpe" in ascending order
      Then the records should be ordered from oldest to newest by "date_etablissement_dpe"

    @happy
    Example: Sort records by 'date_etablissement_dpe' descending
      When I fetch DPE records sorted by "date_etablissement_dpe" in descending order
      Then the records should be ordered from newest to oldest by "date_etablissement_dpe"

    @sad
    Example: Sort by a non-existent field
      When I fetch DPE records sorted by "not_a_field" in ascending order
      Then I should receive an error indicating the sort field is invalid

  Rule: Select specific columns

    @happy
    Example: Select only 'adresse_ban' and 'date_etablissement_dpe'
      When I fetch DPE records selecting columns "adresse_ban" and "date_etablissement_dpe"
      Then each record should only contain the fields "adresse_ban" and "date_etablissement_dpe"

    @happy
    Example: Select all columns by default
      When I fetch DPE records without specifying columns to select
      Then each record should contain all available fields

    @sad
    Example: Select a non-existent column
      When I fetch DPE records selecting columns "adresse_ban" and "not_a_column"
      Then I should receive an error indicating one or more selected columns are invalid

  Rule: Filter records by field values

    @happy
    Example: Filter records by 'code_insee_ban' and 'etiquette_dpe'

      When I fetch DPE records filtering where "code_insee_ban" is "77014" and "etiquette_dpe" is "B"
      Then all returned records should have "code_insee_ban" equal to "77014"
      And all returned records should have "etiquette_dpe" equal to "B"
      
    @sad
    Example: Filter by a non-existent field
        When I fetch DPE records filtering where "not_a_field" is "value"
        Then I should receive an error indicating the filter field is invalid

