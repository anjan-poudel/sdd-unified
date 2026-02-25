# T003 Constitution System

## Objective
Implement recursive constitution resolution for project/submodule context.

## Scope
- Constitution format
- Recursive merge resolver
- Deterministic override precedence

## Dependencies
- none

## Steps
1. Define constitution schema/sections.
2. Implement directory ascent/lookup.
3. Merge sections with nearest-scope precedence.

## Definition of Done
- Effective constitution is deterministic for any task path.

## Test Strategy
- Unit tests for merge precedence and missing section behavior.

## Rollback/Fallback
- If no constitution found, run with framework default constitution.
