# ai-sdd: Planning Documents Index

**Status:** Draft
**Date:** 2026-02-23

---

## Documents

| Doc | Purpose |
|---|---|
| [PRD.md](PRD.md) | Product requirements, target users, success metrics |
| [PLAN.md](PLAN.md) | Architecture, component overview, phased delivery plan, migration map |

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
| [T009](tasks/T009-cli-and-config.md) | CLI, Project Config, Runtime Adapter | T004 |

### Phase 2: Overlays

| Task | Title | Dependencies |
|---|---|---|
| [T006](tasks/T006-confidence-overlay.md) | Confidence Scoring and Confidence Loop Overlay | T004 |
| [T007](tasks/T007-paired-workflow-overlay.md) | Paired Workflow Overlay | T004, T006 |
| [T008](tasks/T008-agentic-review-overlay.md) | Agentic Review Loop Overlay | T004, T005, T006 |

### Phase 3: Workflow SDK

| Task | Title | Dependencies |
|---|---|---|
| T010 (TBD) | Python Workflow SDK | All Phase 1+2 tasks |

---

## Execution Order (Phase 1)

```
T001 ──┐
       ├──► T002 ──► T004 ──► T005
T003 ──┘              │
                      └──► T009
```

T001 and T003 can run in parallel (no shared dependencies).
T002 depends on T001. T004 depends on T001, T002, T003.
T005 and T009 depend on T004 and can run in parallel.

---

## Key Design Decisions

1. **Overlays are decorator-wrapped hooks**, not subclasses of the engine. This keeps the core thin.
2. **Everything is a YAML file** until Phase 3 brings the SDK. This lowers the barrier to entry.
3. **Constitutions replace monolithic system prompts** — they're composable and maintainable.
4. **HIL is on by default** as a safety net; all other overlays require explicit opt-in.
5. **Default agents mirror sdd-unified roles** — existing users get a zero-friction migration path.
