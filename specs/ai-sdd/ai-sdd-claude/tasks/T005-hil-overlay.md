# T005: Human-in-the-Loop (HIL) Overlay

**Phase:** 1 (Core Engine — included in Phase 1 as HIL is on by default)
**Status:** PENDING
**Dependencies:** T004 (core engine with hooks)

---

## Context

HIL is the only overlay that is **on by default**. It provides a safety net:
- Tasks explicitly marked as requiring human approval are paused until a human provides a decision.
- Deadlocks (a loop reaching MAX_ITERATION without an exit condition) are escalated to a human.
- A human operator can inspect the context, provide guidance, and unblock the workflow.

---

## Acceptance Criteria

```gherkin
Feature: Human-in-the-loop overlay

  Scenario: Task requires human approval
    Given a task with `requires_human: true` in the workflow YAML
    When the task completes its agent execution
    Then the engine pauses and writes a HIL request to the queue
    And the workflow does not advance until a human responds

  Scenario: Human approves — workflow proceeds
    Given a HIL request for task "review-l1" is pending
    When a human operator marks the request as APPROVED
    Then the engine reads the approval
    And unblocks the downstream tasks

  Scenario: Human rejects — task reruns
    Given a HIL request for task "review-l1" is pending
    When a human operator marks the request as REJECTED with notes
    Then the engine re-queues the task with the human's notes injected into context
    And the task reruns

  Scenario: Loop deadlock escalation
    Given a loop task that has reached MAX_ITERATION without exiting
    And HIL is enabled
    When MAX_ITERATION is hit
    Then the engine writes a deadlock HIL request with the full loop history
    And pauses execution until a human resolves it

  Scenario: HIL queue inspection
    Given one or more pending HIL requests
    When the operator runs `ai-sdd hil list`
    Then all pending requests are shown with task name, context summary, and options

  Scenario: HIL disabled
    Given HIL is disabled via config (`hil.enabled: false`)
    And a task is marked `requires_human: true`
    When the task completes
    Then the engine logs a warning and auto-approves
    And the workflow continues without pausing
```

---

## HIL Request Schema

```json
{
  "request_id": "hil-001",
  "task_id": "review-l1",
  "reason": "requires_human",
  "status": "PENDING",
  "context_summary": "...",
  "full_context_path": ".ai-sdd/state/hil/hil-001-context.md",
  "created_at": "...",
  "options": ["APPROVE", "REJECT"],
  "resolution": null,
  "resolution_notes": null,
  "resolved_at": null
}
```

---

## Implementation Notes

- HIL queue is stored as JSON files in `.ai-sdd/state/hil/`.
- CLI command `ai-sdd hil list` shows pending items.
- CLI command `ai-sdd hil resolve <request_id> --decision APPROVE|REJECT [--notes "..."]` resolves a request.
- Engine polls the HIL queue directory for resolutions (file-based approach, runtime-agnostic).
- Deadlock detection: hook into `on_loop_exit(task, reason="max_iterations_reached")`.
- Config: `hil.enabled: true` (default), `hil.queue_path: .ai-sdd/state/hil/`.

---

## Files to Create

- `overlays/hil/hil_overlay.py`
- `overlays/hil/hil_queue.py`
- `cli/hil_commands.py`
- `tests/test_hil_overlay.py`
