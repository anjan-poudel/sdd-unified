# T004: Core Engine — Orchestrator, State Manager, and Context Assembler

**Phase:** 1 (Core Engine)
**Status:** PENDING
**Dependencies:** T001 (agent system), T002 (workflow system), T003 (constitution system)
**Changes from synthesized-claude:** RuntimeAdapter signature includes `idempotency_key`; post-task hook registers manifest writer; concurrency budget config added; context assembly note updated (pull model).

---

## Context

The core engine ties together the agent system, workflow DAG, and constitution system. It is responsible for:

1. Loading the workflow and resolving the execution plan.
2. Persisting task state to disk (so workflows can be resumed after interruption).
3. Dispatching each ready task to its configured agent via a `RuntimeAdapter`.
4. Assembling agent context (merged constitution including artifact manifest + handover state).
5. Exposing hooks for overlays and integrations (pre-task, post-task, on-failure, on-loop-exit).

The engine is runtime-agnostic — it dispatches through an adapter interface. No business logic lives in the engine. Context management uses the **pull model**: the constitution manifest tells agents what exists; agents fetch what they need via their native tools.

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

  Scenario: Parallel task execution within concurrency budget
    Given tasks B and C both depend on A but not on each other
    And engine.max_concurrent_tasks=3
    When task A completes
    Then the engine dispatches B and C concurrently (asyncio semaphore)
    And no more than max_concurrent_tasks tasks run simultaneously

  Scenario: Post-task hook fires manifest writer
    Given a post-task hook registered by the manifest writer
    When any task completes
    Then the manifest writer updates the constitution.md artifact manifest
    Before the next task is dispatched

  Scenario: Context assembly uses artifact manifest
    Given task "design-l1" with constitution containing the artifact manifest
    When the engine assembles context for "design-l1"
    Then the assembled context includes: merged constitution (with manifest), handover state
    And does NOT pre-load all prior task output file contents

  Scenario: Runtime adapter decoupling
    Given the engine is initialized with a MockRuntimeAdapter
    When any task is dispatched
    Then the mock adapter records the call with idempotency_key
    And no real LLM calls are made
```

---

## Inputs

- `WorkflowGraph` (from T002)
- `AgentRegistry` (from T001)
- `ConstitutionResolver` (from T003)
- Persisted state file (if resuming)

## Outputs

- Task execution results written to `.ai-sdd/state/`
- Updated state file after each task completes or fails
- Updated constitution.md artifact manifest after each task (via manifest writer hook)

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
      "outputs": [
        { "path": "requirements.md", "contract": "requirements_doc@1" }
      ],
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
    def dispatch(self, task: Task, context: AgentContext,
                 idempotency_key: str) -> TaskResult:
        """
        Dispatch a task to the underlying AI runtime.
        idempotency_key: stable key for safe retries (workflow:task:run:attempt).
        Returns TaskResult with: status, outputs, handover_state, error, tokens_used.
        """
        ...
```

Context bundle passed to each agent:
```python
AgentContext(
    constitution=<merged constitution string including artifact manifest>,
    handover_state=<dict from previous tasks>,
    task_definition=<task YAML definition>
    # Note: task_inputs are NOT pre-loaded — agents read what they need
    # via their native tools using paths from the artifact manifest
)
```

---

## Hook Points

```python
engine.on_pre_task(task_id, callback)
engine.on_post_task(task_id, callback)    # "*" matches all tasks
engine.on_failure(task_id, callback)
engine.on_loop_exit(task_id, callback)
```

Default post-task hooks registered by the engine:
- `manifest_writer.write_artifact_manifest` — updates constitution.md after every task

---

## Concurrency Budget Config

```yaml
# ai-sdd.yaml
engine:
  max_concurrent_tasks: 3           # asyncio semaphore on dispatch
  rate_limit_requests_per_minute: 20
  cost_budget_per_run_usd: 10.00    # pause → HIL when exceeded
```

---

## Implementation Notes

- `asyncio` for parallel dispatch; semaphore enforces `max_concurrent_tasks`.
- State file at `.ai-sdd/state/workflow-state.json`; atomic writes (temp + rename).
- Hook dispatch: run all registered hooks in registration order.
- Handover state: completed tasks write a `handover` dict; next tasks receive it.
- On unrecoverable failure: persist state, emit on-failure, stop gracefully.
- Context assembly: pass merged constitution (includes manifest) + handover state. Do NOT pre-load artifact file contents — agents pull via native tools.

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
- Unit tests: concurrency budget — no more than N tasks dispatch simultaneously.
- Unit tests: context assembly — constitution included; file contents NOT pre-loaded.
- Integration tests: full workflow run (A → B → C); interruption + resume; parallel dispatch.
- Integration test: failed task halts downstream; on-failure hook fires.
- Integration test: manifest writer post-task hook fires after every task.

## Rollback/Fallback

- On unrecoverable task failure: persist FAILED state; stop engine safely.
- On adapter dispatch error: retry per adapter contract (T015), then mark FAILED.
- State file write failure: emit critical error; do not proceed to next task.
