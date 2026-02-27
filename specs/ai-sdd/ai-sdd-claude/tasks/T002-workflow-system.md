# T002: Workflow System — YAML Schema, DAG Loader, and Default Template

**Phase:** 1 (Core Engine)
**Status:** PENDING
**Dependencies:** T001 (agent system must be loadable to validate agent references in workflow)

---

## Context

Workflows are fully described in YAML. The engine parses the YAML, builds an internal DAG, validates it (no cycles, all referenced agents exist), and makes it available for execution.

The default SDD workflow template should reproduce the sdd-unified pipeline so existing users can migrate without changing their development process.

---

## Acceptance Criteria

```gherkin
Feature: Workflow YAML loader

  Scenario: Load a valid workflow
    Given a valid workflow YAML file
    When the workflow loader initializes
    Then all tasks are loaded with their agent, inputs, outputs, and dependencies
    And the DAG is built correctly

  Scenario: Dependency resolution
    Given workflow with task B depending on A, and task C depending on B
    When the engine resolves execution order
    Then task A is scheduled first, then B, then C

  Scenario: Parallel independent tasks
    Given workflow with tasks B and C both depending on A but not on each other
    When task A completes
    Then tasks B and C are both scheduled for parallel execution

  Scenario: Cyclic dependency detection
    Given a workflow YAML where task A depends on B and B depends on A
    When the workflow loader initializes
    Then a validation error is raised: "cyclic dependency detected"

  Scenario: Unknown agent reference
    Given a workflow YAML referencing agent "foobar" which does not exist in the registry
    When the workflow loader initializes
    Then a validation error is raised: "agent 'foobar' not found"

  Scenario: Loop task configuration
    Given a workflow task with `loop.max_iterations: 3` and one exit condition
    When the task loop runs
    Then it will execute at most 3 times
    And it exits early when the exit condition is satisfied
```

---

## Inputs

- Workflow YAML file(s)
- `AgentRegistry` (from T001)

## Outputs

- `WorkflowGraph`: validated DAG of tasks
- Topological execution plan (ordered task list respecting dependencies)

---

## Implementation Notes

- Use `networkx` for DAG representation and topological sort, or implement a simple Kahn's algorithm.
- Validate the DAG is acyclic before returning.
- Loop blocks in YAML: `loop.max_iterations` (required), `loop.exit_conditions` (list of expressions, at least one required).
- `exit_conditions` are string expressions evaluated against task context at runtime (e.g., `"review.decision == GO"`).
- Default workflow template should cover: define-requirements → design-l1 → review-l1 → design-l2 → review-l2 → design-l3 → execute-tasks.

---

## Files to Create

- `core/workflow_loader.py`
- `workflows/schema.yaml`
- `workflows/default-sdd.yaml`
- `tests/test_workflow_loader.py`
