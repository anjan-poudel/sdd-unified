# T001 Agent System

## Objective
Implement YAML-based agent registry with defaults and extension support.

## Scope
- Agent schema
- Default agents (BA, Architect, PE, DEV, LE, Reviewer)
- Inheritance/override loader

## Dependencies
- none

## Steps
1. Define `agents.schema.yaml`.
2. Implement loader with `extends` resolution.
3. Add default YAML definitions.
4. Validate per-agent model/hyperparams.

## Definition of Done
- Agent config validation passes.
- Override precedence is deterministic.

## Test Strategy
- Unit tests for schema and inheritance merge.

## Rollback/Fallback
- Fallback to default agents if custom overlay fails validation.
