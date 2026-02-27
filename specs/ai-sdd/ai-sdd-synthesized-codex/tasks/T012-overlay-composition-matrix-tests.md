# T012 Overlay Composition Matrix Tests

## Objective
Guarantee deterministic behavior across overlay combinations.

## Deliverables
- Matrix for {HIL, policy gate, review, paired, confidence}
- Invariant assertions (bounded loops, no silent promotion, deterministic routing)
- Golden trace fixtures

## Done When
- Pairwise matrix passes in CI.
- High-risk combinations have full-combination integration tests.
