# ai-sdd: Synthesized Implementation Plan

**Version:** 0.1.0-draft
**Status:** Synthesized from Claude, Codex, and Gemini Plans

---

## 1. Executive Summary

The `ai-sdd` implementation is a declarative, configuration-driven orchestration system designed for Specification-Driven Development (SDD). It leverages agentic AI tools by enforcing a rigorous development methodology. This synthesis extracts the best architectural patterns, overlay mechanisms, and phased rollout strategies from multiple models to create a robust, deterministic framework.

The framework is delivered in three primary phases: Core Engine & YAML Configuration, Overlays & Loop Mechanics, and Developer Experience & Tooling.

---

## 2. Architecture & Execution Model

### 2.1 Component Overview (Extracted from Claude)

The architecture is built around a lightweight Directed Acyclic Graph (DAG) executor, configuration loaders, and overlay decorators.

```text
ai-sdd/
├── core/                      # Engine: orchestrator, workflow runner, state manager
│   ├── engine.py              # Main workflow loop (DAG execution)
│   ├── workflow_loader.py     # YAML workflow parser + DAG builder
│   ├── agent_loader.py        # YAML agent definition loader (supports inheritance)
│   ├── state_manager.py       # Task state persistence for resuming
│   ├── context_manager.py     # Context assembly (constitutions + task inputs)
│   └── hooks.py               # Lifecycle hooks
├── constitution/              # Constitution resolver (Recursive merge)
├── agents/                    # Agent system (YAML configurations)
├── workflows/                 # Workflow templates (YAML DAG definitions)
├── overlays/                  # Optional overlay modules (Decorators)
├── eval/                      # Evaluation metrics & confidence scoring
├── runtime/                   # Backend adapters for AI tools (Claude Code, Roo, etc.)
└── cli/                       # CLI entrypoint
```

### 2.2 Execution Model & Overlay Order (Extracted from Codex)

The execution model guarantees deterministic task routing and human oversight where necessary. The overlay order is crucial for safety and confidence evaluation.

1. **Load:** Parse configuration, agent schemas, and workflow DAG.
2. **Resolve:** Aggregate context via the `constitution/resolver.py` based on the task path.
3. **Dispatch:** Execute the task through the strict overlay chain:
   - **HIL (Human-in-the-Loop):** Always evaluated first.
   - **Evidence Policy Gate:** Checks acceptance criteria, tests, and operational readiness.
   - **Agentic Review:** (If enabled) Peer critique before progressing.
   - **Paired Workflow:** (If enabled) Driver/challenger iterative loops.
   - **Confidence Loop:** (If enabled) Auto-transition based on evaluation metrics.
   - **Agent Execution:** The actual invocation of the backend adapter (LLM).
4. **Persist:** Record state transitions (`state.json`) for auditability and resumption.

### 2.3 Configuration Schemas (Extracted from Claude & Gemini)

- **Workflow YAML:** Defines tasks, dependencies (DAG), required agents, inputs/outputs, and overlay toggles.
- **Agent YAML:** Defines the persona, tool (LLM provider), hyperparameters, and capabilities. Supports `extends: <base_agent>` for extensibility.
- **Constitution MD:** Hierarchical steering documents that merge upwards from the specific module to the project root.

---

## 3. Phased Rollout Strategy

### Phase 1: Core Engine & Configuration Layer
**Objective:** A functional pipeline using default agents and YAML workflows.
- Implement YAML loaders for Agents and Workflows.
- Build the core DAG execution engine and state manager.
- Develop the Constitution recursive resolver.
- Implement the basic CLI and the foundational `HIL` overlay.
- Provide initial runtime adapters for the AI tool backends.

### Phase 2: Overlays & Advanced Mechanics
**Objective:** Introduce multi-agent interactive loops, evaluation metrics, and routing.
- Implement explicit primitives for `max_iterations` and loop exit conditions.
- Build the Evaluation Metrics and Confidence Score engine.
- Implement the sequence of overlays: Agentic Review, Paired Workflow, and Confidence Loops.
- Enforce strict rules: Confidence never promotes by itself; evidence gate checks are mandatory; T2 routing requires human sign-off (Codex rule).

### Phase 3: Developer Experience & Tooling
**Objective:** Programmatic abstractions and workflow-as-code.
- Python SDK for fluent, programmatic workflow definition.
- Exporters from SDK to YAML.
- Comprehensive examples and CLI utilities for dry-running and constitution validation.

---

## 4. Gap Analysis & Proposed Solutions

While the synthesized plans outline a strong architecture, several critical operational gaps remain:

### Gap 1: Ambiguous Integration with AI Coding Tools
**Issue:** The plans mention "runtime/adapters/*" but do not detail how the orchestrator communicates with external agents (Claude Code, Roo Code, etc.) which often operate as interactive CLIs or complex applications themselves.
**Proposed Solution:** Define a robust `RuntimeAdapter` interface utilizing standard protocols (like the Model Context Protocol (MCP) or standard stdio wrappers). The adapter must handle asynchronous streams, intercept tool calls (if managing them centrally), and translate generic `execute_task` payloads into tool-specific commands (e.g., generating a prompt file and invoking `claude-code --prompt-file`).

### Gap 2: Context Window Management & Bloat
**Issue:** As the DAG progresses, aggregating constitutions, previous task outputs (design docs), and current requirements can quickly exceed context windows or dilute the LLM's focus.
**Proposed Solution:** Introduce a `ContextReducer` or `SemanticFilter` within the `context_manager.py`. This component should:
- Summarize older task outputs.
- Filter the context based on relevance (e.g., using basic embeddings or keyword matching) before injecting it into the agent's prompt.
- Enforce hard limits on context sizes, failing gracefully or paginating context if exceeded.

### Gap 3: State Recovery, Resiliency, & Debugging
**Issue:** The `state_manager.py` is present, but handling midway failures, infinite loops inside AI agents, or debugging complex DAGs is not well-defined.
**Proposed Solution:**
- Enhance the CLI with `--dry-run` and `--step` execution modes.
- Implement a robust replay mechanism that can resume a workflow from any previously completed node in the DAG using the persisted `state.json`.
- Add explicit circuit breakers inside the engine that timeout unresponsive runtime adapters.

### Gap 4: Testing the Orchestration Framework Itself
**Issue:** Testing complex, multi-agent interactions and overlay logic usually requires expensive and slow LLM calls, making CI/CD difficult.
**Proposed Solution:** Develop an `eval/mock_runtime` suite. This suite provides deterministic mock agents that return predefined responses or simulate failures. This allows the DAG logic, loop exits, and overlay execution order to be exhaustively unit-tested without external API calls.