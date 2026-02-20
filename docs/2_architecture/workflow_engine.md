# Workflow Engine

## Purpose

Define how task dependencies and statuses drive feature execution.

## Workflow File

Canonical template: `../../templates/workflow.json.template`

Each task has:

- `command`
- `status`: `PENDING|READY|RUNNING|COMPLETED|FAILED`
- `dependencies`: upstream task IDs

## Execution Rules

1. A task can run only when all dependencies are `COMPLETED`.
2. Tasks with no unmet dependencies become `READY`.
3. `READY` tasks may run in parallel when independent.
4. Task completion unblocks downstream tasks.

## Minimal Example

```json
{
  "define-requirements": {
    "command": "sdd-ba-define-requirements --task_id=define-requirements",
    "status": "PENDING",
    "dependencies": ["init"]
  }
}
```

## Rework Pattern

- Review task fails -> corresponding rework task executes
- Rework task updates artifact
- Review task reruns
- Circuit breakers prevent infinite loops

## Operational Checks

- Validate no circular dependencies
- Validate every dependency ID exists
- Track stalled workflows (no `READY` tasks while `PENDING` remains)

## Related

- `iterative_reviews.md`
- `task_driven_implementation.md`

Full historical version: `../archive/non_core/2_architecture/workflow_engine-full.md`
