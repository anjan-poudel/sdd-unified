# Task 04: Evaluation Metrics & Confidence Scoring

## Description
Implement the tooling necessary to evaluate task outputs and compute a confidence score. This score acts as the gating mechanism for advanced overlays like the Confidence Level Loop and the Paired Workflow Loop.

## Requirements
- **Evaluation Metrics:** Create tools capable of calculating specific evaluation metrics from task evidence (e.g., test coverage, linting scores, PR checklist completion, or LLM-as-a-judge criteria).
- **Confidence Computation:** Implement a formula or aggregator function: `confidence = f([]EvalMetric) -> decimal`.
- **Raw Score Fallback:** Ensure that if computing a strict decimal confidence score adds too much complexity for simple tasks, raw evaluation scores can be used directly as the evaluation gate.
- **Configurability:** Ensure this entire evaluation mechanism is configurable and disabled by default.

## Acceptance Criteria
- [ ] The tool successfully calculates a normalized confidence score based on a set of provided evaluation metrics.
- [ ] A fallback mechanism allowing raw scores to bypass the `f()` computation is implemented.
- [ ] The scoring mechanism is easily toggleable via workflow or agent configuration YAMLs.