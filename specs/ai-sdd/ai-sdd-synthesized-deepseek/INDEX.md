# ai-sdd: Synthesized Planning Documents Index

**Status:** Draft
**Date:** 2026-02-27

---

## Documents

| Doc | Purpose |
|---|---|
| [PRD.md](PRD.md) | Product requirements, target users, success metrics |
| [PLAN.md](PLAN.md) | Architecture, component overview, phased delivery plan, migration map |
| [ROADMAP.md](ROADMAP.md) | Milestones, task groups, effort estimates, sequencing |
| [ROADMAP.yaml](ROADMAP.yaml) | Machine-readable roadmap with task groups and risks |

---

## Tasks

### Phase 1: Core Engine

| Task | Title | Dependencies | Size (Days) |
|---|---|---|---|
| [T001](tasks/T001-agent-system.md) | Agent System — YAML schema, loader, default agents | none | S (4) |
| [T002](tasks/T002-workflow-system.md) | Workflow System — YAML schema, DAG loader, default template | T001 | M (5) |
| [T003](tasks/T003-constitution-system.md) | Constitution System — recursive context resolution | none | XS (3) |
| [T004](tasks/T004-core-engine.md) | Core Engine — orchestrator, state manager, context assembler | T001, T002, T003 | L (8) |
| [T005](tasks/T005-hil-overlay.md) | Human-in-the-Loop (HIL) Overlay | T004 | S (4) |
| [T009](tasks/T009-cli-and-config.md) | CLI, Project Config, Runtime Adapter | T004 | M (7) |

### Phase 2: Overlays

| Task | Title | Dependencies | Size (Days) |
|---|---|---|---|
| [T006](tasks/T006-confidence-overlay.md) | Confidence Scoring and Confidence Loop Overlay | T004 | S (4) |
| [T007](tasks/T007-paired-workflow-overlay.md) | Paired Workflow Overlay | T004, T006 | M (6) |
| [T008](tasks/T008-agentic-review-overlay.md) | Agentic Review Loop Overlay | T004, T005, T006 | S (5) |

### Phase 3: Workflow SDK

| Task | Title | Dependencies | Size (Days) |
|---|---|---|---|
| T010 (TBD) | Python Workflow SDK | All Phase 1+2 tasks | L (12) |

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
6. **Confidence scoring is advisory only** and never used as a standalone promotion gate.
7. **Evidence policy gate** uses acceptance evidence, verification results, operational readiness, with optional requirement coverage.
8. **Risk-tier routing** (T0 lightweight, T1 standard, T2 strict + human sign-off) provides graduated governance.
9. **Overlay order** is fixed: HIL → Evidence policy gate → Agentic review → Paired workflow → Confidence → Agent execution.
10. **Complexity management** via raw metric mode as fallback; confidence off by default.

---

## Migration from sdd-unified

| sdd-unified | ai-sdd |
|---|---|
| `agents/roles/*.yaml` | `agents/defaults/*.yaml` (same schema, enhanced) |
| `commands/**/*.yaml` (agent commands) | Referenced in agent YAML `commands` section |
| `templates/workflow.json.template` | `workflows/default-sdd.yaml` (YAML, not JSON) |
| `orchestrator/main.py` | `core/engine.py` |
| `docs/2_architecture/pair_review_overlay.md` | `overlays/paired/` module |
| `docs/2_architecture/confidence_routing_overlay.md` | `overlays/confidence/` module |
| `orchestrator/policy_gate.py` | `overlays/policy_gate/` module |
| `orchestrator/human_queue.py` | `overlays/hil/` module |
| Hardcoded role names (sdd-ba, etc.) | Configurable via agent YAML `name` field |

---

## Next Steps

1. Review synthesized PRD for completeness.
2. Validate architecture against existing sdd-unified implementation.
3. Begin implementing tasks in order of dependencies.
4. Run validation tests as described in `validation-tests/`.
