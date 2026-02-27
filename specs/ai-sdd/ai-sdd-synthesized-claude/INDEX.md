# ai-sdd: Synthesized Planning Documents Index

**Version:** 0.1.0-synthesized
**Date:** 2026-02-27
**Synthesized from:** ai-sdd-claude, ai-sdd-codex, ai-sdd-gemini

---

## Overview Documents

| Doc | Purpose |
|---|---|
| [PRD.md](PRD.md) | Product requirements, target users, success metrics |
| [PLAN.md](PLAN.md) | Architecture, component overview, phased delivery plan, migration map |
| [ROADMAP.md](ROADMAP.md) | Milestones, task groups, MVP gate |
| [GAPS-ANALYSIS.md](GAPS-ANALYSIS.md) | Identified gaps across source plans and proposed solutions |

---

## Tasks

### Phase 1: Core Engine

| Task | Title | Dependencies |
|---|---|---|
| [T001](tasks/T001-agent-system.md) | Agent System — YAML schema, loader, default agents | none |
| [T002](tasks/T002-workflow-system.md) | Workflow System — YAML schema, DAG loader, default template | T001 |
| [T003](tasks/T003-constitution-system.md) | Constitution System — recursive context resolution | none |
| [T004](tasks/T004-core-engine.md) | Core Engine — orchestrator, state manager, context assembler | T001, T002, T003 |
| [T005](tasks/T005-hil-overlay.md) | Human-in-the-Loop (HIL) Overlay | T004 |
| [T010](tasks/T010-cli-and-config.md) | CLI, Project Config, Runtime Adapter | T004 |
| [T011](tasks/T011-observability.md) | Observability — structured event emission and logging | T004 |

### Phase 2: Overlay Suite

| Task | Title | Dependencies |
|---|---|---|
| [T006](tasks/T006-evidence-policy-gate.md) | Evidence Policy Gate *(new — from Codex)* | T004, T005 |
| [T007](tasks/T007-confidence-overlay.md) | Confidence Scoring and Confidence Loop Overlay | T004, T006 |
| [T008](tasks/T008-paired-workflow-overlay.md) | Paired Workflow Overlay | T004, T007 |
| [T009](tasks/T009-agentic-review-overlay.md) | Agentic Review Loop Overlay | T004, T005, T007 |

### Phase 3: Workflow SDK

| Task | Title | Dependencies |
|---|---|---|
| T012 (TBD) | Python + TypeScript Workflow SDK | All Phase 1+2 |
| T013 (TBD) | Reference Example Projects | T012 |
| T014 (TBD) | Dry-Run Mode + Cost/Latency Docs | T012 |

### Phase 4: Production Hardening

| Track | Description |
|---|---|
| Reliability | Retries, idempotency, load tests |
| Security | Secret sanitization, supply-chain scan |
| Observability (extended) | Traces, metrics, SLO alerts |
| Runtime Integration | Timeout/quota, provider fallback |
| Governance | Audit export, policy packs |

---

## Execution Order (Phase 1)

```
T001 ──┐
       ├──► T002 ──► T004 ──► T005 ──► T006 (Phase 2)
T003 ──┘              │
                      ├──► T010
                      └──► T011
```

T001 and T003 can run in parallel (no shared dependencies).
T005, T010, T011 depend on T004 and can run in parallel.

---

## Key Design Decisions

1. **Overlays are decorator-wrapped hooks** — not subclasses of the engine. Core stays thin.
2. **Evidence Gate is mandatory for promotion** — confidence score is advisory only. Never sole criterion.
3. **Everything is YAML** until Phase 3 brings the Python + TypeScript SDK.
4. **Constitutions replace monolithic system prompts** — composable and maintainable.
5. **HIL is on by default** as a safety net; all other overlays require explicit opt-in.
6. **Default agents mirror sdd-unified roles** — zero-friction migration path.
7. **Observability is baked in from Phase 1** — not retrofitted. Secrets never in logs.
8. **Reviewer independence rule** — paired workflow challenger cannot be the same agent as the formal reviewer in a subsequent review task.
9. **Config merge: CLI > project > framework defaults** — predictable precedence.
10. **T2 risk tier always requires HIL** — no config bypass; governance is architectural.

---

## Synthesis Sources

| Feature | Best Source | Notes |
|---|---|---|
| Gherkin acceptance criteria | Claude | Most detailed; used throughout |
| Evidence Policy Gate | Codex | Unique contribution; critical governance layer |
| Production hardening roadmap | Codex | Added as Phase 4 |
| TypeScript SDK option | Gemini | Added alongside Python SDK in Phase 3 |
| HIL queue states (PENDING/ACKED/RESOLVED/REJECTED) | Codex | More complete state machine |
| Reviewer independence rule | Claude | Important safety constraint |
| Observability as Phase 1 requirement | Synthesized (gap) | Missing from all three; added here |
| Dry-run mode | Gemini | Added to CLI spec |
| Secret sanitization | Synthesized (gap) | Missing from all three; added to observability |
| Config merge cascade (CLI > file > defaults) | Claude | Most explicit |
