# Task 005: Evaluation Metrics & Confidence

## Objective
Provide a quantitative mechanism for the framework to determine when to automatically proceed without human intervention.

## Requirements
1. **Evidence Collection**: Build tooling to aggregate test results, linting scores, and validation outputs into an array of `EvalMetric` objects.
2. **Confidence Calculation**:
   - Implement a configurable function `f([]EvalMetric) -> decimal` to yield a normalized confidence score (0.0 to 1.0).
   - Provide a simplified configuration flag to bypass the decimal calculation and use raw eval scores directly (to reduce complexity for smaller setups).
3. **Confidence Level Loop**:
   - Implement an overlay that automatically approves a transition to the next task if the calculated confidence score exceeds the workflow's configured threshold (e.g., `> 0.85`).
   - This overlay should be disabled by default.

## Acceptance Criteria
- Workflow auto-advances when mock evaluation metrics generate a confidence score above the configured threshold.
- Workflow halts and routes to HIL or Review loop when the confidence score falls below the threshold.
