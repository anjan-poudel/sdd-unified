# ai-sdd: Synthesized Roadmap

**Version:** 0.1.0-synthesized
**Date:** 2026-02-27

---

## Milestones

| Milestone | Outcome | Task Groups |
|---|---|---|
| **M1 Agent + Workflow Foundation** | YAML agent/workflow schemas load and validate | A, B |
| **M2 Core Engine** | End-to-end YAML pipeline executes and resumes | C, D |
| **M3 Safety Layer** | HIL default-ON; evidence policy gate active | E |
| **M4 Overlay Suite** | Confidence/paired/review loops operational and composable | F |
| **M5 CLI + DX** | CLI run/resume/status/validate-config/hil usable | G |
| **M6 MVP Demo** | Repeatable demo with docs and expected artifacts | H |
| **M7 Workflow SDK** | Python + TypeScript programmatic workflow definitions | I |
| **M8 Production Hardening** | Reliability, security, observability, governance | J |

---

## Task Groups

### A. Agent Foundation
- YAML schema, default agents (BA, Architect, PE, LE, DEV, Reviewer), inheritance
- Exit: agent load/override validated; schema violations fail fast

### B. Workflow Foundation
- DAG schema/loader, cycle detection, loop config, parallel task eligibility
- Exit: topological execution and loop guards verified

### C. Constitution Resolution
- Recursive merge (framework → root → sub-module), override precedence
- Exit: deterministic merged context with clear resolution order

### D. Core Engine + State
- Dispatch loop, hook lifecycle, persistence, resume, asyncio parallelism, RuntimeAdapter
- Exit: resumable workflow with consistent state transitions; mock adapter functional

### E. Safety + Governance
- HIL default-ON (file-based queue, PENDING/ACKED/RESOLVED/REJECTED lifecycle)
- Evidence-based policy gate (acceptance + verification + readiness evidence)
- Risk-tier routing T0 (lightweight) / T1 (standard) / T2 (strict + human sign-off)
- Requirement coverage optional and tunable

### F. Overlay Suite
- Confidence overlay (advisory only — does not bypass evidence gate)
- Paired workflow (driver/challenger, role-switch policies, pair session history)
- Agentic review (coder/reviewer, GO/NO_GO, auditable decisions)
- Overlay composition: correct behaviour when multiple overlays active simultaneously

### G. CLI + Config DX
- `run`, `resume`, `status`, `validate-config`, `hil` commands
- Config discovery, merge order, schema validation on startup
- `ai-sdd.yaml` project config schema

### H. MVP Demo + Verification
- Reference demo workflow (multi-agent handover with review)
- Expected artifacts documented
- Runbook for reproducing the demo

### I. Workflow SDK
- Python fluent API for workflow definitions
- TypeScript API for Node/TS consumers
- SDK → YAML export for engine execution
- Dry-run mode (validate without executing)
- Reference example projects (simple linear + high-assurance paired)
- Cost/latency tradeoff documentation

### J. Production Hardening
1. **Reliability**: Retries with backoff, idempotency, load tests
2. **Security**: Secret sanitization in state/logs, supply-chain scan
3. **Observability**: Structured logs, distributed traces, task duration metrics, SLO alerts
4. **Runtime Integration**: LLM timeout/quota, provider fallback behaviour
5. **Governance**: Audit export (promotion decisions + evidence), policy packs

---

## MVP Gate

MVP is ready when groups A–H complete and a reference run demonstrates:
- Multi-agent handovers (at least BA → Architect → PE)
- Bounded loops (paired + review overlay with MAX_ITERATION)
- Evidence-based routing decisions (T1 policy gate pass/fail)
- HIL fallback with file queue (loop exhaustion escalation scenario)

---

## Phase Summary

| Phase | Milestones | Description |
|---|---|---|
| Phase 1 — Core Engine | M1–M3, M5 | Working pipeline with safety layer |
| Phase 2 — Overlays | M4 | Full overlay suite, composable |
| Phase 3 — SDK | M6–M7 | SDK, examples, MVP demo |
| Phase 4 — Hardening | M8 | Enterprise production readiness |
