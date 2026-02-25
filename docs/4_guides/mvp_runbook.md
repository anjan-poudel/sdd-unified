# MVP Runbook

This runbook executes a functional MVP demonstration of:

- multi-agent orchestration
- handovers via `context.json`
- review rejection/rework loops
- evidence-based policy routing
- optional file-based human queue
- audit metrics reporting

## Commands

Run complete demo:

```bash
bash validation-tests/mvp-demo/run-mvp-demo.sh
```

Inspect pending human queue items:

```bash
python3 orchestrator/human_queue.py validation-tests/policy-gate-fixtures/t2_human_queue list --status PENDING
```

Resolve a queued item:

```bash
python3 orchestrator/human_queue.py validation-tests/policy-gate-fixtures/t2_human_queue ack --queue-id <id> --reviewer principal
python3 orchestrator/human_queue.py validation-tests/policy-gate-fixtures/t2_human_queue resolve --queue-id <id> --decision GO --reviewer principal --summary "Approved"
```

## Expected Artifacts

- `validation-tests/mvp-demo/results/mvp_loop.log`
- `validation-tests/mvp-demo/results/mvp_queue.log`
- `validation-tests/mvp-demo/results/mvp_metrics.json`
- `validation-tests/policy-gate-fixtures/t2_human_queue/review/human_review_queue.json`
- `validation-tests/mvp-demo/MVP_ACCEPTANCE_CHECKLIST.md`

## Troubleshooting

1. Queue not found:
- verify `context.json` has `policy_gate.human_queue.file_path`
- verify route decision is `HUMAN_QUEUE`

2. Workflow appears stuck:
- inspect `workflow.json` for `FAILED` review tasks
- inspect `context.json.circuit_breaker`

3. No metrics comparisons:
- ensure `human_audit_*.json` exists for routed phases
