# ai-sdd: Product Requirements Document (PRD)

## 1. Overview
The `ai-sdd` framework aims to provide a highly flexible, robust backbone for orchestrating agentic software engineering tasks and projects. It evolves beyond the rigid, hardcoded role structures of its predecessor (`sdd-unified`) by adopting a completely configurable, overlay-driven architecture.

## 2. Core Requirements

### 2.1 Core Orchestration Engine
- **Thin Layer**: The core provides basic AI workflow orchestration, focusing strictly on dependency resolution, state management, and task dispatching.
- **Agent Integration**: Leverages existing AI coding agents (ClaudeCode, Codex, Gemini, etc.) to perform the actual plan creation, task breakdown, and code generation.
- **Constitutions**: Introduces a recursive, folder-level context system. "Constitutions" define steers (purpose, background, overview, rules, and standards). A submodule or subfolder's constitution extends and overrides the parent folder's constitution, allowing highly localized contextual prompting at the system prompt level.
- **Evaluation & Confidence Metrics**: Provides tooling to calculate evaluation metrics from execution evidence, culminating in a confidence score (`confidence = f([]EvalMetric) -> decimal`). A fallback to raw evaluation scores must be supported if the decimal calculation introduces unnecessary complexity.

### 2.2 Agent Configuration
- **Externalized Personas**: AI Agent roles and responsibilities are externalized to YAML configuration files, removing hardcoded roles (e.g., BA, PE, LE).
- **Default Agents**: The framework will ship with default agents (e.g., BA, PE, DEV, Architect, Reviewer) out of the box.
- **Customization & Extensibility**: Clients can provide custom YAML files to define completely new agent roles, personas, and operating modes. Agents are extensible; an LLM can load extended agents which act as overlays on top of base agent definitions.
- **LLM Agnostic & Tunable**: Any agent can be configured to use any LLM provider/model. Hyperparameters (temperature, max tokens, etc.) are fully tunable per agent via the configuration.

### 2.3 Workflow Configuration
- **YAML Workflows**: Workflows are defined in YAML. These files dictate which agents interact with each other, how handovers are managed, and define loops and loop break conditions.
- **Future SDK**: A programmatic Workflow SDK will be delivered in a later phase to define workflows via code alongside the YAML capability.

## 3. Overlays
Everything beyond the thin core orchestration is treated as an optional overlay. 

### 3.1 Loop Primitives
- All loops must have a `MAX_ITERATION` configuration property to ensure loops exit if no progress is made or if progress is too slow.
- All loops must have explicit exit conditions evaluated at each iteration beyond just hitting `MAX_ITERATION`.

### 3.2 Specific Overlays
- **Confidence Level Loop**: Automates transitions. If an agent's confidence score meets or exceeds a configurable threshold (e.g., `X%`), the workflow automatically proceeds to the next task.
- **Paired Workflow Loop**: Simulates Pair Programming (e.g., PO & BA, or two DEVs). The loop continues until the confidence score exceeds `X%` or the reviewer pair signals approval. Roles switch (driver to reviewer) after a portion of work is implemented, either at the task or subtask level (configurable).
- **Agentic Review Loop**: Similar to the paired workflow, but roles do *not* switch. A coder agent implements, and a reviewer agent enforces code review guidelines to ensure PR quality metrics and requirements are met (e.g., PR code review loop, design review loop).
- **Agent Handovers**: Formalized context passing between disparate agents in the workflow graph.
- **Human in the Loop (HIL)**: A mandatory intervention overlay triggered when a task is explicitly marked as requiring human approval, or when deadlocks/infinite loops occur requiring human judgment.

## 4. Principles of Flexibility
The framework prioritizes "knobs and dials" to balance latency, cost, and quality.
- **Most components are configurable.**
- **Confidence Scoring**: Turned OFF by default.
- **Paired Workflow**: Turned OFF by default.
- **Agentic Review**: Turned OFF by default.
- **Human-in-the-loop (HIL)**: Turned ON by default (as a safety fallback).
- **Any LLM** can be assigned to any persona/role.

**Tradeoffs**: Enabling multiple overlays and loops significantly increases cost and latency while potentially improving output quality. Initially, all loops can be turned on, and users can selectively disable them or lower thresholds if the latency/cost becomes prohibitive.
