# T006: Confidence Scoring and Confidence Loop Overlay

**Phase:** 2 (Overlays)
**Status:** PENDING
**Dependencies:** T004 (core engine)

---

## Context

Confidence scoring provides an evidence-based signal to automate task transitions. The confidence score is computed as a function of evaluation metrics: `confidence = f([EvalMetric]) → decimal`.

When the confidence loop overlay is enabled and a task's score meets the threshold, the engine automatically proceeds to the next task without waiting for a reviewer or human.

This is **off by default** and should be enabled intentionally — higher thresholds increase quality but also latency and cost.

---

## Acceptance Criteria

```gherkin
Feature: Confidence scoring

  Scenario: Compute confidence score from eval metrics
    Given a set of EvalMetric objects with names, values, and weights
    When the confidence scorer is called
    Then it returns a decimal score between 0.0 and 1.0
    And the score reflects the weighted average of the metric values

  Scenario: Raw metrics as simpler alternative
    Given raw eval metric scores without weight configuration
    When the scorer is called in raw mode
    Then it returns the raw scores without computing a composite confidence score

  Scenario: Missing metric values
    Given a metric with no value computed yet
    When the scorer runs
    Then the missing metric contributes a score of 0.0 (not an error)

Feature: Confidence loop overlay

  Scenario: Auto-transition when threshold met
    Given a task with confidence loop enabled and threshold=0.80
    When the task runs and the confidence score is 0.85
    Then the engine automatically transitions to the next task
    And no human or reviewer input is required

  Scenario: Loop continues below threshold
    Given a task with confidence loop enabled and threshold=0.80
    When the task runs and the confidence score is 0.65
    Then the loop reruns the task
    And the iteration count increments

  Scenario: Loop exits at max iterations
    Given a task with confidence loop, threshold=0.80, max_iterations=3
    When 3 iterations complete without the score reaching 0.80
    Then the loop exits (does NOT silently auto-approve)
    And the on_loop_exit hook fires with reason="max_iterations_reached"
    And if HIL is enabled, escalation occurs

  Scenario: Confidence loop disabled
    Given a task with confidence loop disabled (default)
    When the task runs
    Then no confidence scoring occurs
    And the task follows standard completion logic
```

---

## EvalMetric Schema

```python
@dataclass
class EvalMetric:
    name: str               # e.g., "requirement_coverage"
    value: float            # 0.0 – 1.0
    weight: float = 1.0     # relative importance
    notes: str = ""
```

Scorer:

```python
def compute_confidence(metrics: list[EvalMetric]) -> float:
    total_weight = sum(m.weight for m in metrics)
    if total_weight == 0:
        return 0.0
    return sum(m.value * m.weight for m in metrics) / total_weight
```

---

## Workflow YAML Config

```yaml
tasks:
  design-l1:
    agent: architect
    overlays:
      confidence_loop:
        enabled: true
        threshold: 0.80
        max_iterations: 3
        eval_metrics:
          - name: requirement_coverage
            weight: 2.0
          - name: design_completeness
            weight: 1.5
          - name: clarity_score
            weight: 1.0
```

---

## Implementation Notes

- Confidence scoring is a pure utility function; keep it in `eval/scorer.py` separate from the overlay.
- The overlay hooks into `post_task` to evaluate the score and decide whether to loop or advance.
- Metrics are populated by the agent's output (the agent writes metric values into its output context).
- If `eval_metrics` is not configured in the task, fall back to raw scores from agent output.
- Document clearly: enabling confidence loops increases cost (more LLM calls per task).

---

## Files to Create

- `eval/metrics.py`
- `eval/scorer.py`
- `overlays/confidence/confidence_overlay.py`
- `tests/test_confidence_scorer.py`
- `tests/test_confidence_overlay.py`
