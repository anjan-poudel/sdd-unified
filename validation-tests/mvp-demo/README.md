# MVP Demo

This demo shows core concepts end-to-end:

1. Multi-agent execution across BA/Architect/PE/LE/Coder roles
2. Handover log entries in `context.json`
3. Review rejection and rework loop
4. Evidence-based policy routing
5. Human queue flow with file backend (optional) and resolution
6. Metrics report output

## Run

From repo root:

```bash
bash validation-tests/mvp-demo/run-mvp-demo.sh
python3 validation-tests/mvp-demo/verify_mvp_acceptance.py
```

## Outputs

- `validation-tests/mvp-demo/results/mvp_loop.log`
- `validation-tests/mvp-demo/results/mvp_queue.log`
- `validation-tests/mvp-demo/results/mvp_metrics.json`
- `validation-tests/mvp-demo/MVP_ACCEPTANCE_CHECKLIST.md`

## Optional queue override example

Disable queue pause:

```json
"human_queue": {
  "enabled": true,
  "backend": "file",
  "pause_on_enqueue": false
}
```
