# T011: Observability — Structured Event Emission and Logging

**Phase:** 1 (Core Engine) — foundational; production hardening in Phase 4
**Status:** PENDING
**Dependencies:** T004 (core engine)

---

## Context

**This task addresses a gap identified across all three model plans (Claude, Codex, Gemini).**

None of the source plans defined observability as a first-class requirement. Codex mentions it in the production hardening roadmap, but without a concrete specification. Without structured observability, debugging multi-agent workflows is difficult and enterprise adoption is blocked.

Observability must be baked in from Phase 1 — not retrofitted. Phase 1 delivers structured logging and event emission. Phase 4 (Production Hardening) extends with distributed traces, metrics, and SLO alerts.

**Critical constraint:** Secrets must never be written to logs or state files.

---

## Acceptance Criteria

```gherkin
Feature: Structured event emission

  Scenario: Task lifecycle events are logged
    Given a running workflow
    When a task transitions from PENDING to RUNNING
    Then a structured log event is emitted with: task_id, status, timestamp, agent
    When the task transitions to COMPLETED
    Then a structured log event is emitted with: task_id, status, outputs, duration_ms

  Scenario: Constitution resolution is traced
    Given a task that resolves constitutions from 3 levels
    When the resolver runs
    Then a log event is emitted with the resolution trace (ordered list of files merged)

  Scenario: Overlay activity is logged
    Given a task with paired_workflow overlay active
    When each driver/challenger iteration completes
    Then a structured event is emitted with: overlay=paired_workflow, iteration, decision

  Scenario: HIL events are logged
    Given a HIL queue item is created
    When the item is created, resolved, or rejected
    Then a structured event is emitted with: hil_item_id, task_id, trigger, status, timestamp

  Scenario: Secrets are never logged
    Given an agent with an API key in its config
    When any log event is emitted
    Then the API key does not appear in any log output
    And state files do not contain the API key

  Scenario: Log level filtering
    Given log_level=INFO in ai-sdd.yaml
    When DEBUG-level events are emitted
    Then they are not written to the log output

  Scenario: Log rotation (Phase 4)
    Given a long-running workflow that produces >100MB of logs
    When the log file size exceeds the configured limit
    Then the log is rotated automatically
```

---

## Event Schema

All events follow this structure:

```json
{
  "version": "1",
  "timestamp": "2026-02-27T10:30:00.000Z",
  "level": "INFO | WARN | ERROR | DEBUG",
  "event_type": "task.started | task.completed | task.failed | overlay.iteration | hil.created | hil.resolved | constitution.resolved | engine.started | engine.completed",
  "workflow": "default-sdd",
  "task_id": "design-l1",
  "agent": "architect",
  "details": {
    // event-type-specific fields; never contains secrets
  }
}
```

---

## Event Types (Phase 1)

| Event Type | Trigger | Key Details |
|---|---|---|
| `engine.started` | Engine begins run | workflow, project |
| `engine.completed` | Workflow finishes | total_duration_ms, tasks_completed |
| `task.started` | Task begins execution | task_id, agent, iteration |
| `task.completed` | Task finishes | task_id, outputs, duration_ms |
| `task.failed` | Task fails | task_id, error_type, error_message |
| `task.retrying` | Adapter retry | task_id, attempt_number |
| `overlay.iteration` | Overlay loop iterates | overlay_type, iteration, decision |
| `hil.created` | HIL item created | hil_item_id, task_id, trigger |
| `hil.resolved` | HIL item resolved | hil_item_id, resolved_by |
| `hil.rejected` | HIL item rejected | hil_item_id, reason |
| `constitution.resolved` | Constitution merged | task_id, files_merged (list) |

---

## Secret Sanitization

The emitter runs a sanitization pass before any log write:
- Strip fields matching known secret patterns: API keys, tokens, passwords.
- Replace with `[REDACTED]`.
- Configurable additional patterns via `observability.secret_patterns` in `ai-sdd.yaml`.

---

## Implementation Notes

- Emitter is a singleton, initialized at engine startup.
- Log output: structured JSON to `ai-sdd.log` and optionally stdout.
- Log file path: configurable in `ai-sdd.yaml` (`observability.log_file`).
- All engine hooks (pre-task, post-task, on-failure, on-loop-exit) emit events via the emitter.
- Phase 4 extension: OpenTelemetry traces, Prometheus metrics, SLO alerting.

---

## Files to Create

- `observability/emitter.py`
- `observability/sanitizer.py`
- `observability/events.py` (event schema dataclasses)
- `tests/test_emitter.py`
- `tests/test_sanitizer.py`

---

## Test Strategy

- Unit tests: each event type emits correct schema fields.
- Unit tests: secret sanitization removes API keys and passwords from log output.
- Unit tests: log level filtering (DEBUG events suppressed when level=INFO).
- Integration test: full workflow run produces event log; events match expected task transitions.

## Rollback/Fallback

- If log file write fails: log to stderr only; do not fail the workflow.
- Observability is best-effort — a logging failure must not stop task execution.
