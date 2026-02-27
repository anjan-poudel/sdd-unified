# T008 Agentic Review Overlay

## Objective
Implement coder/reviewer loop with GO/NO_GO outcomes and rework feedback.

## Scope
- Review decision schema
- Rework loop behavior
- Quality guidelines from constitution

## Dependencies
- T004, T005, T006

## Steps
1. Define review decision schema.
2. Implement reviewer evaluation pass.
3. Feed required rework back to coder.
4. Enforce bounded loops with escalation.

## Definition of Done
- Review loop produces auditable decisions and bounded rework cycles.

## Test Strategy
- Integration tests for GO/NO_GO paths and escalation behavior.

## Rollback/Fallback
- On repeated NO_GO beyond max iterations, route to HIL.
