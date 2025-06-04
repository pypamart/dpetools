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

## Checklist: Creating a New Action

When adding a new Action to this project, follow this checklist to ensure compliance with architecture and best practices:

1. **Location & Naming**
   - Place the new Action class in `src/{package_name}/application/actions/plugins/`.
   - The class must inherit from `IAction` (or a relevant abstract base Action class).
   - Choose a unique and intention-revealing identifier string (e.g., `ACTION_IDENTIFIER`) for the Action. This identifier will be used for autodiscovery and instantiation by the ActionFactory.

2. **Autodiscovery**
   - Ensure the Action is discoverable by the plugin manager/factory (the identifier must be unique and registered if required).

3. **Abstract Methods**
   - Implement all required abstract methods from `IAction` (e.g., `get_action_identifier`, `get_parameter_specs`, `apply_on`, etc.).
   - Add your business logic in the appropriate method bodies. You may use comments referencing similar or existing Actions for clarity.

4. **Dependency Injection**
   - All infrastructure dependencies (e.g., readers, repositories, external services) must be injected via the constructor or a dedicated injection method.
   - Do **not** instantiate infrastructure classes directly inside the Action.
   - Use interfaces/abstract base classes for all injected dependencies.

5. **DTO Communication**
   - All communication with the infrastructure layer must be done via Data Transfer Objects (DTOs). Do not pass raw models or domain objects across the boundary.
   - Use or create DTOs in `src/{package_name}/application/dto/` as needed.

6. **Testing**
   - Write or update unit tests for the new Action in `tests/unit/application/actions/`.
   - If the Action is part of a business workflow, add or update acceptance tests in `tests/acceptance/` and feature files in `docs/features/`.
   - Use mocks/stubs for infrastructure dependencies in unit tests.

7. **Documentation**
   - Add docstrings to all public classes and methods.
   - Document the Action's identifier, expected parameters, and injected dependencies.

8. **Formatting & Style**
   - Use type hints for all function signatures.
   - Use snake_case for functions and variables, PascalCase for classes.
   - Keep lines under 180 characters.

