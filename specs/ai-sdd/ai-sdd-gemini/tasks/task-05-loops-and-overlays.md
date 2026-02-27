# Task 05: Loops & Overlays (HIL, Paired Workflow, Agentic Review)

## Description
Implement the core workflow loops (or "overlays") that sit on top of the thin core orchestrator. These loops dictate complex, cyclical behaviors like pair programming simulations, agentic code reviews, confidence gating, and essential safety mechanisms like Human-in-the-Loop (HIL).

## Requirements

### Global Loop Mechanisms
- **Max Iterations:** Implement a global `MAX_ITERATION` limit on all cyclical workflows to prevent infinite stalling if no progress is made. Provide a sensible default that can be overridden.
- **Explicit Exit Conditions:** Ensure every loop must define at least one exit condition besides simply hitting the iteration cap.

### The Overlays
1. **Confidence Level Loop:** Auto-transition to the next task in the workflow if the computed confidence score exceeds a configured threshold (`X%`).
2. **Paired Workflow Loop:** Simulate pair programming. The loop continues until the confidence score is above `X%` or the reviewing pair explicitly signals it is okay to proceed. Pairs can switch roles (Driver vs. Reviewer) once a portion of work is completed.
3. **Agentic Review Loop:** A static-role loop (roles don't switch) where a coder agent submits code against formal guidelines (e.g., a PR checklist or design document) and a reviewer agent provides feedback.

### Human-in-the-Loop (HIL)
- **Interrupt System:** The workflow must pause execution and await user input when explicitly marked as requiring a human decision, when a deadlock/infinite loop is suspected, or for qualitative judgment calls.
- **Default State:** HIL must be toggled **ON** by default to ensure safety.

## Acceptance Criteria
- [ ] A `MAX_ITERATION` cap successfully breaks cyclical loops that fail to progress.
- [ ] The Human-in-the-Loop feature pauses the agent execution and resumes based on human input.
- [ ] A Paired Workflow loop correctly switches agent roles mid-task.
- [ ] An Agentic Review loop correctly rejects bad outputs until the criteria are satisfied or max iterations are reached.