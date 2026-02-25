# Task 003: Loop Primitives & HIL Overlay

## Objective
Build the safety guardrails required for multi-agent loops and implement the default Human-in-the-Loop system.

## Requirements
1. **Loop Primitives**:
   - Ensure the orchestrator's state manager enforces a `MAX_ITERATION` limit on any cyclic path.
   - Provide a mechanism for a workflow transition to evaluate dynamic exit conditions.
2. **Human-in-the-Loop (HIL)**:
   - Build an overlay that intercepts task execution if a task is flagged with `requires_human: true`.
   - The engine must pause execution, save state, and present a prompt to the user to approve, reject, or provide guidance.
   - The engine must automatically trigger the HIL overlay if `MAX_ITERATION` is hit to resolve deadlocks.
   - HIL must be enabled by default.

## Acceptance Criteria
- A workflow containing an infinite loop automatically halts and escalates to HIL upon reaching the default `MAX_ITERATION`.
- Tasks marked for human review successfully pause execution until manual input is provided via CLI.
