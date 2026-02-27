# Task 004: Advanced Overlays (Review & Paired)

## Objective
Implement the highly interactive, multi-agent loop strategies.

## Requirements
1. **Agentic Review Loop**:
   - Implement an overlay where an outputting agent (Coder) submits artifacts to a Reviewer agent.
   - The loop continues until the Reviewer agent outputs a predefined success signal, adhering to code review guidelines injected via the constitution.
   - Roles do *not* switch.
2. **Paired Workflow Loop**:
   - Simulate pair programming.
   - Driver agent implements a portion, Challenger agent critiques.
   - Implement configurable role-switching (Driver becomes Challenger) upon successful subtask completion.
3. **Configuration**:
   - Ensure both overlays are disabled by default.
   - Ensure both overlays gracefully respect the `MAX_ITERATION` and HIL fallback mechanisms built in Task 003.

## Acceptance Criteria
- Agentic review successfully iterates a predefined number of times based on injected failures before passing.
- Paired workflow successfully switches active models/system prompts after subtask completion.
