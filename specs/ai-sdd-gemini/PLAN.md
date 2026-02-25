# ai-sdd: Implementation Plan

## 1. Executive Summary
The `ai-sdd` implementation will be divided into three primary phases. Phase 1 focuses on the thin core engine and YAML configuration layer. Phase 2 introduces the advanced loop mechanics and overlays. Phase 3 provides developer tooling and the programmatic SDK.

## 2. Architecture Overview
- **Core Orchestrator**: A lightweight Directed Acyclic Graph (DAG) executor that reads workflow states, resolves dependencies, and dispatches tasks to the configured AI agents.
- **Constitution Engine**: A recursive file parser that walks the directory tree upwards from the current task execution context to merge `constitution.yaml` or `constitution.md` files into a unified system prompt.
- **Agent Config Loader**: Parses agent YAML definitions, handling inheritance (`extends` keyword) and applying LLM router settings and hyperparameters.
- **Overlay Decorators**: The advanced features (Paired Workflow, Confidence Loop, HIL) wrap around the core task execution logic, conditionally triggered by the workflow configuration.

## 3. Phased Rollout

### Phase 1: Core Engine & YAML Configuration
**Objective**: Build the foundational routing and context management system capable of executing linear, multi-agent workflows.
- Implement the YAML Agent Configuration parser and loader.
- Implement the YAML Workflow DAG parser.
- Develop the Constitutions Engine (recursive context aggregation).
- Create the core task dispatcher integrating with external AI tools (ClaudeCode, Codex, Gemini).
- Supply default agent YAML files (BA, PE, DEV, Architect, Reviewer).

### Phase 2: Overlays & Loop Mechanics
**Objective**: Introduce the complex, multi-agent interactive loops and confidence routing that form the framework's advanced capabilities.
- Implement `MAX_ITERATION` and explicit exit condition primitives for the orchestrator.
- Build the Human-in-the-Loop (HIL) interrupter (enabled by default).
- Build the Evaluation Metrics and Confidence Score engine (`f([]EvalMetric) -> decimal`).
- Implement the **Confidence Level Loop** overlay.
- Implement the **Agentic Review Loop** overlay.
- Implement the **Paired Workflow Loop** overlay (with role switching).

### Phase 3: Developer Experience & Tooling
**Objective**: Lower the barrier to entry for enterprise teams.
- Release the Workflow SDK (Python/TypeScript) for programmatic pipeline definition.
- Build comprehensive example projects (e.g., Simple linear SDD, High-assurance Paired Workflow SDD).
- Provide CLI utilities for validating constitutions and dry-running workflows.

## 4. Technical Considerations
- **Extensibility**: Agent files must support an `extends: <base_agent>` attribute to allow overlaying behavior dynamically.
- **Complexity Management**: The confidence scoring mechanism must provide a toggle to fall back to simple raw evaluation scores to prevent the configuration from becoming unmanageable for small teams.
