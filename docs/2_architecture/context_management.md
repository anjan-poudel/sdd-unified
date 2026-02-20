# Context Management

## Purpose

Preserve continuity between agents and phases using `context.json`.

## Why It Matters

Without explicit context, agent switching loses:

- decision rationale
- prior review findings
- iteration/rework history
- requirement-to-task traceability

## Minimum Context Fields

- feature identity: `feature_id`, `feature_name`
- phase state: current phase/task/agent
- handover notes
- decision history
- iteration counters
- traceability links

## Recommended Additions (Pair Overlay)

```json
{
  "risk_tier": "T1",
  "pair_session": {
    "driver_agent": "sdd-pe",
    "challenger_agent": "sdd-architect"
  },
  "artifact_dri": "sdd-pe"
}
```

## Update Discipline

After each major task:

1. append handover summary
2. add decisions and rationale
3. update iteration counts
4. record artifact status

## Related

- `../5_reference/context_schema.md`
- `pair_review_overlay.md`

Full historical version: `../archive/non_core/2_architecture/context_management-full.md`
