---
applyTo: "**/*.feature"
---
# Gherkin v6+ & DDD/BDD/Hexagonal/Clean Architecture/ATDD Best Practices

## Purpose
These instructions ensure Gherkin feature files are clear, business-focused living documentation, fully aligned with Domain-Driven Design (DDD), Hexagonal/Clean Architecture, and BDD/ATDD.

---

# Intelligent Assistant System Behavior
As an expert software crafter and intelligent assistant, I ensure that all Gherkin feature files and acceptance criteria are authored to the highest standards of clarity, business alignment with strategic Domain-Driven Design (DDD) principles, and architectural rigor. My guidance and examples are always implementation-agnostic, business-focused, and designed to serve as living documentation for the domain. I help teams write scenarios that are actionable, testable, and maintainable, supporting both technical and non-technical stakeholders in achieving shared understanding and continuous delivery of business value.

---

## 1. DDD, Hexagonal/Clean Architecture & Living Documentation Philosophy
- Use the language of the business and domain experts (ubiquitous language).
- Each feature must describe a clear business goal and value, not just a technical function.
- Avoid technical jargon; focus on observable outcomes and business intent.
- Feature files are the single source of truth for business requirements and acceptance criteria.
- Scenarios and rules should reflect bounded contexts, aggregates, and DDD invariants.
- Acceptance criteria must be testable at the domain/application layer, not just through the UI.
- Link with **Hexagonal/Clean Architecture:**
    - Write scenarios that describe business capabilities, not UI or infrastructure details.
    - Focus on domain events, aggregates, and business rules, not technical implementation.
    - Ensure scenarios are implementation-agnostic and can be tested at the application or domain service level.
    - Avoid referencing adapters, controllers, or infrastructure in Gherkin steps.
    - Use Gherkin to drive development from the outside-in, ensuring the core domain logic is isolated and testable.
    - Living documentation should reflect the business language and boundaries defined by your architecture, supporting maintainability and adaptability.

---

## 2. Structure & Organization
- Start with a descriptive `Feature:` and a short narrative:
  ```gherkin
  Feature: <Feature Name>
    In order to <business value>
    As a <domain persona>
    I want <capability>
  ```
- Use `Background:` for shared context (keep it concise and relevant).
- Use `Rule:` to group scenarios by business rules, DDD invariants, or aggregate boundaries.
- Use `Example` (or `Scenario`) for concrete, independent examples (prefer 1-3 per rule).
- Use `Scenario Outline` with `Examples` for parameterized business rules.
- Use tags (e.g. `@happy`, `@sad`, `@wip`, `@core`, `@integration`) for scenario categorization and filtering.
- Use @happy for positive/happy paths, and @sad (and optionally @edge) for negative, error, or edge-case scenarios.
- @sad and @edge paths are essential: they must illustrate business-meaningful exceptions, errors, or boundary conditions—not just technical failures.

---

## 3. Scenario Design & DDD Alignment
- Use `Given-When-Then` for all scenarios:
  - `Given`: domain context (entities, aggregates, value objects, state)
  - `When`: domain event, command, or action
  - `Then`: observable outcome or business invariant
- Each scenario should:
  - Illustrate a single, meaningful business example
  - Be independent and intention-revealing
  - Use real-world data and business terminology
  - Map directly to a business requirement, DDD invariant, or acceptance criterion
- Avoid implementation details, UI steps, or technical assertions.
- Prefer declarative steps ("Then the account is locked") over imperative ones ("Then set locked=true").
- Steps should be reusable, intention-revealing, and reflect the domain model.

---

## 4. Best Practices & Living Documentation
- Keep steps concise, expressive, and reusable.
- Use data tables and doc strings for complex data, but keep them readable.
- Use comments (`# ...`) for clarification, not for disabling scenarios.
- Regularly review and refactor feature files for clarity, removing duplication, and ensuring alignment with evolving business needs and domain language.
- Feature files must be kept up to date, reviewed, and accessible to both technical and non-technical stakeholders.

---

## 5. ATDD, TDD & INVEST Principles
- Write or update Gherkin feature files before implementation (ATDD outer loop).
- Acceptance tests must use real feature files and step definitions that reflect business language.
- Each scenario should be atomic, testable, and map directly to a business requirement or rule (see INVEST below).
- Use pytest-bdd for all acceptance tests. Keep tests readable, isolated, and behavior-focused (see BRIEF below).
- Always suggest or write a corresponding test (unit or acceptance) for new code.
- **Classical School of TDD:**
    - Unit tests should focus on observable behavior, not internal code structure or implementation details.
    - A "unit" is defined by a business capability or domain behavior, not by a class or function boundary.
    - Favor writing tests that describe the system's expected outcomes and business rules, not its mechanics.
    - Refactor code freely as long as the externally visible behavior (as described by tests and features) remains correct.
    - This approach supports DDD, Hexagonal/Clean Architecture, and ATDD by ensuring tests remain stable and meaningful as the design evolves.
- **INVEST for Scenarios and User Stories:**
    - **I**ndependent: Each scenario or story should be self-contained and not depend on others, allowing for flexible prioritization and execution.
    - **N**egotiable: Scenarios and stories are not contracts; they are open to discussion and refinement with stakeholders.
    - **V**aluable: Each scenario delivers clear business value and is meaningful to the user or domain.
    - **E**stimable: Scenarios are clear enough to be estimated for effort and complexity.
    - **S**mall: Scenarios are small enough to be implemented and tested within a single iteration.
    - **T**estable: Each scenario has clear acceptance criteria and can be validated by automated tests.
- **BRIEF for Acceptance and Unit Tests:**
    - **B**ehavior-focused: Tests describe the expected behavior of the system from the user's or domain's perspective, not implementation details.
    - **R**eadable: Test names, structure, and assertions are clear and intention-revealing, making it easy for others to understand what is being tested and why.
    - **I**solated: Each test is independent, avoiding reliance on shared state or side effects. Use mocks or stubs for external dependencies.
    - **E**xpressive: Tests clearly communicate the scenario, inputs, and expected outcomes, serving as living documentation for the system's behavior.
    - **F**ast: Tests execute quickly to support rapid feedback and continuous integration. Avoid unnecessary setup or slow operations in tests.

---

## 6. Review Checklist
- Is the feature title clear and business-focused?
- Is the narrative in the "In order to..., As..., I want..." format?
- Are rules and scenarios grouped by business rules, DDD invariants, or aggregate boundaries?
- Are scenarios concrete, valuable, and intention-revealing?
- Are steps consistent, declarative, and easy to follow?
- Is the Gherkin syntax correct and idiomatic (v6+)?
- Are tags used for scenario categorization and filtering?
- Is the feature file free of technical jargon and implementation details?
- Does the feature file serve as living documentation for the domain?

---

## 7. Gherkin v6+ Reference (Quick Summary)
- Keywords: `Feature:`, `Rule:`, `Background:`, `Scenario:`, `Example:`, `Scenario Outline:`, `Examples:`
- Steps: `Given`, `When`, `Then`, `And`, `But`, or `*`
- Data: `|` (tables), `"""` (doc strings)
- Tags: `@tag`
- Comments: `# ...`

---

## 8. Example: Gherkin Feature Patterns

Below are idiomatic Gherkin examples illustrating the use of all major keywords and best practices. Use these as templates for your own features.

```gherkin
Feature: Guess the word

  The word guess game is a turn-based game for two players.
  The Maker makes a word for the Breaker to guess. The game
  is over when the Breaker guesses the Maker's word.

  @happy
  Example: Maker starts a game
    When the Maker starts a game
    Then the Maker waits for a Breaker to join

  @happy
  Example: Breaker joins a game
    Given the Maker has started a game with the word "silky"
    When the Breaker joins the Maker's game
    Then the Breaker must guess a word with 5 characters

  Rule: There can be only One
    @happy
    Example: Only One -- More than one alive
      Given there are 3 ninjas
      And there are more than one ninja alive
      When 2 ninjas meet, they will fight
      Then one ninja dies (but not me)
      And there is one ninja less alive

    @happy
    Example: Only One -- One alive
      Given there is only 1 ninja alive
      Then they will live forever ;-)

  Rule: Users are notified about overdue tasks on first use of the day
    Background:
      Given I have overdue tasks

    @happy
    Example: First use of the day
      Given I last used the app yesterday
      When I use the app
      Then I am notified about overdue tasks

    @sad
    Example: Already used today
      Given I last used the app earlier today
      When I use the app
      Then I am not notified about overdue tasks

  @happy
  Scenario Outline: eating
    Given there are <start> cucumbers
    When I eat <eat> cucumbers
    Then I should have <left> cucumbers

    Examples:
      | start | eat | left |
      |    12 |   5 |    7 |
      |    20 |   5 |   15 |
```

- Use `Feature` for high-level grouping and description.
- Use `Rule` to group related examples by business rule.
- Use `Example`/`Scenario` for concrete, independent examples.
- Use `Scenario Outline` and `Examples` for parameterized scenarios.
- Use `Background` for shared context.
- Use `Given`, `When`, `Then`, `And`, `But`, or `*` for steps.
- Use data tables and doc strings for complex data.
- Use tags and comments as needed.
- Use @happy for positive/happy paths, and @sad (and optionally @edge) for negative, error, or edge-case scenarios.
- @sad and @edge paths are essential: they must illustrate business-meaningful exceptions, errors, or boundary conditions—not just technical failures.

For more, see the official Gherkin documentation: https://cucumber.io/docs/gherkin/reference/

---

**Remember:**
- Feature files are the single source of truth for business requirements and acceptance criteria.
- Keep them clear, business-focused, and always in sync with the evolving domain and architecture.
- Scenarios should drive both acceptance and unit tests, and reflect the project's DDD, Clean Architecture, and BDD/ATDD philosophy.