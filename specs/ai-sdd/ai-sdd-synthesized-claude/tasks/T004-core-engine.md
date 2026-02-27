# T004: Core Engine — Orchestrator, State Manager, and Context Assembler

**Phase:** 1 (Core Engine)
**Status:** PENDING
**Dependencies:** T001 (agent system), T002 (workflow system), T003 (constitution system)

---

## Context

The core engine ties together the agent system, workflow DAG, and constitution system. It is responsible for:

1. Loading the workflow and resolving the execution plan.
2. Persisting task state to disk (so workflows can be resumed after interruption).
3. Dispatching each ready task to its configured agent via a `RuntimeAdapter`.
4. Assembling agent context (constitution + handover state + task inputs).
5. Exposing hooks for overlays and integrations (pre-task, post-task, on-failure, on-loop-exit).

The engine must be runtime-agnostic — it dispatches tasks through an adapter interface, never directly to a specific AI tool.

No business logic (review rules, confidence thresholds, pair programming) lives in the engine. These are overlays that register via hooks.

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
    Then the engine dispatches B and C concurrently (asyncio)

  Scenario: Pre-task hook
    Given a pre-task hook registered for task "design-l1"
    When task "design-l1" is about to execute
    Then the pre-task hook is called before agent dispatch

  Scenario: Post-task hook
    Given a post-task hook registered for task "design-l1"
    When task "design-l1" completes
    Then the post-task hook is called with the task result

  Scenario: On-failure hook
    Given an on-failure hook registered
    When any task fails
    Then the on-failure hook is called with the task and error details

  Scenario: Context assembly
    Given task "design-l1" with inputs ["requirements.md"]
    And an active constitution with rules
    And handover state from task "define-requirements"
    When the engine assembles context for "design-l1"
    Then the assembled context includes: constitution content, requirements.md content, and handover state

  Scenario: Runtime adapter decoupling
    Given the engine is initialized with a MockRuntimeAdapter
    When any task is dispatched
    Then the mock adapter records the call
    And no real LLM calls are made
```

---

## Inputs

- `WorkflowGraph` (from T002)
- `AgentRegistry` (from T001)
- `ConstitutionResolver` (from T003)
- Persisted state file (if resuming)

## Outputs

- Task execution results and outputs written to `.ai-sdd/state/`
- Updated state file after each task completes or fails

---

## State File Schema

```json
{
  "version": "1",
  "workflow": "default-sdd",
  "project": "/path/to/project",
  "started_at": "2026-02-27T10:00:00Z",
  "tasks": {
    "define-requirements": {
      "status": "COMPLETED",
      "started_at": "2026-02-27T10:01:00Z",
      "completed_at": "2026-02-27T10:05:00Z",
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

## RuntimeAdapter Interface

```python
class RuntimeAdapter(ABC):
    @abstractmethod
    def dispatch(self, task: Task, context: AgentContext) -> TaskResult:
        """
        Dispatch a task to the underlying AI runtime.
        Returns TaskResult with: status, outputs, handover_state, error.
        """
        ...
```

Context bundle passed to each agent:
```python
AgentContext(
    constitution=<merged constitution string>,
    handover_state=<dict from previous tasks>,
    task_inputs=<list of input file contents>,
    task_definition=<task YAML definition>
)
```

---

## Hook Points

```python
engine.on_pre_task(task_id, callback)
engine.on_post_task(task_id, callback)       # or "*" for all tasks
engine.on_failure(task_id, callback)
engine.on_loop_exit(task_id, callback)
```

Overlays register themselves via these hooks — the engine does not know about specific overlay logic.

---

## Implementation Notes

- Use `asyncio` for parallel task execution of independent task groups.
- State file stored at `.ai-sdd/state/workflow-state.json`.
- Atomic state writes: write to a temp file, then rename to prevent corruption.
- Hook dispatch: run all registered hooks for an event in registration order.
- Handover state: each completed task can write a `handover` dict to state; next tasks receive it.
- On unrecoverable failure: persist state, emit on-failure event, stop gracefully.

---

## Files to Create

- `core/engine.py`
- `core/state_manager.py`
- `core/context_manager.py`
- `core/hooks.py`
- `core/runtime_adapter.py` (interface)
- `adapters/mock_adapter.py`
- `adapters/claude_code_adapter.py`
- `tests/test_engine.py`
- `tests/test_state_manager.py`

---

## Test Strategy

- Unit tests: state transitions (PENDING → RUNNING → COMPLETED/FAILED).
- Unit tests: dependency resolution, topological dispatch order.
- Unit tests: context assembly (constitution + handover + inputs).
- Integration tests: full workflow run (A → B → C); interruption + resume; parallel dispatch.
- Integration test: failed task halts downstream; on-failure hook fires.

## Rollback/Fallback

- On unrecoverable task failure: persist FAILED state; stop engine safely.
- On adapter dispatch error: retry up to configurable limit, then mark FAILED.
- State file write failure: emit critical error; do not proceed to next task.
