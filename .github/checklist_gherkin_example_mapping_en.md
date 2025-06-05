# Step-by-step Checklist: Writing a Gherkin v6+ Feature from Example Mapping

## 1. Preparing the Example Mapping Workshop

- [ ] Gather stakeholders (PO, devs, testers, business, etc.)
- [ ] Define the business subject or objective to explore
- [ ] Prepare a board or colored sticky notes:
  - Yellow: User Stories/Business Rules
  - Blue: Examples
  - Red: Questions

## 2. Running the Example Mapping

- [ ] List business rules (yellow cards) describing the expected behavior, formulated in business language and user story under the following format:
  - In order to _achieve goal_, as a _user role_, I want to _action_ [so that _benefit_].
- [ ] For each rule, propose concrete examples (blue cards)
- [ ] Note questions or uncertainties (red cards) to clarify
- [ ] Ensure each rule is illustrated by at least one example
- [ ] Review and validate shared understanding with the group

## 3. Transforming Example Mapping into Gherkin v6+

- [ ] Create a `.feature` file in `docs/features/` with an explicit name
- [ ] Write the `Feature:` title in business language
- [ ] Add a business description (optional but recommended), including business context, purpose, and—if possible—a link to evergreen business documentation or knowledge base
- [ ] Use the `Background:` section for shared context (if needed)
- [ ] For each business rule, add a `Rule:` block with an explicit title and, if possible, a short explanation or business rationale
- [ ] For each example, write an `Example:` block (preferred in Gherkin v6+), or `Scenario:`/`Scenario Outline:` if required by your tooling, under the relevant rule
- [ ] Use business language, clear and declarative steps:
  - `Given`
  - `When`
  - `Then`
  - Use `And`/`But` for readability
- [ ] Use `Examples:` for `Scenario Outline:` if variations are needed
- [ ] Add tags (`@happy`, `@sad`, `@edge`, etc.) to categorize scenarios
- [ ] Where possible, reference or link to business knowledge, evergreen documentation, or domain glossary for traceability and shared understanding

## 4. Gherkin Quality Check

- [ ] Are steps written in business language, without technical jargon?
- [ ] Are scenarios independent, atomic, and testable?
- [ ] Do rules and examples cover all identified business cases?
- [ ] Are unresolved questions documented or escalated?
- [ ] Is the file readable by a non-technical person?
- [ ] Are steps reusable and intention-revealing?
- [ ] Are scenarios tagged to facilitate test campaigns?

## 5. Living Documentation and Maintenance

- [ ] Is the `.feature` file versioned and accessible to all?
- [ ] Are business changes systematically reflected in the Gherkin?
- [ ] Are scenarios validated by automated tests (ATDD)?
- [ ] Is the file reviewed and updated with every change in requirements?

---

## Example of Gherkin v6+ Structure

```gherkin
Feature: Consult DPE by reference
  In order to consult a public DPE,
  as a user,
  I want to consult a public DPE using its unique reference.
  So that I can verify its details and validity.

  Allow a user to consult a public DPE using its unique reference.

  Background:
    Given the user is authenticated

  Rule: The reference exists
    @happy
    Example: Consult an existing DPE
      When the user enters a valid reference
      Then the corresponding DPE is displayed

  Rule: The reference does not exist
    @sad
    Example: Consult a non-existent DPE
      When the user enters an unknown reference
      Then an error message is displayed
```

---

> This checklist ensures that every Gherkin feature is the result of shared understanding, is well-documented, testable, and maintainable, and aligns with BDD/ATDD best practices and living documentation.
