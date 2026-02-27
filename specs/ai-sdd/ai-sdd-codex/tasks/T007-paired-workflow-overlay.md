# T007 Paired Workflow Overlay

## Objective
Implement driver/challenger paired loop with configurable role-switch policy.

## Scope
- Pair session context
- Role switching (`session`, `subtask`, `checkpoint`)
- Bounded loop exits and escalation

## Dependencies
- T004, T006

## Steps
1. Define pair session model/history.
2. Implement driver/challenger execution loop.
3. Add configurable role-switch strategy.
4. Support exits via approval/evidence criteria.

## Definition of Done
- Paired mode runs deterministically and exits safely.

## Test Strategy
- Integration tests for role switching and max-iteration escalation.

## Rollback/Fallback
- If pair state corrupts, escalate to HIL with full history.
