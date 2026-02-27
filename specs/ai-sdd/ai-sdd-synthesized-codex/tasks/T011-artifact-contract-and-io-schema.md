# T011 Artifact Contract and Task I/O Schema

## Objective
Introduce versioned, typed artifact contracts so task outputs are machine-checkable before handover.

## Deliverables
- `artifact.schema.yaml` with versioning
- Per-task output declarations and compatibility checks
- Validation in workflow loader and runtime before dispatch

## Done When
- Incompatible producer/consumer contracts fail before execution.
- Artifact compatibility appears in diagnostics and run logs.
