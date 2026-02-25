# T005 Human-in-the-Loop Overlay

## Objective
Implement default-on HIL control with file-based queue backend.

## Scope
- Queue item model and lifecycle
- Pause/resume on required-human tasks
- Deadlock and loop-exhaustion escalation

## Dependencies
- T004

## Steps
1. Define queue states (`PENDING`, `ACKED`, `RESOLVED`, `REJECTED`).
2. Implement file-based queue storage.
3. Integrate HIL hooks into engine transitions.
4. Expose CLI resolve/reject operations.

## Definition of Done
- Human approval gates and escalations are observable and functional.

## Test Strategy
- Integration tests for pause, resolve, reject, and timeout scenarios.

## Rollback/Fallback
- If queue write fails, block progression and emit critical error.
