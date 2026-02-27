# ai-sdd Roadmap

## Milestones
| Milestone | Outcome | Task Groups |
|---|---|---|
| M1 Core Runtime | End-to-end YAML pipeline works | A, B, C, D |
| M2 Safe Gates | HIL + evidence policy gate active | E |
| M3 Overlay Modes | Confidence/paired/review loops operational | F |
| M4 Usability | CLI + config + adapters usable | G |
| M5 MVP Demo | Repeatable demo with docs and artifacts | H |
| M6 Production Hardening | Reliability/security/observability uplift | hardening tracks |

## Task Groups

### A. Agent Foundation
- YAML schema, default agents, inheritance
- Exit: agent load/override validated

### B. Workflow Foundation
- DAG schema/loader, cycle detection, loop config
- Exit: topological execution and loop guards verified

### C. Constitution Resolution
- Recursive merge and override precedence
- Exit: deterministic merged context

### D. Core Engine + State
- Dispatch, hooks, persistence, resume
- Exit: resumable workflow with consistent transitions

### E. Safety + Governance
- HIL default-on
- Evidence-based policy gate
- Requirement coverage optional+tunable
- Risk-tier routing T0/T1/T2

### F. Overlay Capabilities
- Confidence overlay (advisory)
- Paired workflow
- Agentic review
- Exit: deterministic composition and bounded loops

### G. CLI + Config DX
- run/resume/validate/hil commands
- Config discovery/merge/validation

### H. Demo + Verification
- Demo workflow, sequence docs, runbook, expected artifacts

## MVP Gate
MVP is ready when groups A-H complete and one reference run demonstrates:
- multi-agent handovers
- bounded loops
- evidence-based routing decisions
- HIL fallback with file queue

## Production Hardening Tracks
1. Reliability: retries/backoff/idempotency/load tests
2. Security: secret policy/sanitization/supply-chain scan
3. Observability: logs/traces/metrics/SLO alerts
4. Runtime integration: timeout/quota/fallback behavior
5. Governance: audit exports and policy packs
