# Task 01: Core Orchestration Layer

## Description
Develop the minimal, thin core engine for the `ai-sdd` framework. This engine is strictly responsible for interpreting the execution order of workflows, triggering agents, managing handovers, and acting as the foundational substrate upon which all advanced overlays (like pairing or confidence loops) will sit.

## Requirements
- **Thin Core Engine:** The orchestrator must not inherently contain business logic related to code reviews, confidence thresholds, or pair programming. These must be treated as external "overlays".
- **Workflow Execution:** Given a parsed workflow (from YAML), the engine must sequentially or cyclically execute the defined nodes (agents).
- **Handovers:** Implement a structured mechanism for passing context, state, and control between agents during node transitions.
- **LLM Agnosticism:** The core execution mechanism must not be coupled to any specific LLM (e.g., Claude Code, Codex, Gemini).

## Acceptance Criteria
- [ ] A basic orchestrator runs a linear `A -> B -> C` agent workflow successfully.
- [ ] State and context are accurately preserved and handed over between `Agent A` and `Agent B`.
- [ ] No hardcoded assumptions about specific LLMs or role types (like "BA" or "PE") exist within the orchestrator's source code.