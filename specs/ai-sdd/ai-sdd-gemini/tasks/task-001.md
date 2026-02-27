# Task 001: Core Orchestrator & Constitutions

## Objective
Establish the foundational execution engine for `ai-sdd` and the context aggregation system.

## Requirements
1. **Thin Orchestrator**: Create the core engine that can accept a parsed Directed Acyclic Graph (DAG) of tasks.
2. **Task Dispatch**: The orchestrator must be able to dispatch a task to a generic interface representing an AI coding agent (e.g., a wrapper for ClaudeCode, Codex, or Gemini).
3. **Constitutions Engine**: 
   - Implement a context builder that recursively traverses upwards from a target directory.
   - Look for `constitution.yaml` or `constitution.md` files.
   - Merge these files to establish project-level and folder-level rules, purpose, and background.
   - Inject the resulting merged context into the system prompt for the dispatched agent.

## Acceptance Criteria
- Orchestrator successfully runs a hardcoded 2-step linear workflow.
- Constitutions defined in a subfolder successfully override/append to constitutions defined in the root folder during task execution.
