# ai-sdd: Synthesized Roadmap

**Version:** 1.0.0-synthesized
**Date:** 2026-02-27
**Status:** Draft

---

## Effort Estimation Key

| Size | Engineering Days | Description |
|---|---|---|
| XS | 1–2 | Simple, well-understood scope |
| S | 3–4 | Moderate complexity, limited unknowns |
| M | 5–7 | Multiple components, integration work |
| L | 8–12 | High complexity, cross-cutting concerns |
| XL | 13+ | Major subsystem or high unknowns |

Estimates assume a single engineer per task. Parallel tracks reduce calendar time, not total effort.

---

## Milestones

| ID | Name | Outcome | Task Groups | Primary Tasks |
|---|---|---|---|---|
| M1 | Core Runtime | YAML pipeline runs end-to-end | A, B, C, D | T001, T002, T003, T004 |
| M2 | Safe Gates | HIL + evidence policy gate active | E | T005, T006 |
| M3 | Overlay Modes | Confidence/paired/review overlays operational | F | T007, T008 |
| M4 | Usability | CLI + config + adapters usable | G | T009 |
| M5 | MVP Demo | Repeatable demo with docs/artifacts | H | demo_package, runbook |
| M6 | Production Hardening | Reliability/security/observability uplift | hardening tracks | test_track, security_track, infra_track |

---

## Task Groups

### A. Agent Foundation
- **Scope:** AGT-001 to AGT-006
- **Deliverables:**
  - YAML schema for agents
  - Default agent definitions (BA, Architect, PE, LE, DEV, Reviewer)
  - Inheritance and override rules
- **Exit Criteria:**
  - Schema validation passes.
  - Default agents load without runtime patching.
  - Per-agent model and hyperparameter overrides resolve correctly.

### B. Workflow Foundation
- **Scope:** WF-001 to WF-006
- **Deliverables:**
  - Workflow schema
  - DAG loader
  - Dependency resolver
  - Loop configuration support
- **Exit Criteria:**
  - Invalid DAG is rejected with clear error.
  - Topological execution is verified.
  - Loop max-iteration and explicit exit conditions are enforced.

### C. Constitution Resolution
- **Scope:** CON-001 to CON-004
- **Deliverables:**
  - Hierarchical constitution merge engine
- **Exit Criteria:**
  - Root and nested constitutions merge deterministically.
  - Nearest-scope override precedence is enforced.

### D. Core Engine and State
- **Scope:** ENG-001 to ENG-005
- **Deliverables:**
  - Dispatcher
  - Hooks
  - State persistence and resume
- **Exit Criteria:**
  - Task state transitions are persisted and resumable.
  - Hook lifecycle callbacks are invoked consistently.
  - Runtime adapter interface is callable from engine.

### E. Safety and Governance Gates
- **Scope:** HIL, evidence policy gate
- **Deliverables:**
  - HIL approval flow (default on)
  - File-based queue fallback (default)
  - Evidence-based gate (not confidence-only)
- **Policy Dimensions:**
  - Requirement coverage (optional, tunable)
  - Acceptance evidence quality
  - Verification results (tests, lint, security)
  - Operational readiness evidence
  - Risk-tier routing (T0, T1, T2)
- **Exit Criteria:**
  - Tasks route by risk tier and evidence scorecard.
  - Missing required evidence blocks promotion and records reason.
  - Requirement coverage control can be disabled or tuned.

### F. Overlay Capabilities
- **Scope:** Confidence Loop, Paired Workflow, Agentic Review
- **Deliverables:**
  - Confidence loop overlay
  - Paired workflow overlay
  - Agentic review overlay
- **Exit Criteria:**
  - Overlays can be independently enabled/disabled via config.
  - Loops exit on explicit rule or max-iteration.
  - Overlay stack order is deterministic and documented.

### G. CLI, Config, and Developer Experience
- **Scope:** CLI, config discovery, validation, runtime adapters
- **Deliverables:**
  - CLI commands (run, resume, validate, hil)
  - Config discovery and merge
  - Validation and error UX
- **Exit Criteria:**
  - run, resume, and validate-config paths work.
  - Config errors fail fast with actionable diagnostics.

### H. Demo and Verification Harness
- **Scope:** MVP demonstration, repeatable checks
- **Deliverables:**
  - Demo workflow
  - Sample artifacts
  - Sequence diagram
  - Run/test script
- **Exit Criteria:**
  - Fresh clone can run demo using documented steps.
  - Expected artifacts are generated deterministically.
  - Troubleshooting covers common failures.

---

## Task Effort Breakdown

### Phase 1 Tasks

| Task | Title | Size | Days | Breakdown |
|---|---|---|---|---|
| **T001** | Agent System | S | 4 | Schema design (0.5) · Loader + inheritance resolution (1.5) · 6 default agent YAMLs (1) · Tests (1) |
| **T002** | Workflow System | M | 5 | Schema design (0.5) · DAG loader + cycle detection (2) · Topological sort (0.5) · Default SDD workflow YAML (1) · Tests (1) |
| **T003** | Constitution System | XS | 3 | Format spec (0.5) · Directory walk + resolver (1) · Section merge algorithm (1) · Tests (0.5) |
| **T004** | Core Engine | L | 8 | Engine execution loop (2) · State manager (1.5) · Context assembler (1.5) · Hooks system (1) · RuntimeAdapter interface (0.5) · Integration tests (1.5) |
| **T005** | HIL Overlay | S | 4 | Queue data model + file ops (1.5) · Engine hook integration (1) · CLI commands (0.5) · Tests (1) |
| **T009** | CLI, Config, Adapters | M | 7 | Config schema + loading + merge (2) · CLI commands: run/status/resume (1.5) · MockRuntimeAdapter (0.5) · ClaudeCodeAdapter (2) · Tests (1) |

**Phase 1 total effort:** 31 days

### Phase 2 Tasks

| Task | Title | Size | Days | Breakdown |
|---|---|---|---|---|
| **T006** | Confidence Scoring + Loop Overlay | S | 4 | EvalMetric model + scorer (1) · Confidence loop overlay (1.5) · Config schema (0.5) · Tests (1) |
| **T007** | Paired Workflow Overlay | M | 6 | Pair session model (1) · Driver/challenger loop (2) · Role switch logic (1) · Config schema (0.5) · Tests (1.5) |
| **T008** | Agentic Review Loop Overlay | S | 5 | Review decision model (0.5) · Review loop (2) · Constitution standards extraction (0.5) · Config schema (0.5) · Tests (1.5) |

**Phase 2 total effort:** 15 days

### Phase 3 Tasks

| Task | Title | Size | Days | Breakdown |
|---|---|---|---|---|
| **T010** | Python Workflow SDK | L | 12 | API design + fluent builder (3) · Task/agent DSL (2) · YAML export (2) · SDK docs + examples (3) · Tests (2) |

**Phase 3 total effort:** 12 days

**Total estimated engineering days:** 58 days (single engineer, sequential milestones)

---

## Milestone Sequencing

### M1 — MVP: Working End-to-End Pipeline
**Definition of done:** A user can run `ai-sdd run` on a project with default agents and YAML workflow, and tasks execute in dependency order with state persisted and HIL pausing on marked tasks.

**Included tasks:** T001, T002, T003, T004, T005, T009

**Critical path** (sequential lower bound):
```
T001 (4d) → T002 (5d) → T004 (8d) → T009 (7d)
                                  └──► T005 (4d)  [parallel with T009]
T003 (3d) ────────────► feeds T004
```

**M1 calendar estimate:** ~24 engineering days

### M2 — Safe Gates: HIL + Evidence Policy Gate
**Definition of done:** HIL overlay default-on with file queue; evidence policy gate active with risk-tier routing (T0/T1/T2).

**Included tasks:** T006 (confidence scoring) as prerequisite for evidence gate.

**M2 calendar estimate:** ~4 days after M1 (confidence scoring) + integration.

### M3 — Overlay Modes: Confidence + Paired + Review
**Definition of done:** All three overlays are independently configurable, tested, and can be composed (multiple overlays active on one workflow).

**Included tasks:** T006, T007, T008

**M3 calendar estimate:** ~10 engineering days after M2

### M4 — Usability: CLI + Config + Adapters
**Definition of done:** CLI commands, config discovery, runtime adapters for at least one provider (Claude Code) usable.

**Included tasks:** T009 (already part of M1). This milestone focuses on polishing.

**M4 calendar estimate:** ~3 days

### M5 — MVP Demo
**Definition of done:** Fresh clone demo run succeeds; expected artifacts produced; documentation complete.

**M5 calendar estimate:** ~5 days

### M6 — Production Hardening
**Definition of done:** Reliability, security, observability, and governance tracks completed.

**Effort estimate:** ~20 days (parallel tracks)

---

## Production Readiness Tracks

### Reliability
- Retries, backoff, idempotency per task
- Crash-safe resume and state integrity checks
- Load/soak testing for long-running workflows

### Security
- Secret handling and provider credential policy
- Prompt/output sanitization controls
- Supply-chain/dependency scanning in CI

### Observability
- Structured logs, traces, and correlation IDs
- Per-task metrics (latency, retries, token/cost, queue wait)
- Alertable SLOs

### Runtime Integration
- Hardened provider adapters (timeouts, quotas, failure mapping)
- Model routing policy integration
- Deterministic fallback behavior

### Governance
- Policy packs by risk tier
- Audit export of decisions/evidence
- Release-readiness checklist automation

---

## Functional MVP Definition

- Task groups A-H are complete at baseline depth.
- A reference run demonstrates multi-agent handovers and at least one bounded loop.
- Evidence-based gate and HIL routing decisions are visible in artifacts/logs.
- Runtime adapter scaffold executes through one real provider path and one mock path.
- Demo docs explain sequence, conditional logic, and script-vs-prompt responsibilities.

---

## Risks and Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Over‑reliance on confidence score | Unsafe auto‑approval | Enforce evidence‑based gate as primary control. |
| Requirement coverage noise | False blocks or false confidence | Keep requirement coverage optional and tunable. |
| Overlay interaction complexity | Non‑deterministic execution | Fix overlay order and test matrix per combination. |
| Provider/runtime instability | Pipeline flakiness | Adapter retries, circuit breakers, and mock fallback. |
| Human queue bottlenecks | Slow throughput | Risk‑tier routing and queue SLA metrics. |
| Confidence overuse | Suboptimal routing | Never use confidence as standalone gate. |
| Noisy requirement coverage | Overhead | Keep requirement coverage optional and tunable. |

---

## Sequencing Recommendation

1. Complete groups A‑D first.
2. Add group E immediately after D.
3. Implement group F after policy/HIL gates stabilize.
4. Finalize groups G and H for MVP consumability.
5. Start production tracks after MVP demo is stable and repeatable.

---

## MVP Scope Gate (M1 Ship Criteria)

- [ ] `ai-sdd run` executes default SDD workflow to completion on a test project
- [ ] State file is written and `ai-sdd run --resume` correctly skips COMPLETED tasks
- [ ] Custom agent YAML extending a default agent resolves correctly
- [ ] Sub‑module constitution overrides root constitution in agent context
- [ ] A task with `requires_human: true` pauses execution and is unblocked via `ai-sdd hil resolve`
- [ ] Schema validation errors are raised on startup for malformed agent/workflow YAML
- [ ] MockRuntimeAdapter is used in all unit tests (no real LLM calls in test suite)
