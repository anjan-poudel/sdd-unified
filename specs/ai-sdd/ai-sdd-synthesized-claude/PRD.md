# ai-sdd: Synthesized Product Requirements Document

**Version:** 0.1.0-synthesized
**Date:** 2026-02-27
**Status:** Draft
**Synthesized from:** ai-sdd-claude, ai-sdd-codex, ai-sdd-gemini

---

## 1. Problem Statement

`sdd-unified` proved the value of specification-driven, multi-agent development. However, it has structural limitations that prevent broad adoption:

- Agent roles are hardcoded (BA, PE, LE, etc.) and cannot be replaced without modifying the framework.
- Workflow sequences are fixed — they cannot be reconfigured without changing core files.
- Overlays (pair programming, confidence scoring, policy gates) are documented but not first-class configurable features.
- There is no recursive context/standards system — every project starts from scratch.
- LLM selection and hyperparameters are not configurable per agent.
- No evidence-based governance layer — artifact promotion decisions lack formal audit trails.

Projects need a **flexible, overlay-based orchestration framework** that provides sensible defaults but lets teams swap, extend, or disable any component without touching framework code.

---

## 2. Vision

`ai-sdd` is a **meta-framework for agentic software engineering pipelines**.

It provides:
- A thin, composable core engine.
- Externalized agent definitions via YAML.
- YAML-based workflow definitions (DAG).
- A constitution system for recursive project context management.
- A set of optional, independently configurable overlays (paired workflow, confidence scoring, agentic review, evidence policy gate, human-in-the-loop).
- Default agent set (BA, PE, DEV, Architect, LE, Reviewer) that teams can use, extend, or replace.
- A production-hardening track for enterprise adoption (security, observability, governance).

Teams can run `ai-sdd` with zero configuration changes and get a working SDD pipeline. Or they can fully customize every agent, workflow, and overlay to suit their project's risk profile and team structure.

---

## 3. Target Users

| Persona | Need |
|---|---|
| **Solo developer** | Automated spec → code pipeline with minimal setup. |
| **Small team** | Shared agent definitions and configurable review gates. |
| **Enterprise team** | Custom agents per domain, compliance-controlled workflows, risk-tiered reviews, audit trails. |
| **Framework integrator** | Embed `ai-sdd` into existing toolchains (CI, project management). |

---

## 4. Core Requirements

### 4.1 Agent System

| ID | Requirement |
|---|---|
| AGT-001 | Agent roles and responsibilities are defined in YAML files, not hardcoded. |
| AGT-002 | Default agents provided: BA, PE, DEV, Architect, LE, Reviewer. |
| AGT-003 | Clients can provide their own agent YAML definitions to replace or extend defaults. |
| AGT-004 | Agents are extensible via an `extends` attribute; a custom agent can inherit from a base agent and override specific attributes (overlay inheritance model). |
| AGT-005 | Each agent can be configured with its own LLM provider and model. |
| AGT-006 | Each agent can be configured with LLM hyperparameters (temperature, max_tokens, etc.). |
| AGT-007 | Schema validation runs on agent load; invalid YAML fails fast with a clear error. |
| AGT-008 | Fallback to default agents when a custom agent override fails validation. |

### 4.2 Workflow System

| ID | Requirement |
|---|---|
| WF-001 | Workflows are defined in YAML files as directed acyclic graphs (DAGs). |
| WF-002 | Workflow YAML defines: tasks, dependencies, assigned agent, inputs, outputs, loop conditions, and overlay config. |
| WF-003 | The engine resolves task dependencies and executes tasks in valid topological order. |
| WF-004 | Independent tasks can execute in parallel. |
| WF-005 | Default workflow templates are provided that mirror the current SDD pipeline. |
| WF-006 | Workflows support loops with configurable `MAX_ITERATION` and explicit exit conditions beyond iteration count. |
| WF-007 | Cycle detection is performed at load time; cyclic graphs fail fast. |

### 4.3 Constitution System

| ID | Requirement |
|---|---|
| CON-001 | A "constitution" is a set of steering files (purpose, background, rules, standards) that define context for a project or sub-module. |
| CON-002 | Constitutions are hierarchical: a child folder's constitution inherits and can override a parent's constitution. |
| CON-003 | The engine merges active constitutions into the system prompt context for each agent at execution time. |
| CON-004 | Constitution resolution is recursive and deterministic (sub-module overrides parent, which overrides root). |

### 4.4 Core Engine

| ID | Requirement |
|---|---|
| ENG-001 | The engine provides a thin orchestration layer: load workflow, resolve dependencies, dispatch tasks to agents, collect outputs. |
| ENG-002 | Engine state (task status, context, iteration counts) is persisted to a structured JSON file store. |
| ENG-003 | Engine exposes integration hooks: pre-task, post-task, on-failure, on-loop-exit. |
| ENG-004 | Uses existing AI coding agents (Claude Code, Codex, Gemini, etc.) as execution backends via a `RuntimeAdapter` interface. |
| ENG-005 | Agent plan and task-breakdown rules are injected via constitution (system prompt level), not hardcoded in the engine. |
| ENG-006 | Engine can resume interrupted workflows from last persisted state. |
| ENG-007 | On unrecoverable task failure, the engine persists state and stops safely. |

### 4.5 Evaluation Metrics

| ID | Requirement |
|---|---|
| EVL-001 | The engine provides a tool for computing a confidence score as a function of evaluation metrics: `confidence = f([EvalMetric]) → decimal`. |
| EVL-002 | Supported metric types: test coverage, linting scores, checklist completion, LLM-as-a-judge scores. |
| EVL-003 | Raw eval metric scores are available as a simpler alternative when confidence scoring adds too much complexity. |
| EVL-004 | Confidence scoring is **off by default** and must be explicitly enabled per workflow. |
| EVL-005 | Confidence score is an **advisory signal only** — it must not be the sole criterion for artifact promotion. |

---

## 5. Overlay Requirements

All overlays are **off by default** except HIL. Overlays compose via a decorator chain around core task dispatch.

### 5.1 Human-in-the-Loop (HIL) Overlay

| ID | Requirement |
|---|---|
| HIL-001 | HIL is **on by default**. |
| HIL-002 | Tasks can be marked as requiring human approval before proceeding. |
| HIL-003 | HIL is triggered automatically when a deadlock or unresolvable loop condition is detected (loop exhaustion). |
| HIL-004 | HIL queue exposes pending items to a human operator with context and decision options. |
| HIL-005 | Default queue backend is file-based. |
| HIL-006 | HIL queue item lifecycle: `PENDING` → `ACKED` → `RESOLVED` / `REJECTED`. |

### 5.2 Evidence Policy Gate Overlay

| ID | Requirement |
|---|---|
| PG-001 | A confidence percentage **must not** be a standalone gate criterion for artifact promotion. |
| PG-002 | Gate uses three categories of evidence: acceptance evidence, verification results (tests/lint/security), and operational readiness. |
| PG-003 | Requirement coverage check is optional and tunable. |
| PG-004 | Three risk tiers: T0 (lightweight), T1 (standard), T2 (strict + mandatory human sign-off). |
| PG-005 | T2-tier promotions require HIL sign-off regardless of confidence score. |

### 5.3 Confidence Loop Overlay

| ID | Requirement |
|---|---|
| CL-001 | When enabled, if a task's confidence score exceeds a configurable threshold `X%`, the engine provides an advisory signal to advance. |
| CL-002 | Threshold `X` is configurable per workflow or per task. |
| CL-003 | Loops have `MAX_ITERATION` and explicit exit conditions beyond iteration count. |
| CL-004 | Confidence loop exit does not bypass the Evidence Policy Gate. |

### 5.4 Paired Workflow Overlay

| ID | Requirement |
|---|---|
| PW-001 | Supports driver/challenger pair execution for any task. |
| PW-002 | The pair continues a loop until confidence score exceeds `X%` OR the reviewer pair signals approval. |
| PW-003 | Role switching (driver ↔ challenger) is configurable: per session, per subtask, or at defined checkpoints. |
| PW-004 | Examples: PO + BA pair, Dev + Dev pair (pair programming). |
| PW-005 | Loops have `MAX_ITERATION` and explicit exit conditions. |
| PW-006 | If pair state corrupts, escalate to HIL with full pair history. |
| PW-007 | Reviewer independence rule: if a formal independent review follows, the challenger must not be the same agent as the formal reviewer. |

### 5.5 Agentic Review Loop Overlay

| ID | Requirement |
|---|---|
| AR-001 | Similar to paired workflow but roles do NOT switch: coder produces, reviewer critiques. |
| AR-002 | Coder follows code review guidelines (from constitution) to ensure artifact meets configurable quality metrics. |
| AR-003 | Review decision is GO / NO_GO; NO_GO includes required rework feedback. |
| AR-004 | Loops have `MAX_ITERATION` and explicit exit conditions. |
| AR-005 | Repeated NO_GO beyond max iterations routes to HIL. |
| AR-006 | Review decisions are auditable (stored in review log). |

---

## 6. Flexibility & Configuration Principles

| Principle | Detail |
|---|---|
| **Everything configurable** | All overlays, thresholds, LLM settings, and loop conditions are externalized in config files. |
| **Overlays off by default** | Confidence scoring, paired workflow, evidence gate, and agentic review are disabled unless explicitly enabled. |
| **HIL on by default** | Human oversight is on unless explicitly disabled. |
| **Any LLM, any agent** | Each agent can use a different LLM provider and model. |
| **Overlay composability** | Multiple overlays can be active on the same workflow simultaneously. |
| **Confidence is advisory only** | A confidence score alone can never promote an artifact. Evidence must back it. |
| **Latency/cost tradeoff transparency** | Documentation explicitly states that enabling more overlays increases cost and latency. Start with all on and selectively disable. |

---

## 7. Non-Functional Requirements

| ID | Requirement |
|---|---|
| NFR-001 | Framework core has no mandatory dependency on a specific LLM provider. |
| NFR-002 | Agent YAML files and workflow YAML files are human-readable and editable without programming knowledge. |
| NFR-003 | The engine fails fast and clearly when configuration is invalid (schema validation on startup). |
| NFR-004 | State files are structured (JSON), versioned, and inspectable. |
| NFR-005 | Engine can resume interrupted workflows from last persisted state. |
| NFR-006 | Framework is installable into an existing project without modifying the project's structure. |
| NFR-007 | All workflow execution events are emitted to a structured log for observability. |
| NFR-008 | Secrets are never written to state files or logs. |

---

## 8. Out of Scope (v1)

- GUI / web dashboard for monitoring workflows.
- Native CI/CD pipeline integration (provided via hooks, not built-in).
- Multi-project federation or shared agent registries.
- Cost/token tracking per workflow run (planned for Phase 3).

---

## 9. Success Metrics

| Metric | Target |
|---|---|
| Time to first working pipeline for a new project | < 30 minutes with default agents + workflow |
| Agent replacement (swap one default agent for a custom one) | No framework code changes required |
| Overlay enable/disable | Single config flag change, no code changes |
| Workflow customization (add/remove tasks) | YAML-only change |
| Evidence gate bypass | Impossible by design (T2 always requires HIL sign-off) |
