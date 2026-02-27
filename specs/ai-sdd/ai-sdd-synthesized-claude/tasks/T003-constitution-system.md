# T003: Constitution System — Recursive Context Resolution

**Phase:** 1 (Core Engine)
**Status:** PENDING
**Dependencies:** none

---

## Context

A "constitution" is a set of steering files (purpose, background, rules, standards) that define the operational context for a project or sub-module. Constitutions are hierarchical: a sub-module's constitution overrides its parent, which overrides the project root, which overrides the framework defaults.

At task execution time, the engine merges the active constitution chain into the agent's system prompt, ensuring agents operate within the correct context without requiring monolithic system prompts.

---

## Acceptance Criteria

```gherkin
Feature: Constitution resolver

  Scenario: Project root constitution is loaded
    Given a project with .ai-sdd/constitution.md at the root
    When a task runs from the project root
    Then the root constitution is included in the agent context

  Scenario: Sub-module constitution overrides root
    Given a project root constitution with rule "use Python 3.11"
    And a sub-module constitution with rule "use Python 3.12"
    When a task runs from within the sub-module
    Then the merged constitution contains "use Python 3.12" (sub-module wins)
    And other root rules not overridden by the sub-module are preserved

  Scenario: Framework defaults are base layer
    Given a project with no constitution files at all
    When a task runs
    Then the framework default context is used
    And no error is raised

  Scenario: Constitution file not found
    Given a project path with no constitution files anywhere
    When the resolver runs
    Then it returns only the framework defaults
    And does not raise an error

  Scenario: Deep nesting
    Given constitutions at: framework → project root → src/ → src/auth/
    When a task runs inside src/auth/
    Then all four layers are merged in order (framework < root < src < src/auth)
```

---

## Constitution File Format

```markdown
# constitution.md

## Purpose
[Why this project/module exists and what it's trying to achieve]

## Background
[Domain context, key constraints, technology choices and rationale]

## Rules
- [Hard rule 1 — these must be followed]
- [Hard rule 2]

## Standards
- Code style: [...]
- Testing: [...]
- Naming: [...]
- Documentation: [...]
```

---

## Resolution Algorithm

Resolution order (lowest priority first — highest wins):
1. Framework default context (`config/defaults.yaml` context section)
2. Project root `constitution.md` (found at `<project-root>/.ai-sdd/constitution.md`)
3. Each intermediate directory's `constitution.md` walking upward from task root
4. Task-specific directory `constitution.md` (closest to the task)

Merge strategy:
- **Purpose / Background**: child overrides parent completely (replace).
- **Rules / Standards**: append child rules; if child re-states a rule, child version takes precedence.

---

## Inputs

- Project root path
- Task execution path (to determine which sub-module constitutions apply)

## Outputs

- Merged constitution string (injected as system prompt context)
- Resolution trace (list of files merged in order, for debug/observability)

---

## Implementation Notes

- Walk directory tree upward from task path to project root, collecting `constitution.md` files.
- Apply merge in bottom-up order (framework → root → closest sub-module).
- Cache resolved constitutions per path to avoid re-reading on repeated task dispatches.
- Constitution resolution trace is emitted as an observability event.

---

## Files to Create

- `constitution/resolver.py`
- `constitution/schema.yaml`
- `config/defaults.yaml` (includes framework-level default context section)
- `tests/test_constitution_resolver.py`

---

## Test Strategy

- Unit tests: single constitution load, two-level override, deep nesting.
- Unit tests: missing constitution at all levels (graceful fallback).
- Unit tests: merge strategy for Rules/Standards sections.
- Integration test: constitution is correctly injected into agent context bundle.

## Rollback/Fallback

- If a constitution file is malformed (not valid markdown with expected sections), log a warning and skip that level — do not fail the workflow.
