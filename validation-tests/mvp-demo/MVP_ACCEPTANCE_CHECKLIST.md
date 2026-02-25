# MVP Acceptance Checklist

Use this checklist after running:

```bash
bash validation-tests/mvp-demo/run-mvp-demo.sh
```

## A. Multi-Agent Flow

- [ ] `mvp_loop.log` includes tasks run by these agents:
  - `sdd-ba`
  - `sdd-architect`
  - `sdd-pe`
  - `sdd-le`
  - `sdd-coder`
- [ ] `validation-tests/mvp-demo/feature-loop/context.json` has non-empty `execution_log`.

## B. Handover Continuity

- [ ] `validation-tests/mvp-demo/feature-loop/context.json` contains `handover_notes.history`.
- [ ] `handover_notes.history` has at least 5 entries.
- [ ] Entries include `task_completed` and `from_agent`.

## C. Review Loop (Reject -> Rework -> Re-Review)

- [ ] `mvp_loop.log` contains:
  - `Review rejected - forcing design-l1-rework to READY`
  - `Task: design-l1-rework`
  - subsequent rerun of `review-l1-ba`
- [ ] `validation-tests/mvp-demo/feature-loop/workflow.json` shows:
  - `design-l1-rework.status == COMPLETED`
  - `review-l1-ba.status == COMPLETED`

## D. Policy Routing

- [ ] `validation-tests/mvp-demo/feature-loop/review/review_routing_design_l1.json` exists.
- [ ] `.../review_routing_design_l2.json` exists.
- [ ] `.../review_routing_design_l3.json` exists.
- [ ] Each routing artifact includes:
  - `route`
  - `risk_tier`
  - `evidence_summary`

## E. Human Queue (Optional + File Backend Default)

- [ ] `mvp_queue.log` contains `HUMAN_QUEUE` pause message.
- [ ] `validation-tests/policy-gate-fixtures/t2_human_queue/review/human_review_queue.json` exists.
- [ ] Queue item has:
  - `queue_id`
  - `status`
  - `backend == "file"`
- [ ] After resolve path, `validation-tests/policy-gate-fixtures/t2_human_queue/review/human_audit_design_l1.json` exists.

## F. Metrics Output

- [ ] `validation-tests/mvp-demo/results/mvp_metrics.json` exists and parses.
- [ ] JSON includes keys:
  - `route_distribution`
  - `rework_events_completed`
  - `handover_events`
  - `audit_disagreement_rate`
- [ ] `rework_events_completed >= 1`
- [ ] `handover_events >= 5`

## G. Test Gate

- [ ] `python3 -m unittest discover -s orchestrator -p 'test_*.py' -v` passes.

## H. Sign-Off

- [ ] MVP demonstrates core concepts end-to-end.
- [ ] File-based human queue behavior is optional/configurable.
- [ ] Team agrees this is sufficient for stakeholder demo.
