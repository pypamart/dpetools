# GitHub Copilot Instructions

## General Principles
- Always follow Domain-Driven Design (DDD) principles: keep domain logic in the domain layer, and avoid leaking infrastructure or application details into the domain.
- Use Hexagonal (Ports & Adapters) and Clean Architecture: separate domain, application, infrastructure, and interface layers. Dependencies should point inward.
- Use Test-Driven Development (TDD) and Acceptance Test-Driven Development (ATDD): always write or suggest tests before implementation.
- Use Behavior-Driven Development (BDD) for acceptance criteria and feature files. Step definitions should be clear and map directly to feature scenarios.

## Code Organization
- Place domain models, value objects, and aggregates in `src/{package_name}/domain/models/`.
- Place repositories, services, and interfaces in their respective domain or application subfolders.
- Application services, use cases, and action orchestration go in `src/{package_name}/application/`.
- Infrastructure code (adapters, persistence, readers, etc.) goes in `src/{package_name}/infrastructure/`.
- Interface adapters (controllers, events, etc.) go in `src/{package_name}/interfaces/`.
- Tests are organized in `tests/acceptance/` for BDD/ATDD and `tests/unit/` for unit tests.

## Best Practices
- Always inject dependencies (e.g., readers, repositories) via constructor or method parameters, never hardcode them.
- Use interfaces/abstract base classes for all dependencies crossing architectural boundaries.
- Write clear, isolated unit tests for domain logic. Use mocks/stubs for infrastructure in unit tests.
- Acceptance tests should use real feature files and step definitions that reflect business language.
- Use descriptive, intention-revealing names for classes, methods, and variables.
- Avoid logic in controllers, readers, or infrastructure classes—keep it in the domain or application layer.
- Prefer immutability and pure functions in the domain layer.
- Use custom exceptions for domain and application errors.
- Document public APIs and important classes with docstrings.

## Copilot Suggestions
- When generating new code, always suggest a corresponding test (unit or acceptance) in the correct folder.
- When generating infrastructure or adapter code, ensure it depends only on interfaces defined in the application or domain layer.
- When generating step definitions for BDD, use the language and structure from the `.feature` files in `docs/features/`.
- When generating new domain logic, ensure it is free of infrastructure or framework dependencies.
- When generating repository or service interfaces, place them in the appropriate `interfaces/` or `domain/services/` folder.
- When generating code for dependency injection, use constructor injection and avoid service locators or global state.

## Formatting and Style
- Use type hints for all function signatures.
- Use snake_case for functions and variables, PascalCase for classes.
- Use docstrings for all public classes and methods.
- Keep lines under 120 characters.
- Use pytest for all tests.

## What to Avoid
- Do not place business logic in infrastructure or interface layers.
- Do not use static or global state for dependencies.
- Do not tightly couple application code to frameworks or libraries.
- Do not generate code that mixes concerns from different architectural layers.
- Do not generate code without a corresponding test or usage example.

## Domain-Driven Design (DDD) Strategic Patterns
- DDD strategic patterns help align software architecture with business strategy and organizational boundaries.
- **Bounded Contexts**: Explicit boundaries within which a particular domain model applies. Each bounded context has its own ubiquitous language and model, and integration between contexts is managed through well-defined interfaces or contracts.
- **Context Mapping**: Techniques for describing and managing relationships between bounded contexts, such as Shared Kernel, Customer/Supplier, Conformist, Anticorruption Layer, and Open Host Service. These patterns help teams coordinate and integrate across different models and systems.
- **Ubiquitous Language**: A shared language developed by the team and stakeholders within a bounded context, used consistently in code, documentation, and conversation to reduce ambiguity and improve communication.
- **Core Domain**: The most critical part of the business where competitive advantage is created. Focus development effort here, and keep the core domain isolated from generic or supporting subdomains.
- **Supporting and Generic Subdomains**: Supporting subdomains assist the core domain but are not unique, while generic subdomains are common to many businesses and can often be bought or reused.
- **Partnerships and Team Organization**: Strategic DDD encourages aligning team structure and communication with bounded contexts, supporting Conway's Law and enabling autonomous, focused teams.
- Applying DDD strategic patterns ensures that software architecture, team structure, and business strategy remain aligned, supporting scalability, maintainability, and business agility.

## INVEST for User Stories
- Write user stories and features that follow the INVEST criteria: **Independent**, **Negotiable**, **Valuable**, **Estimable**, **Small**, and **Testable**.
- Each story should be self-contained and not depend on others, allowing for flexible prioritization and development.
- Requirements should be open to discussion and refinement, focusing on delivering clear business value.
- Stories must be small enough to be completed within a single iteration and clearly testable through acceptance criteria and automated tests.
- Applying INVEST ensures that your backlog remains actionable, maintainable, and aligned with business goals.

## Behavior-Driven Development (BDD) and Living Documentation
- BDD is a collaborative approach that connects software development with business goals, supporting DDD's strategic design by making domain language explicit.
- Example Mapping is recommended as a workshop technique to capture business rules, examples, and questions, which are then translated into Gherkin scenarios.
- Gherkin feature files serve as living documentation, ensuring that business requirements, domain knowledge, and system behavior remain aligned and accessible to all stakeholders.
- Living documentation is continuously updated and validated by automated acceptance tests, providing a single source of truth for both technical and non-technical team members. This fosters shared understanding, reduces ambiguity, and enables rapid adaptation to changing business needs.
- This process helps teams clarify requirements, reduce ambiguity, and maintain a shared understanding of the domain as it evolves.

## Gherkin Best Practices
- Use Gherkin v6+ syntax, leveraging `Rule` and `Example` blocks to organize scenarios by business rules and to clarify intent.
- Write scenarios in business language, focusing on user value and clear acceptance criteria.
- Use tags (e.g., `@happy`, `@sad`, `@wip`) to categorize scenarios for targeted test runs and reporting.
- Prefer declarative steps over imperative ones; describe what, not how.
- Keep steps reusable and intention-revealing; avoid technical jargon in favor of domain language.
- Use Background sections for shared context, and keep scenarios independent when possible.
- Maintain feature files as living documentation: keep them up to date, reviewed, and accessible to both technical and non-technical stakeholders.
- Ensure each scenario is atomic, testable, and maps directly to a business requirement or rule.
- Regularly review and refactor feature files to improve clarity, remove duplication, and ensure alignment with evolving business needs.

## Acceptance Test-Driven Development (ATDD) Outer Loop
- Begin each new feature or change by writing or updating Gherkin feature files in `docs/features/` to capture business requirements and acceptance criteria.
- Implement acceptance tests in `tests/acceptance/` using pytest-bdd, ensuring each scenario in the feature file is mapped to a step definition (test glue).
- Step definitions should use business language and intention-revealing names, directly reflecting the Gherkin steps.
- The ATDD process ensures that development is guided by business value and that features are only considered complete when all acceptance criteria pass.
- This ATDD outer loop drives the TDD inner loop, providing high-level, end-to-end validation and living documentation for the project.

## Test-Driven Development (TDD) Inner Loop
- After writing acceptance tests and feature files (BDD/ATDD), use TDD for all new or changed domain and application logic.
- Infrastructure code can also be developed using TDD, with unit tests for adapters and persistence logic.
- When interacting with external systems (e.g., APIs, databases), prefer integration tests to validate real-world behavior.
- For each new feature or change:
  1. Write or update unit tests in `tests/unit/` before implementing the logic.
  2. Use mocks/stubs for infrastructure dependencies in unit tests.
  3. Ensure unit tests are focused, isolated, and intention-revealing.
  4. Only implement the minimum code needed to make the unit test pass.
  5. Refactor code and tests for clarity and maintainability, keeping all tests green.
- This TDD inner loop ensures robust, well-designed domain, application, and infrastructure code, and complements the outer ATDD/BDD loop.

## BRIEF for Testing
- BRIEF is a mnemonic for writing effective and intention-revealing tests: **B**ehavior-focused, **R**eadable, **I**solated, **E**xpressive, and **F**ast.
- **Behavior-focused**: Tests should describe the expected behavior of the system from the user's or domain's perspective, not implementation details.
- **Readable**: Test names, structure, and assertions should be clear and intention-revealing, making it easy for others to understand what is being tested and why.
- **Isolated**: Each test should be independent, avoiding reliance on shared state or side effects. Use mocks or stubs for external dependencies.
- **Expressive**: Tests should clearly communicate the scenario, inputs, and expected outcomes, serving as living documentation for the system's behavior.
- **Fast**: Tests should execute quickly to support rapid feedback and continuous integration. Avoid unnecessary setup or slow operations in tests.
- Applying BRIEF ensures that your test suite remains maintainable, trustworthy, and valuable as the codebase evolves.

## Domain-Driven Design (DDD) Tactical Patterns and Model-Driven Design
- DDD tactical patterns help structure the domain layer for clarity, maintainability, and business alignment.
- **Value Objects** represent immutable concepts with no identity, defined only by their attributes (e.g., Money, Address).
- **Entities** have a unique identity and a lifecycle; their identity persists even if their attributes change (e.g., User, DpeRecord).
- **Aggregate Roots** are entities that act as entry points to aggregates, enforcing invariants and consistency boundaries (e.g., Order as root of OrderLines).
- **Aggregates** are clusters of entities and value objects bound together by an aggregate root, which enforces consistency rules within the boundary.
- **Domain Services** encapsulate domain logic that doesn't naturally fit within a single entity or value object.
- **Repositories** provide interfaces for retrieving and persisting aggregates, abstracting away infrastructure concerns.
- **Factories** are responsible for creating complex aggregates or entities, encapsulating the logic required to ensure invariants and valid construction.
- Model-Driven Design means the code structure and language reflect the business domain, supporting ubiquitous language and collaboration between technical and business stakeholders.
- Use these tactical patterns to keep the domain model expressive, intention-revealing, and free from infrastructure or application concerns.

## Hexagonal and Clean Architecture
- Hexagonal (Ports & Adapters) and Clean Architecture enforce a clear separation of concerns between domain, application, infrastructure, and interface layers.
- Dependencies always point inward: infrastructure and interface code depend on application and domain abstractions, never the reverse.
- The domain layer contains pure business logic, free from technical details or frameworks.
- The application layer orchestrates use cases and coordinates domain logic, relying only on domain abstractions and interfaces.
- Infrastructure (adapters, persistence, external APIs) implements interfaces defined in the application or domain layer, and is injected via constructor or method parameters.
- Interface adapters (controllers, events, etc.) handle input/output and user interaction, delegating all business logic to the application or domain layer.
- This architecture enables testability, maintainability, and adaptability to change, ensuring the core business logic remains isolated from external concerns.

## Clean Code Principles
- Write code that is easy to read, understand, and maintain for both current and future developers.
- Use intention-revealing names for variables, functions, and classes; avoid abbreviations and unclear terms.
- Keep functions and classes small and focused on a single responsibility.
- Remove duplication and favor DRY (Don't Repeat Yourself) principles.
- Write code that expresses intent clearly, so comments are only needed for non-obvious decisions or business rules.
- Refactor regularly to improve structure, readability, and maintainability without changing behavior.
- Prefer immutability and pure functions where possible, especially in the domain layer.
- Ensure code is covered by meaningful tests, and keep all tests passing (green) at all times.
- Strive for simplicity: make the code as simple as possible, but no simpler.

## Software Design Principles
- Follow the SOLID principles: Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, and Dependency Inversion to ensure code is modular, extensible, and robust.
- Apply YAGNI (You Aren't Gonna Need It): only implement what is required by current business needs, avoiding speculative features.
- Embrace KISS (Keep It Simple, Stupid): favor simple, straightforward solutions over complex or clever code.
- Use DRY (Don't Repeat Yourself): eliminate duplication by abstracting common logic and reusing code where appropriate.
- Prefer composition over inheritance to maximize flexibility and reduce tight coupling.
- Strive for high cohesion within modules and loose coupling between them.
- Regularly review and refactor code to maintain adherence to these principles as the codebase evolves.

## Checklist: Adding a New Feature

Follow this checklist to ensure new features are robust, maintainable, and aligned with best practices:

1. **Feature Definition & Living Documentation**
   - Write or update a Gherkin feature file in `docs/features/` using Gherkin v6+ syntax (`Feature`, `Rule`, `Example`).
   - Use business language and clear acceptance criteria. Organize scenarios with tags (e.g., `@happy`, `@sad`).
   - Ensure the feature file serves as living documentation, accessible to both technical and non-technical stakeholders.

2. **Acceptance Criteria & ATDD**
   - Create or update acceptance test files in `tests/acceptance/` to match the new feature scenarios.
   - Implement step definitions that map directly to the Gherkin steps, using intention-revealing names and business language.
   - Use pytest-bdd for all acceptance tests. Keep tests readable, isolated, and behavior-focused.

3. **Test-Driven Development (TDD) & Unit Testing**
   - Write or update unit tests for new or changed domain/application logic in `tests/unit/` before implementing the logic.
   - Use mocks/stubs for infrastructure dependencies in unit tests. Ensure tests are expressive, fast, and maintainable.

4. **Domain & Application Logic**
   - Place new domain models, value objects, and aggregates in `src/{package_name}/domain/models/`.
   - Add or update application services, use cases, or orchestration logic in `src/{package_name}/application/`.
   - Keep all business logic in the domain or application layer, not in infrastructure or interface code.

5. **Infrastructure & Interfaces**
   - Add or update infrastructure code (adapters, persistence, etc.) in `src/{package_name}/infrastructure/` as needed.
   - Place interface adapters (controllers, events, etc.) in `src/{package_name}/interfaces/`.
   - Inject all infrastructure dependencies via constructor or method parameters, using interfaces/abstract base classes.

6. **Continuous Integration, Linters, Type Checking & Code Quality**
   - Ensure all tests pass in the CI pipeline before merging changes.
   - Integrate static analysis, security checks, and code formatting tools into the pipeline.
   - Run linters (e.g., ruff linter, flake8, pylint), type checkers (e.g., mypy), and code formatters (e.g., ruff formatter, black, isort) before every commit or as a pre-commit hook.
   - Refactor code regularly to manage technical debt and improve maintainability.

7. **Documentation & Code Style**
   - Add or update docstrings for all public classes and methods.
   - Ensure the feature and its scenarios are clearly documented in the Gherkin file.
   - Use type hints for all function signatures, snake_case for functions/variables, PascalCase for classes, and keep lines under 120 characters.

By following this checklist, you ensure that new features are well-designed, testable, and maintainable, and that they fit cleanly into the project's architecture and documentation standards.

