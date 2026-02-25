# T001: Agent System — YAML Schema, Loader, and Default Agents

**Phase:** 1 (Core Engine)
**Status:** PENDING
**Dependencies:** none

---

## Context

The agent system replaces hardcoded role definitions (sdd-ba, sdd-pe, etc.) with externalized YAML files. Any client can swap out a default agent or introduce a new one without touching framework code.

A custom agent can `extend` a base agent and override specific fields (overlay inheritance model).

---

## Acceptance Criteria

```gherkin
Feature: Agent YAML loader

  Scenario: Load a default agent
    Given a valid agent YAML file at agents/defaults/ba.yaml
    When the agent loader initializes
    Then the BA agent is available with its role, LLM config, and commands

  Scenario: Custom agent extends a default agent
    Given a custom agent YAML with `extends: ba`
    And the custom agent overrides `llm.model` to a different value
    When the agent loader resolves the custom agent
    Then the custom agent inherits all fields from ba.yaml
    And the overridden `llm.model` takes precedence

  Scenario: Invalid agent YAML fails fast
    Given an agent YAML file missing the required `role.description` field
    When the agent loader initializes
    Then a schema validation error is raised with a clear message

  Scenario: Agent LLM config is per-agent
    Given agent ba.yaml uses model claude-sonnet-4-6
    And agent architect.yaml uses model claude-opus-4-6
    When both agents are loaded
    Then each agent dispatches to its own configured model
```

---

## Inputs

- Agent YAML files (project or defaults directory)
- Agent base schema (`agents/base_agent.yaml`)

## Outputs

- `AgentRegistry`: in-memory registry of loaded agents
- Resolved agent definitions (with inherited fields applied)

---

## Implementation Notes

- Use Python `dataclasses` or `pydantic` for agent models.
- Inheritance resolution: walk the `extends` chain, apply field-level overrides (deep merge).
- Schema validation on load using `jsonschema` or `pydantic` validators.
- Default agents to implement: `ba`, `architect`, `pe`, `le`, `dev`, `reviewer`.
- Each default agent YAML must include: `name`, `display_name`, `version`, `llm`, `role`, `commands`.

---

## Files to Create

- `core/agent_loader.py`
- `agents/base_agent.yaml`
- `agents/schema.yaml`
- `agents/defaults/ba.yaml`
- `agents/defaults/architect.yaml`
- `agents/defaults/pe.yaml`
- `agents/defaults/le.yaml`
- `agents/defaults/dev.yaml`
- `agents/defaults/reviewer.yaml`
- `tests/test_agent_loader.py`
