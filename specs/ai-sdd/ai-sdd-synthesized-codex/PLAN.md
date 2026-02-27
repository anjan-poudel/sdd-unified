# ai-sdd Synthesized Implementation Plan (Codex)

**Version:** 1.0.0-synthesized
**Date:** 2026-02-27
**Status:** Draft

## 1. Architecture (Best-of)

### 1.1 Core Modules
- `core/engine.py`: orchestration runtime + dependency readiness
- `core/workflow_loader.py`: workflow schema validation + DAG/cycle checks
- `core/agent_loader.py`: agent registry + `extends` inheritance
- `core/state_manager.py`: checkpointing, resume, crash-safe transitions
- `core/context_manager.py`: constitution + handover + artifact context assembly
- `core/hooks.py`: lifecycle hooks for overlay composition
- `constitution/resolver.py`: recursive constitution merge with nearest override precedence
- `eval/scorer.py`: `confidence = f([EvalMetric])`
- `overlays/{hil,confidence,paired,review,policy_gate}`
- `runtime/adapters/{mock,claude,codex,gemini}`
- `cli/main.py`: `run/resume/status/validate-config/hil`

### 1.2 Execution Model
1. Load config and validate schemas.
2. Load agent/workflow definitions and resolve DAG.
3. Resolve constitutions per task path.
4. Execute task via deterministic overlay chain.
5. Persist each transition and evidence artifact.
6. Resume from checkpoint when requested.

### 1.3 Overlay Order (Locked)
1. HIL (default-on)
2. Evidence policy gate
3. Agentic review (optional)
4. Paired workflow (optional)
5. Confidence (optional, advisory)
6. Agent execution

## 2. Operating Rules
1. Every loop requires `max_iterations` and explicit non-iteration exit criteria.
2. Confidence is optional/off by default and cannot promote alone.
3. Promotions require evidence gate pass (tests/lint/security/acceptance/op-readiness).
4. Risk tiers govern autonomy:
- `T0`: low risk, minimal gate
- `T1`: standard gate
- `T2`: strict gate + mandatory human sign-off
5. HIL is default-on with file-queue fallback.

## 3. Phased Delivery

### Phase 1: Core Runtime + Safe Baseline
- T001 Agent system
- T002 Workflow system
- T003 Constitution system
- T004 Core engine/state/hooks
- T005 HIL overlay
- T009 CLI/config/runtime adapter scaffold

### Phase 2: Advanced Overlay Suite
- T006 Confidence overlay (advisory)
- T007 Paired workflow overlay
- T008 Agentic review overlay
- Policy gate integration across T006-T008

### Phase 3: DX + Workflow SDK
- Workflow SDK (Python/TypeScript)
- YAML export/import parity
- Example projects (minimal + high-assurance)

### Phase 4: Hardening Tracks
- Reliability (retry/backoff/idempotency/load)
- Security (secrets/sanitization/supply-chain)
- Observability (logs/traces/metrics/SLOs)
- Governance (audit export/policy packs)

## 4. MVP Exit Criteria
1. End-to-end YAML workflow execution with handovers and bounded loops.
2. Resume from persisted checkpoints after interruption.
3. HIL queue lifecycle works (`list`, `resolve`, `reject`).
4. Evidence-based decisions are logged and auditable.
5. Mock adapter path and at least one real provider path are verified.
6. Config errors fail fast with actionable diagnostics.

## 5. Gap-Driven Additions (New)
The source plans miss several implementation-critical details. Add:
- T010 Expression DSL + safe evaluator for loop/exit conditions.
- T011 Artifact contract + typed task I/O schema versioning.
- T012 Overlay composition matrix and invariant tests.
- T013 Adapter reliability contract (timeouts/retries/error mapping).
- T014 Observability baseline (structured logs/traces/cost metrics).
- T015 Security baseline (prompt/output sanitization + secret handling).
