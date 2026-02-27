# T008: Agentic Review Loop Overlay

**Phase:** 2 (Overlays)
**Status:** PENDING
**Dependencies:** T004 (core engine), T005 (HIL, for escalation), T006 (confidence, optional)

---

## Context

The agentic review overlay implements a coder/reviewer loop where roles do NOT switch. The coder produces an artifact; the reviewer critiques it against configurable quality guidelines. The coder revises and resubmits. The loop continues until the reviewer signals GO or MAX_ITERATION is reached.

Typical use cases:
- PR code review loop: coder produces code, reviewer checks against PR quality metrics.
- Design review loop: designer produces design, reviewer checks against architecture standards.

This overlay is **off by default**.

---

## Acceptance Criteria

```gherkin
Feature: Agentic review overlay

  Scenario: Basic review loop
    Given a task with agentic review enabled, coder=dev, reviewer=reviewer
    When the task starts
    Then the coder (dev) runs and produces an artifact
    Then the reviewer checks the artifact against quality guidelines
    And if the reviewer signals NO_GO, the coder receives the feedback and reruns

  Scenario: Review passes — GO
    Given a review loop where the reviewer signals GO
    When the reviewer outputs GO
    Then the loop exits
    And the artifact is marked as review-approved
    And the workflow advances

  Scenario: Review fails — NO_GO with rework
    Given a review loop where the reviewer signals NO_GO with required_rework items
    When the reviewer output is NO_GO
    Then the coder re-runs with the required_rework items injected into context
    And the iteration count increments

  Scenario: Max iterations escalation
    Given a review loop with max_iterations=3
    When 3 iterations complete without a GO decision
    Then the loop exits
    And HIL is triggered (if enabled) with the full review history

  Scenario: Quality guidelines injected from constitution
    Given the constitution.md contains a "Code Review Standards" section
    When the review loop runs
    Then the reviewer agent receives the code review standards from the constitution
    And applies them when evaluating the artifact

  Scenario: Agentic review disabled (default)
    Given a task with no agentic review configuration
    When the task runs
    Then no review loop occurs
    And the task follows standard completion logic
```

---

## Review Decision Schema

```json
{
  "review_decision": {
    "reviewer_agent": "reviewer",
    "iteration": 2,
    "decision": "NO_GO",
    "failed_criteria": [
      "Missing unit tests for edge case X",
      "Function Y exceeds complexity threshold"
    ],
    "required_rework": [
      "Add test for null input handling in method processPayment()",
      "Extract logic from Y into smaller functions"
    ],
    "passed_criteria": [
      "Naming conventions followed",
      "API contracts match spec"
    ],
    "timestamp": "2026-02-23T12:00:00Z"
  }
}
```

---

## Workflow YAML Config

```yaml
tasks:
  execute-task-001:
    agent: dev
    overlays:
      agentic_review:
        enabled: true
        reviewer_agent: reviewer
        max_iterations: 3
        quality_guidelines: "from_constitution"   # or inline string
        exit_conditions:
          - "review.decision == GO"
```

---

## Implementation Notes

- The overlay wraps task dispatch: run coder, then reviewer, then loop.
- Reviewer prompt template: "You are an independent reviewer. Evaluate the following artifact against the quality guidelines below. Output a JSON review decision with `decision: GO|NO_GO`, `failed_criteria`, `required_rework`, and `passed_criteria`."
- When `quality_guidelines: "from_constitution"`, extract the review standards section from the resolved constitution.
- Required rework items from the review decision are appended to the coder's context for the next iteration.
- Review history is accumulated and injected into subsequent iterations so the reviewer can track progress.
- This overlay is independent of the paired workflow overlay — they can both be active on different tasks in the same workflow.

---

## Files to Create

- `overlays/review/review_overlay.py`
- `overlays/review/review_decision.py`
- `tests/test_review_overlay.py`
