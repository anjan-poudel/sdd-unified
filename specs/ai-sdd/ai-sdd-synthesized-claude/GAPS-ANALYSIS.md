# ai-sdd: Gaps Analysis

**Date:** 2026-02-27
**Scope:** Comparison of ai-sdd-claude, ai-sdd-codex, ai-sdd-gemini plans

---

## 1. Model Comparison Summary

### What Each Model Gets Right

| Aspect | Claude | Codex | Gemini |
|---|---|---|---|
| Detail level | Highest — full Gherkin ACs, JSON schemas, file lists | Concise — good rollback/fallback sections | Medium — clear principles, good roadmap |
| Architecture clarity | Strong overlay decorator chain spec | Strong with evidence gate | Strong on extensibility principles |
| Evidence governance | Missing | **Best** — Evidence Policy Gate with T0/T1/T2 tiers | Missing |
| Production readiness | Missing | **Best** — explicit hardening tracks | Mentions in Phase 3 only |
| Developer experience | Good | Good | **Best** — cost/latency docs, TypeScript SDK, examples |
| HIL state machine | Basic | **Best** — PENDING/ACKED/RESOLVED/REJECTED | Basic |
| Reviewer independence rule | Present | Missing | Missing |
| Observability | Missing | Phase 4 mention only | Missing |
| Dry-run mode | Missing | Missing | Phase 3 mention |

---

## 2. Gaps Identified

### GAP-001: No Observability Specification
**Severity:** High
**Present in:** None of the three models
**Problem:** Multi-agent workflows are opaque without structured logging. Debugging failures across 6+ agents across multiple loop iterations is nearly impossible without event traces.

**Solution:** Added T011 (Observability) as a Phase 1 task. Structured JSON event emission for all workflow transitions, overlays, HIL events, and constitution resolution. Secret sanitization pass on all log writes. Phase 4 extends with OpenTelemetry traces and Prometheus metrics.

---

### GAP-002: Evidence Policy Gate Missing from Claude and Gemini
**Severity:** High
**Present in:** Codex only
**Problem:** Both Claude and Gemini allow confidence score to be the sole promotion criterion (or leave it ambiguous). This creates a governance failure mode where high confidence = automatic promotion without evidence.

**Solution:** Added T006 (Evidence Policy Gate) as the overlay that runs *before* confidence loop in the chain. Three risk tiers (T0/T1/T2). T2 always requires HIL. Confidence is explicitly advisory-only in the PRD.

---

### GAP-003: No Secret Handling Specification
**Severity:** High
**Present in:** None of the three models
**Problem:** Agent configs contain API keys and LLM credentials. None of the plans specify how to prevent secrets from leaking into state files, HIL queue items, or observability logs.

**Solution:** Added secret sanitization to the Observability module (T011). The emitter strips secrets before any log write. State file schema excludes credential fields. Added NFR-008 to the PRD.

---

### GAP-004: No Dry-Run Mode
**Severity:** Medium
**Present in:** Gemini (Phase 3 mention), not Claude or Codex
**Problem:** Users cannot validate workflow structure and overlay configuration without triggering LLM calls. This makes iteration on workflow design expensive.

**Solution:** Added `ai-sdd run --dry-run` to T010 (CLI). Prints execution plan (task order, overlay config per task) without dispatching any tasks. Also useful for CI/CD pipeline validation.

---

### GAP-005: No Structured Error Taxonomy
**Severity:** Medium
**Present in:** None of the three models
**Problem:** All three plans mention "fail fast" but none specify a taxonomy of error types. Network errors, LLM errors, validation errors, and state corruption should be handled differently.

**Proposed Solution (Future Task):** Define an error taxonomy:
- `ValidationError`: bad YAML, schema violation → fail fast, no retry
- `AdapterError`: LLM network/quota error → retry with backoff
- `StateError`: state file corruption → pause and alert
- `OverlayError`: overlay logic failure → escalate to HIL
- `CriticalError`: unrecoverable → persist state, exit

**Status:** Defined in T004 implementation notes (rollback/fallback sections) but warrants a dedicated task in Phase 2.

---

### GAP-006: No Schema Versioning Strategy
**Severity:** Medium
**Present in:** None of the three models
**Problem:** When `ai-sdd.yaml`, workflow schema, or state file schema changes in a new release, in-progress workflows using the old schema may break or silently misbehave.

**Proposed Solution:**
- All schemas have a `version` field (already added to state file schema in T004).
- On load, engine checks schema version; if mismatch, either auto-migrate (for minor changes) or fail with a migration guide URL.
- Added to production hardening track (Phase 4).

---

### GAP-007: Reviewer Independence Rule Not Enforced in Codex and Gemini
**Severity:** Low–Medium
**Present in:** Claude only
**Problem:** In a workflow where a paired workflow task is followed by a formal independent review task, assigning the same agent as both challenger (in the pair) and formal reviewer undermines the independence of the review.

**Solution:** Added reviewer independence validation to T008 (Paired Workflow). At workflow load time, if the challenger agent matches the formal review agent for a subsequent task, emit a validation warning. This is a warning (not error) by default; configurable to fail-fast.

---

### GAP-008: No Runtime Adapter for Codex/Gemini in Phase 1
**Severity:** Low
**Present in:** Claude (defers to Phase 2), Codex (defers), Gemini (not specified)
**Problem:** All plans defer non-Claude adapters to later phases. This creates a first-class dependency on Claude Code for Phase 1, limiting the "any LLM" principle.

**Solution:** T010 delivers `MockRuntimeAdapter` (fully functional for tests) and `ClaudeCodeAdapter` in Phase 1. `CodexAdapter` and `GeminiAdapter` are scaffolded in Phase 1 (interface-compliant stubs) and fully implemented in Phase 2.

---

### GAP-009: No Cost/Token Tracking
**Severity:** Low
**Present in:** None (Gemini mentions cost/latency docs but not tracking)
**Problem:** When multiple LLMs are used across many agents and multiple overlay iterations, there is no mechanism to track cost or token usage. Enterprise teams need this for budgeting.

**Proposed Solution:** Add `cost_tracking` to the observability module in Phase 3. Each adapter can optionally report token usage in the `TaskResult`. The emitter aggregates and reports per-workflow cost. Deferred to Phase 3.

---

### GAP-010: No State Migration Spec
**Severity:** Low
**Present in:** None of the three models
**Problem:** If a workflow schema or state file schema changes in a new release, existing in-progress workflows may break silently.

**Solution:** Added to risks table in PLAN.md. State file includes `version` field. Full migration spec deferred to Phase 4 (Production Hardening).

---

## 3. What Was Taken from Each Source

### From ai-sdd-claude
- Full Gherkin acceptance criteria format for all tasks
- Detailed JSON/YAML schema definitions (state file, pair session, ai-sdd.yaml)
- Files-to-create lists per task
- Reviewer independence rule
- Config merge cascade: CLI > project > framework defaults
- Python asyncio for parallel execution
- pydantic for schema validation

### From ai-sdd-codex
- **Evidence Policy Gate** (T006) — critical governance layer absent from other plans
- HIL queue state machine: PENDING → ACKED → RESOLVED / REJECTED
- Evidence-based promotion decision (confidence is advisory only)
- Production hardening roadmap tracks (Reliability, Security, Observability, Governance)
- MVP Gate criteria with concrete observable outcomes
- Rollback/fallback sections per task
- `validate-config` and `hil` as explicit CLI commands
- T0/T1/T2 risk tiers for policy gate
- Advisory confidence routing (confidence influences but cannot solely decide)

### From ai-sdd-gemini
- TypeScript SDK option in Phase 3 (alongside Python)
- Dry-run mode for CLI
- Cost/latency tradeoff documentation requirement
- "Start with all overlays on, selectively disable" default posture guidance
- LLM-as-a-judge as a named eval metric type
- PR checklist as a named example quality metric for agentic review
- Explicit milestone structure with Safety & Evaluation as a distinct phase

### Synthesized (Gaps Addressed)
- **Observability as Phase 1 requirement** (T011) — missing from all three
- Secret sanitization in logs and state files
- Error taxonomy definition (partial — in task notes)
- Schema versioning via `version` field in state files
- `CodexAdapter` and `GeminiAdapter` as Phase 1 stubs

---

## 4. Open Questions

1. **Should the Evidence Policy Gate be required or optional?** Currently optional (off by default). Should T2 workflows require it?
2. **How should the SDK handle overlay composition?** The Python/TypeScript SDK should express overlays as composable wrappers — spec needed for Phase 3.
3. **Multi-project agent registry**: All plans defer this. When should it be addressed?
4. **LLM-as-a-judge**: Who judges the judge? When the llm_judge metric is used, can the same agent judge its own output? Should a separate agent be required?
5. **State migration**: What is the migration path when workflow schema changes? Needs a dedicated policy.
