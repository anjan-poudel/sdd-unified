# T007: Confidence Scoring and Confidence Loop Overlay

**Phase:** 2 (Overlay Suite)
**Status:** PENDING
**Dependencies:** T004 (core engine), T006 (evidence policy gate)

---

## Context

The confidence scoring system computes a decimal score from a set of evaluation metrics. This score is an **advisory signal only** — it can suggest that a task is ready to advance, but it cannot by itself promote an artifact. The Evidence Policy Gate (T006) always has the final say.

Two modes:
- **Composite mode**: `confidence = f([EvalMetric]) → decimal` (weighted aggregation).
- **Raw mode**: individual metric scores are evaluated directly without aggregation (simpler, for low-overhead tasks).

Confidence loop overlay: auto-advance advisory when score ≥ threshold. The engine emits the advisory; it is the policy gate that decides promotion.

This overlay is **off by default**.

---

## Acceptance Criteria

```gherkin
Feature: Confidence scoring

  Scenario: Composite confidence score computation
    Given three EvalMetrics with values [0.9, 0.8, 0.7] and equal weights
    When the scorer computes confidence
    Then the result is 0.8 (weighted mean)

  Scenario: Raw mode bypasses aggregation
    Given a task configured with raw score mode
    And individual metric scores [0.85, 0.90]
    When the scorer runs in raw mode
    Then individual scores are returned without aggregation
    And the threshold is checked against each individual metric

  Scenario: Confidence is off by default
    Given a workflow with no confidence_loop configuration
    When a task runs
    Then no confidence scoring occurs
    And no advisory signal is emitted

  Scenario: Confidence loop overlay fires advisory
    Given a task with confidence_loop.enabled=true and threshold=0.80
    When the task produces outputs with computed confidence=0.85
    Then the overlay emits an advisory signal "confidence threshold met"
    And the signal is included in the policy gate context
    But the task does not advance without the policy gate also passing

  Scenario: Confidence below threshold — loop continues
    Given a task with confidence_loop.enabled=true and threshold=0.80
    When the computed confidence is 0.72
    Then no advisory signal is emitted
    And the loop continues to the next iteration

  Scenario: Confidence loop reaches MAX_ITERATION
    Given confidence_loop.max_iterations=3 and threshold never met
    When 3 iterations complete
    Then the loop exits
    And if HIL is enabled, escalation occurs

  Scenario: Confidence score does not bypass policy gate
    Given a task with confidence=0.99 (above threshold)
    And policy_gate.risk_tier=T2
    When the confidence advisory is emitted
    Then the policy gate still requires HIL sign-off
    And the high confidence score is noted as advisory in the gate report
```

---

## EvalMetric Types

| Type | Description | Example |
|---|---|---|
| `test_coverage` | Percentage of code covered by tests | 0.87 |
| `lint_score` | Linting pass rate (0–1) | 1.0 (clean) |
| `security_score` | Security scan clean rate | 0.95 |
| `checklist_completion` | PR/review checklist items completed | 0.80 |
| `llm_judge` | LLM-as-a-judge score for output quality | 0.78 |
| `requirement_coverage` | Requirements covered by outputs | 0.92 |

---

## Workflow YAML Config

```yaml
tasks:
  design-l1:
    agent: architect
    overlays:
      confidence_loop:
        enabled: true
        mode: composite            # composite | raw
        threshold: 0.80
        max_iterations: 5
        metrics:
          - type: llm_judge
            weight: 0.5
          - type: checklist_completion
            weight: 0.3
          - type: requirement_coverage
            weight: 0.2
        exit_conditions:
          - "confidence_score >= 0.80"
          - "pair.challenger_approved == true"  # if paired_workflow also enabled
```

---

## Scorer Interface

```python
def compute_confidence(metrics: list[EvalMetric]) -> float:
    """Weighted mean of all metric scores. Returns decimal in [0.0, 1.0]."""
    ...

def compute_raw(metrics: list[EvalMetric]) -> list[float]:
    """Return raw individual metric scores without aggregation."""
    ...
```

---

## Implementation Notes

- The confidence score is computed post-task by the scorer.
- The score and metric breakdown are included in the gate report (T006).
- Overlays communicate via the shared `TaskContext` object — confidence writes its score there.
- LLM-judge metric: the agent itself is asked to score its own output against the acceptance criteria; the score is extracted from the response.

---

## Files to Create

- `eval/metrics.py`
- `eval/scorer.py`
- `overlays/confidence/confidence_overlay.py`
- `tests/test_scorer.py`
- `tests/test_confidence_overlay.py`

---

## Test Strategy

- Unit tests: weighted mean computation, raw mode, edge cases (empty metrics, all-zero).
- Unit tests: advisory signal emitted only when threshold met.
- Unit tests: confidence does not bypass policy gate (integration assertion).
- Integration test: confidence loop with max_iterations; HIL escalation.

## Rollback/Fallback

- If confidence computation fails, log warning and treat score as 0.0 (conservative).
- Disable overlay via config; standard execution path continues unaffected.
