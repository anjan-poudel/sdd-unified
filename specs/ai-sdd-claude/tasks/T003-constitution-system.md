# T003: Constitution System — Recursive Context Resolution

**Phase:** 1 (Core Engine)
**Status:** PENDING
**Dependencies:** none

---

## Context

A "constitution" is a set of steering files that defines project context: purpose, background, rules, and standards. Constitutions are hierarchical — a sub-module's constitution overrides its parent's, which overrides the root.

At task execution time, the engine merges all applicable constitutions into the system prompt context injected into the agent.

This replaces the manual, monolithic system prompt approach in sdd-unified.

---

## Acceptance Criteria

```gherkin
Feature: Constitution resolver

  Scenario: Root-only constitution
    Given a project with only a root constitution.md
    When a task runs for a file in the project root
    Then the agent context includes the root constitution content

  Scenario: Sub-module overrides root
    Given a root constitution.md defining rule "use snake_case"
    And a sub-module constitution.md overriding it with "use camelCase"
    When a task runs for a file inside the sub-module
    Then the merged constitution shows "use camelCase" (sub-module wins)

  Scenario: Constitution inheritance — additive fields
    Given root constitution defines "Background: payment domain"
    And sub-module constitution does not define Background
    When the constitution is resolved for a task in the sub-module
    Then the resolved constitution includes "Background: payment domain" from root

  Scenario: Missing constitution
    Given a project with no constitution.md at any level
    When the constitution resolver runs
    Then it returns an empty/default constitution without error

  Scenario: Constitution injected into agent context
    Given a resolved constitution with rules and standards
    When the engine assembles the context for a task
    Then the constitution content is prepended to the agent's system prompt
```

---

## Inputs

- Path to task's working directory
- Root project path (to find root constitution)

## Outputs

- `ResolvedConstitution`: merged content string ready for injection into system prompt

---

## Implementation Notes

- Constitution files are named `constitution.md` (configurable) and placed in `.ai-sdd/` within each directory level.
- Resolution walk: start at task's directory, walk up to project root, collect all `constitution.md` files.
- Merge strategy:
  - Named sections (Purpose, Background, Rules, Standards) are merged separately.
  - Child sections override parent sections of the same name.
  - Unnamed content is appended.
- The resolver should be purely functional (no side effects) for testability.

---

## Files to Create

- `constitution/resolver.py`
- `constitution/schema.md` (template/example constitution)
- `tests/test_constitution_resolver.py`
