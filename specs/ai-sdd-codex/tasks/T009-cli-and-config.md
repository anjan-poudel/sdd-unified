# T009 CLI and Config

## Objective
Provide practical project interface for run/resume/validate/hil operations.

## Scope
- Project config schema and merge precedence
- CLI command surface
- Runtime adapter scaffold (mock + provider)

## Dependencies
- T004

## Steps
1. Define `ai-sdd.yaml` schema.
2. Implement config discovery and precedence.
3. Add CLI commands: `run`, `resume`, `validate-config`, `hil`.
4. Implement runtime adapter interface and mock adapter.

## Definition of Done
- CLI can execute and resume workflows with validated config.

## Test Strategy
- CLI integration tests and config validation tests.

## Rollback/Fallback
- If provider adapter fails, support deterministic mock fallback when configured.
