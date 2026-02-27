# ai-sdd: Roadmap

## Milestone 1: The Core Foundation (Phase 1)
**Focus**: Extensible configurations and basic execution.
*   **M1.1**: Define YAML schemas for Agents and Workflows.
*   **M1.2**: Implement Agent Loader supporting `extends`, LLM routing, and hyperparameters.
*   **M1.3**: Implement the Workflow DAG parser and thin core execution layer.
*   **M1.4**: Implement the recursive Constitutions context aggregator.
*   **M1.5**: Ship default agents (BA, PE, DEV, Reviewer) and a standard linear SDD workflow.

## Milestone 2: Safety & Evaluation (Phase 2A)
**Focus**: Guardrails and measurable task success.
*   **M2.1**: Implement `MAX_ITERATION` and exit condition primitives across all execution paths.
*   **M2.2**: Implement Human-in-the-loop (HIL) overlay (Enabled by default).
*   **M2.3**: Develop Evaluation Metrics tooling and the decimal Confidence Score calculator.

## Milestone 3: Advanced Overlays (Phase 2B)
**Focus**: Agentic interaction loops.
*   **M3.1**: Implement Confidence Level Loop (Auto-transition based on score thresholds).
*   **M3.2**: Implement Agentic Review Loop (Static roles, quality gating).
*   **M3.3**: Implement Paired Workflow Loop (Role-switching pair programming simulation).
*   **M3.4**: Ensure all Phase 2B overlays are configurable and *Disabled by default*.

## Milestone 4: SDK & Ecosystem (Phase 3)
**Focus**: Programmatic control and developer experience.
*   **M4.1**: Release Workflow SDK for programmatic definitions.
*   **M4.2**: Publish comprehensive examples and workflow templates.
*   **M4.3**: Documentation detailing cost/latency vs. quality tradeoffs (tuning the knobs).
