# Task-Driven Implementation

## Purpose

Convert approved design into small, testable implementation units.

## Core Principle

Do not implement from one monolithic L3 plan. Generate discrete task files with explicit acceptance criteria.

## Task Unit Contract

Each task should define:

- `task_id`
- scope/goal
- dependencies
- acceptance criteria (BDD-style)
- expected artifacts/files

## Execution Pattern

1. Generate tasks from approved design.
2. Implement one task at a time (or parallelize independent tasks).
3. Review each task output against acceptance criteria.
4. Rework only failed tasks.

## Example Task Skeleton

```yaml
task_id: task-003
description: Implement JWT token generation
acceptance_criteria:
  - Given valid user credentials
  - When generateToken() is called
  - Then a signed JWT is returned
  - And token expiry is enforced
```

## Quality Rules

- acceptance criteria must be objective and testable
- tasks must be independently reviewable
- traceability to requirements must be maintained

## Related

- `workflow_engine.md`
- `iterative_reviews.md`
- `../4_guides/feature_development.md`

Full historical version: `../archive/non_core/2_architecture/task_driven_implementation-full.md`
