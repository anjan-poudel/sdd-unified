## Task
Use this `sdd-unified` project to produce a complete specification package for a new framework named `ai-sdd`.

## Non-Negotiable Output Path
- Write all generated artifacts under `specs/ai-sdd-codex/`.
- Do not create or update artifacts under `specs/ai-sdd/`.

## Required Output Files
1. `specs/ai-sdd-codex/PRD.md`
2. `specs/ai-sdd-codex/PLAN.md`
3. `specs/ai-sdd-codex/INDEX.md`
4. `specs/ai-sdd-codex/ROADMAP.md`
5. `specs/ai-sdd-codex/ROADMAP.yaml`
6. `specs/ai-sdd-codex/tasks/T001-agent-system.md`
7. `specs/ai-sdd-codex/tasks/T002-workflow-system.md`
8. `specs/ai-sdd-codex/tasks/T003-constitution-system.md`
9. `specs/ai-sdd-codex/tasks/T004-core-engine.md`
10. `specs/ai-sdd-codex/tasks/T005-hil-overlay.md`
11. `specs/ai-sdd-codex/tasks/T006-confidence-overlay.md`
12. `specs/ai-sdd-codex/tasks/T007-paired-workflow-overlay.md`
13. `specs/ai-sdd-codex/tasks/T008-agentic-review-overlay.md`
14. `specs/ai-sdd-codex/tasks/T009-cli-and-config.md`

If a required file is missing, output is invalid.

## Product Direction and Constraints

### Core principles
- Core engine must be thin, extensible, and workflow-agnostic.
- Everything except core orchestration should be modeled as overlays.
- Agent roles must be externalized to YAML (no hardcoded BA/PE/LE logic in engine).
- Default agents are provided (BA, PE, DEV, Architect, LE, Reviewer), but replaceable.
- Workflows are YAML-defined DAGs with explicit dependencies, handovers, loops, and exits.
- Phase 2 can introduce workflow SDK (programmatic workflows), but YAML must be primary in v1.

### Core engine scope
- Recursive constitutions: root + subfolder merge/override.
- Orchestration lifecycle: load config, resolve dependencies, dispatch tasks, persist state, resume.
- Agent runtime abstraction over existing coding agents (Codex/Claude/Gemini/etc).
- Plan/task-breakdown behavior should be steered by constitution/rules, not hardcoded logic.
- Evaluation metrics tooling should support confidence computation from evidence; raw metrics are allowed as simpler mode.

### Overlay scope
- All agents support configurable LLM + hyperparameters.
- All loops require:
  - `max_iterations`
  - explicit non-iteration exit conditions
- Confidence overlay:
  - confidence scoring is optional and off by default
  - confidence is supportive signal, not standalone promotion gate
- Paired workflow overlay:
  - driver/challenger pattern
  - configurable role-switch policy
  - bounded loop with explicit exits
- Agentic review overlay:
  - non-switching coder/reviewer loop
  - artifact quality checks before progression
- HIL overlay:
  - on by default
  - manual approval path
  - deadlock fallback
  - file-based queue fallback by default

### Governance policy constraints
- Do not use model confidence percentage as standalone gate criterion.
- Use evidence-based policy gates with risk-tier routing.
- Evidence dimensions must include:
  - requirement coverage (optional, tunable parameter)
  - acceptance evidence quality
  - verification outcomes (tests/lint/security)
  - operational readiness evidence
- Risk tiers:
  - T0: lightweight review
  - T1: standard gate
  - T2: strict gate + human sign-off

## Document Requirements

### PRD requirements
- Include: problem statement, target users, product goals, non-goals, functional requirements, non-functional requirements, success metrics.
- Every requirement must include:
  - ID (stable format like `AGT-001`)
  - description
  - rationale
  - acceptance criteria
  - risk/constraint notes

### PLAN requirements
- Include architecture, component boundaries, config hierarchy, overlay model, execution model.
- Define dependency graph and phase order.
- Identify extension points and adapter interfaces.

### TASK requirements
- Each task file must include:
  - objective
  - in-scope / out-of-scope
  - dependencies
  - implementation steps
  - definition of done
  - test and verification strategy
  - rollback/fallback considerations

### ROADMAP requirements
- `ROADMAP.md` must include milestones, task groups, MVP gate, production hardening tracks, risks.
- `ROADMAP.yaml` must be machine-readable with stable top-level keys:
  - `version`
  - `date`
  - `status`
  - `goals`
  - `milestones`
  - `task_groups`
  - `functional_mvp_definition`
  - `production_readiness_tracks`
  - `sequencing_recommendation`
  - `risks`
  - `status_tracking_template`

## Consistency and Traceability Rules
- Requirement IDs in `PRD.md` must be referenced by `PLAN.md` and task docs.
- Task IDs and dependency chains must match `INDEX.md` and roadmap artifacts.
- No orphan IDs, no undefined terms, no contradictory defaults.
- If adding any new capability beyond constraints, label it `Proposed Extension`.

## Output Generation Order (Mandatory)
1. `PRD.md`
2. `PLAN.md`
3. task files (`T001`..`T009`)
4. `ROADMAP.md`
5. `ROADMAP.yaml`
6. `INDEX.md` (final cross-link check)

## Validation Checklist (Run Before Finalizing)
- All required files exist in `specs/ai-sdd-codex/`.
- No outputs created in `specs/ai-sdd/`.
- All requirement IDs are unique and cross-referenced.
- Every loop definition has both max iteration and explicit exit conditions.
- Confidence is never documented as standalone promotion gate.
- Requirement coverage is explicitly marked optional and tunable.
- HIL default-on behavior and file-based queue fallback are documented.
- ROADMAP.yaml parses as valid YAML and matches ROADMAP.md structure.

## Output Style Rules
- Prefer concise, implementation-ready language.
- Use deterministic heading structure.
- Use tables for requirements and milestones.
- Explicitly label assumptions.
- Do not include marketing language.
