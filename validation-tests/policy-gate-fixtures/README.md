# Policy Gate Fixtures (T0/T1/T2)

These fixtures battle-test the evidence-based policy gate routing behavior.

## Fixtures

1. `t0_auto_approve`
- Risk tier: `T0`
- Policy: `auto_approve_enabled=true`
- Expected route: `AUTO_APPROVE`

2. `t1_auto_review`
- Risk tier: `T1`
- Policy: `auto_review_enabled=true`
- Expected route: `AUTO_REVIEW`

3. `t2_human_queue`
- Risk tier: `T2`
- Policy: strict human path
- Expected route: `HUMAN_QUEUE` and autonomous pause

## Run

From repo root:

```bash
bash validation-tests/policy-gate-fixtures/run-fixtures.sh
```

This will:
- reset fixture review outputs
- run orchestrator in autonomous mode for each fixture
- write route artifacts under each fixture's `review/`
- generate metrics report:
  - `validation-tests/policy-gate-fixtures/results/audit_metrics.json`

Seeded review artifacts are stored under each fixture's `review_seed/` and copied into `review/` on every run.

## Notes

- Requirement coverage is intentionally optional/tunable in fixture policy configs.
- `t1_auto_review` includes a seeded human audit that disagrees with automated outcome to exercise disagreement metrics.
