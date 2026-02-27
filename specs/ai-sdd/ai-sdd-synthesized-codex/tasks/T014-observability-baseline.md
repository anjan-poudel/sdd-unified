# T014 Observability Baseline

## Objective
Provide minimally sufficient telemetry for debugging and governance.

## Deliverables
- Structured event schema for task lifecycle
- Correlation/run IDs in every event
- Metrics: latency, retries, queue wait, token/cost, loop counts
- CLI summary and export hooks

## Done When
- Failed runs are diagnosable from logs/metrics without reproducing locally.
