# Implementation Gap Analysis and Solutions

## Method
Gaps were identified by comparing model plans for completeness, internal consistency, and implementability.

## Gaps

| Gap | Why It Matters | Seen In | Proposed Solution |
|---|---|---|---|
| No formal expression DSL for `exit_conditions` | Ambiguous/unsafe runtime evaluation, inconsistent behavior | All 3 | T010: define grammar, safe evaluator, validation errors, test corpus |
| No typed artifact contract for task I/O | Downstream tasks may consume incompatible outputs | All 3 | T011: versioned artifact schema + compatibility checks |
| No overlay-combination test matrix | Composed overlays can produce non-deterministic routing | All 3 | T012: pairwise/full matrix invariant tests and golden traces |
| Adapter reliability semantics not fully specified | Retry/failure handling differs by provider; resume can break | Gemini/Claude partial, Codex partial | T013: adapter contract with timeout/retry/quota/error mapping |
| Observability baseline not in MVP tasks | Hard to debug runs or prove governance decisions | All 3 (mostly deferred) | T014: structured logs, event schema, trace IDs, cost/latency metrics |
| Security controls not tied to implementation tasks | Prompt injection/data leakage risk | All 3 (mostly deferred) | T015: prompt/output sanitization, secret redaction, policy checks |
| Task catalog inconsistency (duplicate Gemini tasks) | Planning confusion and execution drift | Gemini | Normalize task IDs and maintain one canonical backlog |
| Parallel execution policy lacks resource guardrails | Possible overload/cost spikes in DAG parallelism | All 3 | Add concurrency budgets and queue controls in core engine config |

## Prioritized Remediation
1. T010 Expression DSL (blocks safe loop execution).
2. T011 Artifact contract (blocks reliable handovers).
3. T012 Overlay composition testing (blocks safe advanced modes).
4. T013 Adapter reliability contract (blocks stable real-provider runs).
5. T014 Observability baseline (blocks triage and governance evidence).
6. T015 Security baseline (blocks enterprise readiness).

## Definition of Gap Closure
A gap is closed only when:
1. A spec exists (schema/contract/grammar).
2. Runtime enforcement exists.
3. Tests cover both success and failure paths.
4. Docs include operator-facing troubleshooting guidance.
