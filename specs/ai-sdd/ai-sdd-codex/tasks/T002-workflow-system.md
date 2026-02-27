# T002 Workflow System

## Objective
Implement YAML workflow DAG loader with loop and handover support.

## Scope
- Workflow schema
- DAG build/topological ordering
- Loop constraints (`max_iterations` + exits)

## Dependencies
- T001

## Steps
1. Define `workflow.schema.yaml`.
2. Implement DAG parser and cycle detection.
3. Validate agent references from registry.
4. Add default SDD workflow template.

## Definition of Done
- Invalid workflows fail fast.
- Valid workflows execute in topological order.

## Test Strategy
- Unit tests for validation/cycle detection.
- Integration test for multi-step workflow.

## Rollback/Fallback
- Reject malformed workflow and emit actionable diagnostics.
