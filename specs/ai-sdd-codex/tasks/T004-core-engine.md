# T004 Core Engine

## Objective
Deliver thin orchestration runtime with persistence, hooks, and resume.

## Scope
- Task dispatch loop
- State machine persistence
- Hook lifecycle
- Context assembly

## Dependencies
- T001, T002, T003

## Steps
1. Implement task state model and transitions.
2. Build dispatch loop with dependency readiness checks.
3. Add persistence checkpoints and resume logic.
4. Wire pre/post/failure/loop-exit hooks.

## Definition of Done
- End-to-end workflow runs and resumes correctly.

## Test Strategy
- Integration tests for interruption/resume and failed-task handling.

## Rollback/Fallback
- On unrecoverable task failure, persist state and stop safely.
