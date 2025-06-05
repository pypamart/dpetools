# How to Prompt GitHub Copilot for High-Quality Gherkin Feature Files

## Purpose
This guide helps you, as a product owner, business analyst, or developer, to get the best possible Gherkin v6+ feature files from GitHub Copilot (or any advanced AI). It ensures the AI produces business-relevant, maintainable, and testable features, and that it asks clarifying questions when requirements are ambiguous or incomplete.

---

## Recommended Prompt Template

> **Prompt:**
>
> I want you to generate a high-quality Gherkin v6+ feature file for a new business capability. Please:
>
> 1. **Follow BDD and DDD best practices:** Use business language, clear acceptance criteria, and structure the file with `Feature`, `Background`, `Rule`, and `Example` blocks (not just `Scenario`). Use tags for scenario categorization.
> 2. **Reflect Example Mapping:** If you need more information about business rules, examples, or open questions, ask me for clarification before proceeding.
> 3. **Document context:** Add a concise business description and, if possible, reference or link to evergreen business documentation or glossary.
> 4. **Be explicit:** If any part of the business process, rule, or example is unclear, ask me targeted questions to clarify intent, edge cases, or expected outcomes.
> 5. **Quality check:** Ensure the feature file is readable by non-technical stakeholders, steps are intention-revealing and reusable, and all business rules and examples are covered.
>
> Here is the business capability or user story I want to cover:
>
> [Paste your business capability, user story, or Example Mapping here]
>
> Please ask any questions you need to clarify the requirements before generating the Gherkin file.

---

## Why This Works
- **Encourages clarification:** The AI is explicitly invited to ask questions, reducing the risk of misinterpretation or missing requirements.
- **Promotes best practices:** The prompt enforces BDD/DDD structure, business language, and traceability to business knowledge.
- **Ensures living documentation:** The resulting feature file is suitable for both technical and non-technical stakeholders, and can evolve with the business.

---

## Example Usage

> I want you to generate a high-quality Gherkin v6+ feature file for the following capability:
>
> "In order to verify the energy performance of a property, as a real estate agent, I want to retrieve the DPE record by its unique reference."
>
> Please ask me any questions you need to clarify the business rules, edge cases, or expected outcomes before generating the feature file.

---

## Tips for Effective Collaboration
- **Be ready to answer questions:** The more context and clarification you provide, the better the feature file will be.
- **Share Example Mapping artifacts:** If you have example mapping cards or workshop notes, include them in your prompt.
- **Link to business documentation:** Reference evergreen documentation, glossaries, or business rules to ensure traceability.
- **Review and iterate:** Use the AI’s questions and drafts as a basis for discussion and refinement with your team.

---

> This approach ensures that your Gherkin features are business-aligned, testable, and ready for living documentation, while leveraging the full potential of AI assistance.
