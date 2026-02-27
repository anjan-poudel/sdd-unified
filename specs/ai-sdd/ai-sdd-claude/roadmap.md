# ai-sdd: Roadmap

**Version:** 0.1.0-draft
**Date:** 2026-02-23

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

| With parallelism | Calendar days |
|---|---|
| Week 1–2: T001 + T003 (parallel) | 4d elapsed |
| Week 2–3: T002 (blocked on T001) | +5d = 9d elapsed |
| Week 3–5: T004 (blocked on T001+T002+T003) | +8d = 17d elapsed |
| Week 5–7: T005 + T009 (parallel, both blocked on T004) | +7d = 24d elapsed |

**M1 calendar estimate: ~24 engineering days**

---

### M2 — Overlay Suite: Confidence + Paired + Review

**Definition of done:** All three overlays are independently configurable, tested, and can be composed (multiple overlays active on one workflow).

**Included tasks:** T006, T007, T008

**Critical path:**
```
T006 (4d) → T007 (6d)
         └──► T008 (5d)  [parallel with T007]
```

| With parallelism | Calendar days |
|---|---|
| T006 (required by both T007 and T008) | 4d elapsed |
| T007 + T008 in parallel | +6d = 10d elapsed |

**M2 calendar estimate: ~10 engineering days after M1**

---

### M3 — Hardening and Usability

**Definition of done:** Framework is installable into a real project, documentation is complete, and at least one end-to-end validation test passes using the default SDD workflow with a real LLM backend.

**Included tasks:** (no new T-numbered tasks; this is a hardening milestone)

| Work item | Days |
|---|---|
| End-to-end integration test (default SDD workflow, ClaudeCode backend) | 3 |
| Schema validation error messages (human-readable, actionable) | 2 |
| Install script + project scaffolding command (`ai-sdd init`) | 2 |
| Migration guide from sdd-unified | 1 |
| User documentation (getting started, workflow authoring, agent authoring) | 3 |
| Example projects (minimal and full SDD workflow) | 2 |

**M3 effort estimate: ~13 days**
**M3 calendar estimate: ~13 engineering days after M2**

---

### M4 — Workflow SDK (Phase 3)

**Definition of done:** A Python SDK allows workflows to be defined programmatically and serialized to YAML for execution by the core engine.

**Included tasks:** T010

**M4 calendar estimate: ~12 engineering days after M3**

---

## Summary Timeline (Sequential Milestones)

| Milestone | Calendar Days | Cumulative |
|---|---|---|
| M1 — MVP Core | 24 | 24 |
| M2 — Overlay Suite | 10 | 34 |
| M3 — Hardening & Usability | 13 | 47 |
| M4 — Workflow SDK | 12 | 59 |

**Total estimate: ~59 engineering days** (single engineer, sequential milestones)

With two engineers working in parallel across milestones, M1+M2 could reach ~20 calendar days.

---

## Critical Path

The longest dependency chain in the project:

```
T003 (3d)
    ↓
T001 (4d) → T002 (5d) → T004 (8d) → T005 (4d) → T006 (4d) → T007 (6d)
```

Length: 3+4+5+8+4+4+6 = **34 days** (if all run sequentially)
With parallelism: the ~24d M1 + 10d M2 = 34d is essentially the critical path.

---

## Risk Flags

| Task | Risk | Mitigation |
|---|---|---|
| T004 (Core Engine) | Largest task; hook design may require iteration | Build + validate hooks with T005 in the same sprint |
| T009 (ClaudeCodeAdapter) | Claude Code's execution model may not map cleanly to the RuntimeAdapter interface | Start with MockAdapter; treat ClaudeCodeAdapter as a research spike |
| T007 (Paired Workflow) | Role-switch logic and pair context accumulation are novel; complexity may be underestimated | Prototype driver/challenger loop before committing to full implementation |
| T003 (Constitution) | Section merge semantics need precise definition to avoid ambiguity | Define and document merge algorithm spec before writing code |
| M2 overlay composition | Multiple overlays active simultaneously may interact unexpectedly | Dedicate 1 day to overlay interaction tests before M2 close |

---

## MVP Scope Gate (M1 Ship Criteria)

The following must be true before M1 is considered complete:

- [ ] `ai-sdd run` executes default SDD workflow to completion on a test project
- [ ] State file is written and `ai-sdd run --resume` correctly skips COMPLETED tasks
- [ ] Custom agent YAML extending a default agent resolves correctly
- [ ] Sub-module constitution overrides root constitution in agent context
- [ ] A task with `requires_human: true` pauses execution and is unblocked via `ai-sdd hil resolve`
- [ ] Schema validation errors are raised on startup for malformed agent/workflow YAML
- [ ] MockRuntimeAdapter is used in all unit tests (no real LLM calls in test suite)
