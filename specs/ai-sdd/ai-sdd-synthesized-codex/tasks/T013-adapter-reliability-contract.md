# T013 Adapter Reliability Contract

## Objective
Standardize provider adapter behavior under failures and quotas.

## Deliverables
- Unified adapter error taxonomy
- Timeout/retry/backoff defaults
- Idempotency and dedupe keys for retries
- Deterministic mapping from adapter errors to engine task states

## Done When
- Mock and one real adapter conform to the same contract tests.
