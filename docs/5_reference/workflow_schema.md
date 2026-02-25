# Workflow Schema Reference

## Canonical Template

The canonical workflow template is:
- `../../templates/workflow.json.template`

## Core Fields

Core task fields:
- `command` (string)
- `status` (`PENDING|READY|RUNNING|COMPLETED|FAILED`)
- `dependencies` (string array of task IDs)

Route gate tasks are supported as standard workflow tasks (for example, `route-review-l1`, `route-review-l2`, `route-review-l3`) and use the same schema.

## Example Task

```json
{
  "design-l1": {
    "command": "sdd-architect-design-l1 --task_id=design-l1",
    "status": "PENDING",
    "dependencies": ["define-requirements"]
  }
}
```

## Related

See architecture details:
- `../2_architecture/workflow_engine.md`
