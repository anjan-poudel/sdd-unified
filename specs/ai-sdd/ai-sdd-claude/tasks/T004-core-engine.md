# T004: Core Engine — Orchestrator, State Manager, and Context Assembler

**Phase:** 1 (Core Engine)
**Status:** PENDING
**Dependencies:** T001 (agent system), T002 (workflow system), T003 (constitution system)

---

## Context

The core engine ties together the agent system, workflow DAG, and constitution system. It is responsible for:

1. Loading the workflow and resolving the execution plan.
2. Persisting task state to disk (so workflows can be resumed).
3. Dispatching each ready task to its configured agent.
4. Assembling agent context (constitution + handover state + task inputs).
5. Exposing hooks for overlays and integrations (pre-task, post-task, on-failure).

The engine must be runtime-agnostic — it dispatches tasks through an adapter interface, not directly to a specific tool (Claude Code, Codex, etc.).

---

## Acceptance Criteria

```gherkin
Feature: Core engine execution

  Scenario: Full pipeline execution
    Given a valid workflow with tasks A → B → C
    When `engine.run()` is called
    Then tasks execute in dependency order
    And each task receives its inputs and produces its outputs
    And all tasks reach COMPLETED status

  Scenario: State persistence between runs
    Given a workflow where task A is COMPLETED and task B is PENDING
    When the engine is started fresh (simulating a crash/restart)
    Then the engine loads state from disk
    And skips task A (already COMPLETED)
    And continues from task B

  Scenario: Failed task halts downstream
    Given task A fails during execution
    When the engine detects the failure
    Then task A's status is set to FAILED
    And all tasks that depend on A are NOT executed
    And the engine emits an on-failure event

  Scenario: Parallel task execution
    Given tasks B and C both depend on A but not on each other
    When task A completes
    Then the engine dispatches B and C concurrently

  Scenario: Pre-task hook
    Given a pre-task hook registered for task "design-l1"
    When task "design-l1" is about to execute
    Then the pre-task hook is called before agent dispatch

  Scenario: Context assembly
    Given task "design-l1" with inputs ["requirements.md"]
    And an active constitution with rules
    And handover state from task "define-requirements"
    When the engine assembles context for "design-l1"
    Then the assembled context includes: constitution content, requirements.md content, and handover state
```

---

## Inputs

- `WorkflowGraph` (from T002)
- `AgentRegistry` (from T001)
- `ConstitutionResolver` (from T003)
- Persisted state file (if resuming)

## Outputs

- Task execution results and outputs written to the project's `.ai-sdd/state/` directory
- Updated state file after each task completes

---

## State File Schema

```json
{
  "workflow": "default-sdd",
  "project": "/path/to/project",
  "started_at": "2026-02-23T10:00:00Z",
  "tasks": {
    "define-requirements": {
      "status": "COMPLETED",
      "started_at": "...",
      "completed_at": "...",
      "outputs": ["requirements.md"],
      "iterations": 1
    },
    "design-l1": {
      "status": "PENDING",
      "started_at": null,
      "completed_at": null,
      "outputs": [],
      "iterations": 0
    }
  }
}
```

---

## Implementation Notes

- Engine dispatch: `RuntimeAdapter` interface with implementations per runtime (Claude Code, Codex, mock for tests).
- State file stored at `.ai-sdd/state/workflow-state.json` in project root.
- Use `asyncio` for parallel task execution.
- Hook points: `pre_task(task)`, `post_task(task, result)`, `on_failure(task, error)`, `on_loop_exit(task, reason)`.
- Overlays register themselves via hooks — the engine does not know about specific overlay logic.
- Context bundle passed to each agent: `{ constitution, handover_state, task_inputs, task_definition }`.

---

## Files to Create

- `core/engine.py`
- `core/state_manager.py`
- `core/context_manager.py`
- `core/hooks.py`
- `core/runtime_adapter.py` (interface + mock implementation)
- `tests/test_engine.py`
- `tests/test_state_manager.py`
