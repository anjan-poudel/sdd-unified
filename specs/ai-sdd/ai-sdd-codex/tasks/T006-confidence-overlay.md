# T006 Confidence Overlay

## Objective
Implement optional confidence scoring and advisory routing overlay.

## Scope
- Metric model and scorer
- Confidence loop behavior
- Integration with evidence policy gate

## Dependencies
- T004

## Steps
1. Define `EvalMetric` schema and scorer.
2. Implement optional confidence overlay hooks.
3. Ensure confidence is advisory only.
4. Integrate with evidence-gate decision context.

## Definition of Done
- Confidence can influence routing but cannot solely promote artifacts.
- Raw metric mode works without composite scoring.

## Test Strategy
- Unit tests for scoring math.
- Integration tests ensuring promotion requires evidence gate pass.

## Rollback/Fallback
- Disable overlay by config and continue standard execution path.
