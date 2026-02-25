# Task 03: Constitutions Engine

## Description
Develop the logic to implement "Constitutions" across the repository. The constitution mechanism governs how an agent behaves when operating within specific folders, allowing projects to define unique steers, purposes, background rules, and standards.

## Requirements
- **Recursive Parsing:** The engine must traverse the directory structure from the root down to the target folder, parsing constitution files (e.g., `.ai-constitution.yaml` or `.ai-steer.yaml`).
- **Merging & Overriding:** Rules defined in subdirectories must extend, merge, or override rules defined higher up in the directory tree.
- **Prompt Injection:** The aggregated constitution for a given context must be formatted and injected into the agent's system prompt prior to task execution.

## Acceptance Criteria
- [ ] The engine correctly traverses and parses constitution files from a target directory up to the project root.
- [ ] Conflicting rules are correctly overridden by the most specific (deepest) constitution file.
- [ ] The final aggregated steer is successfully injected into the active agent's system prompt.