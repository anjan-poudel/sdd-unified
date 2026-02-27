# Plan Comparison Across Models

## Scope Compared
Compared `PLAN.md`, `ROADMAP(.md/.yaml)`, `PRD.md`, and task definitions from Claude, Gemini, and Codex plans.

## Side-by-Side Assessment

| Dimension | Claude | Gemini | Codex | Best Extracted |
|---|---|---|---|---|
| Architectural specificity | Very strong (module tree, schema examples, overlay stack) | Medium (conceptual) | Strong (concise module map + execution model) | Claude + Codex |
| Task definition quality | Very strong (gherkin acceptance, files, tests) | Mixed (duplicate task sets, broad wording) | Strong (clean DoD/test strategy/fallback) | Claude + Codex |
| Governance/safety clarity | Strong (policy gate, risk tiers in roadmap) | Medium (HIL + confidence focus) | Very strong (explicit evidence gate + non-promotion rule) | Codex |
| Delivery planning depth | Very strong (effort, critical path, milestone estimates) | Medium (phased but high-level) | Strong (clear milestones/groups) | Claude + Codex |
| Operability/production hardening | Strong (reliability/security/observability tracks) | Weak-Medium | Strong (tracks + risk controls) | Claude + Codex |
| Simplicity/onboarding | Medium | Very strong (clear, minimal framing) | Strong | Gemini + Codex |
| Consistency | High | Low (duplicate/overlapping task files) | High | Codex |

## Strengths To Preserve
1. Claude: detailed acceptance criteria and implementation/test depth.
2. Claude: effort model and critical-path thinking.
3. Codex: explicit evidence policy gate and risk-tier routing guardrails.
4. Codex: practical CLI/config/runtime adapter framing.
5. Gemini: clear phased narrative and simplicity for adoption.
6. Gemini: explicit cost/latency tradeoff framing.

## Weaknesses To Avoid
1. Gemini task duplication (`task-001..005` and `task-01..05`) creating ambiguity.
2. Confidence-as-gate ambiguity (must remain advisory/evidence-backed).
3. Missing explicit overlay-composition test matrix in all three plans.
4. Missing concrete expression-language spec for loop/exit conditions.
5. Missing strict artifact contract (task I/O schema + versioning).
