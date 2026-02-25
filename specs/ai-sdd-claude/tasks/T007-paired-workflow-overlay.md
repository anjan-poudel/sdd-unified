# T007: Paired Workflow Overlay

**Phase:** 2 (Overlays)
**Status:** PENDING
**Dependencies:** T004 (core engine), T006 (confidence scoring, for optional exit condition)

---

## Context

The paired workflow overlay implements a driver/challenger loop for any task. The driver produces an artifact; the challenger critiques it. The loop continues until:
- The confidence score meets the threshold (if confidence scoring is enabled), OR
- The reviewer pair signals approval.

Role switching (driver ↔ challenger) is configurable: it can happen per full session, per subtask, or at defined checkpoints.

This overlay is **off by default**.

---

## Acceptance Criteria

```gherkin
Feature: Paired workflow overlay

  Scenario: Basic driver/challenger loop
    Given a task with paired workflow enabled, driver=pe, challenger=architect
    When the task starts
    Then the driver (pe) runs first and produces an artifact
    Then the challenger (architect) critiques the artifact
    Then the driver revises based on the critique
    And the loop continues until an exit condition is met

  Scenario: Exit on challenger approval
    Given a paired loop with exit condition "pair.challenger_approved == true"
    When the challenger signals approval
    Then the loop exits and the artifact is locked
    And the workflow advances to the next task

  Scenario: Exit on confidence threshold
    Given a paired loop with confidence_loop overlay also enabled
    And threshold=0.82
    When the driver output scores 0.85 confidence
    Then the loop exits automatically
    And challenger critique is skipped for this iteration

  Scenario: Role switch at subtask level
    Given a paired loop with role_switch=subtask
    When the first subtask completes
    Then the challenger becomes the new driver for the next subtask
    And the driver becomes the new challenger

  Scenario: Role switch per session (no switch)
    Given a paired loop with role_switch=session (default)
    When the entire task loop completes
    Then the driver and challenger roles do not swap during the session

  Scenario: Max iterations reached
    Given a paired loop with max_iterations=4
    When 4 iterations complete without an exit condition being satisfied
    Then the loop exits
    And if HIL is enabled, escalation occurs with full pair history

  Scenario: Paired workflow disabled (default)
    Given a task with no paired workflow configuration
    When the task runs
    Then no driver/challenger loop occurs
    And the task runs with its assigned single agent
```

---

## Pair Session Context Schema

```json
{
  "pair_session": {
    "driver_agent": "pe",
    "challenger_agent": "architect",
    "current_role_driver": "pe",
    "iteration": 2,
    "role_switch": "session",
    "history": [
      {
        "iteration": 1,
        "driver_output_summary": "...",
        "challenger_critique": "...",
        "challenger_approved": false
      }
    ],
    "challenger_approved": false
  }
}
```

---

## Workflow YAML Config

```yaml
tasks:
  design-l1:
    agent: architect
    overlays:
      paired_workflow:
        enabled: true
        driver_agent: architect
        challenger_agent: pe
        role_switch: session        # options: session | subtask | checkpoint
        max_iterations: 5
        exit_conditions:
          - "pair.challenger_approved == true"
          - "confidence_score >= 0.85"
```

---

## Implementation Notes

- The paired overlay wraps task dispatch: run driver, then challenger, then driver again (loop).
- Challenger prompt is: "You are the challenger. Critique the following driver output and identify assumptions, gaps, and risks. Signal `challenger_approved: true` if the output is ready to lock."
- Role switch logic: track `current_role_driver`; swap on the configured trigger.
- Pair history is accumulated in `pair_session.history` and injected into each subsequent iteration's context.
- The overlay communicates with the confidence overlay (if active) via the shared task context object.
- Reviewer independence rule: if an independent review task follows, the challenger should not be the same agent assigned as the formal reviewer.

---

## Files to Create

- `overlays/paired/paired_overlay.py`
- `overlays/paired/pair_session.py`
- `tests/test_paired_overlay.py`
