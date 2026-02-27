# T010 Expression DSL and Safe Evaluator

## Objective
Define and enforce a safe, deterministic expression language for loop and gate conditions.

## Deliverables
- DSL grammar (`==`, `!=`, `>`, `>=`, `<`, `<=`, boolean ops, bounded path lookups)
- Parser + evaluator without arbitrary code execution
- Validation errors with task/file pointers
- Golden tests for valid/invalid expressions

## Done When
- All `exit_conditions` and gate expressions are parsed by DSL only.
- No runtime `eval` or equivalent dynamic execution paths remain.
