# Elderly Assistant Prompt Synthesis (Unified)

## Scope Reviewed
Reviewed prompt variants across:
- `specs/elderly-assistant/claude/*`
- `specs/elderly-assistant/codex/*`
- `specs/elderly-assistant/deepseek/*`
- `specs/elderly-assistant/gemini/*`
- supporting synthesis files in `specs/elderly-assistant/*.md`

## What Worked Best Across LLM Styles
1. Clear role + objective framing at the top.
2. Strong structure with explicit sections/artifacts.
3. Sequential execution steps to avoid drift.
4. Acceptance criteria/checklists per phase.
5. Explicit treatment of mobile constraints (iOS/Android background limits).
6. Safety-first emergency design with consent and false-positive mitigation.
7. Strong caregiver remote-config requirements.
8. Explicit fact vs assumption separation.
9. Evidence/logging requirements for critical decisions.
10. A critic/review pass before final output.

## Common Weaknesses Observed
1. Some prompts were long but under-specified on output format.
2. Some over-indexed on confidence routing without enough evidence gating.
3. Inconsistent artifact naming and phase boundaries.
4. Limited explicit MVP scoping guardrails.
5. Some claims risked platform infeasibility without verification gates.

## Synthesis Principles Used
- Keep confidence as advisory, not standalone gate.
- Use evidence-based gates for progression.
- Keep prompts reusable across Claude/GPT/Gemini/DeepSeek.
- Constrain output shape for predictable quality.

---

## 1) Refined Prompt — Basic

```md
Role: You are an expert AI Product Architect and Mobile Systems Designer.

Task: Design an implementation-oriented system specification for an AI Assistant mobile app for elderly users from non-English speaking backgrounds.

Context:
- Users struggle with smartphone UI due to language, cognitive decline, and motor challenges.
- They still need voice-first access to routines, communication, health-related safety flows, and entertainment.
- Family/caregivers must be able to remotely configure the system.

Must-Have Features:
1. Voice-first interaction for reminders, calls, messages, phone guidance, and calendar queries.
2. Daily routine engine: medication (persistent reminders), meals, exercise/yoga, sleep.
3. Communication: voice calling/messaging and important notification readout.
4. Entertainment automation: scheduled music/news/yoga video.
5. Health integration: Apple HealthKit + Google Health Connect (where supported).
6. Emergency flow: detect threshold breach, confirm safely, notify contacts, escalate appropriately.
7. Caregiver remote configuration portal + on-device simplified settings.

Constraints:
- Must account for iOS/Android background execution limits.
- Must support multilingual + dialect tolerance.
- Voice is convenience auth factor; fallback PIN required.
- Define offline/degraded behavior for core tasks.

Required Output:
1. Problem statement and user personas.
2. Functional and non-functional requirements.
3. High-level architecture (mobile, backend, AI pipeline, integrations).
4. Key data flows (reminder, health alert, emergency, config sync).
5. Security/privacy model and consent model.
6. MVP scope (8–12 weeks) and phase roadmap.
7. Risks, assumptions, and open questions.

Output Style:
- Use clear headings, tables, and concise implementation detail.
- Separate facts from assumptions.
```

---

## 2) Refined Prompt — AI-Optimized (Structured Agentic)

```md
SYSTEM DIRECTIVE
You are producing a build-ready Product + System Design package for an elderly-focused, voice-first mobile assistant.

Execution Rules:
- Work sequentially through phases.
- Do not skip sections.
- Each phase must end with a checklist and acceptance criteria.
- Clearly mark FACTS, ASSUMPTIONS, and DECISIONS.

PHASE 0 — Scope Lock
Deliver:
- Target platforms (iOS/Android/both)
- Supported languages/dialects (minimum 3)
- Compliance scope by region
- MVP boundary (max 10 core stories)
Acceptance:
- [ ] Scope is unambiguous
- [ ] MVP stories are measurable

PHASE 1 — Users and Requirements
Deliver:
- 3–5 personas
- 6–10 primary user journeys
- Functional and non-functional requirements with IDs
Acceptance:
- [ ] Each requirement has measurable acceptance criteria

PHASE 2 — Architecture and Data Flows
Deliver:
- Component architecture (mobile, backend, voice, integrations, caregiver portal)
- On-device vs cloud split
- Data flows: reminders, communication, emergency, config push
Acceptance:
- [ ] No critical interface is left TBD
- [ ] Offline/degraded behavior is specified

PHASE 3 — Voice, UX, and Safety
Deliver:
- STT/TTS/NLU design and dialect strategy
- Accessibility UX rules for elderly users
- Emergency state machine with false-positive mitigation
Acceptance:
- [ ] Core flows are operable by voice
- [ ] Risky actions have confirmation policy

PHASE 4 — Security and Privacy
Deliver:
- Threat model
- Auth model (caregiver + elderly user)
- Encryption and audit logging
- Consent and data minimization policy
Acceptance:
- [ ] Health/personal data protections are explicit
- [ ] Abuse scenarios and mitigations are listed

PHASE 5 — Delivery Plan
Deliver:
- 8–12 week MVP plan with milestones
- Test strategy (unit/integration/e2e/accessibility/reliability)
- Risk register and validation plan
Acceptance:
- [ ] Every MVP story maps to tests
- [ ] Top risks have mitigations and owners

Final Output Format:
- A1 Product Definition
- A2 Personas & Journeys
- A3 Requirements
- A4 Architecture
- A5 Safety & Emergency
- A6 Security & Privacy
- A7 MVP Plan
- A8 Test Strategy
- A9 Risk Register
- A10 Open Questions & Assumptions
```

---

## 3) Refined Prompt — Advanced (Evidence-Gated Multi-Agent)

```md
AUTONOMOUS MULTI-AGENT DIRECTIVE
Design a build-ready specification for an elderly voice-first assistant app.

Operating Model:
- Multi-agent collaboration with orchestrator.
- Evidence-based progression gates.
- Confidence is advisory only (not standalone merge/promotion gate).
- Critical unknowns must block or be explicitly risk-accepted.

Agent Roles:
- ORCH: sequencing, gate enforcement, conflict resolution, final merge
- ARCH: architecture, service boundaries, data models
- ML: STT/TTS/NLU, personalization, confidence calibration
- HEALTH: health integrations + emergency safety logic
- UX: accessibility + localization + onboarding
- SEC: auth/privacy/compliance/threat model
- CONFIG: remote config and audit pipeline
- QA: acceptance checks, evidence validation, red-team review
- CRITIC: adversarial failure-mode review and simplification

Mandatory Evidence Package (per major artifact):
- Decision summary
- Evidence sources (API docs/benchmarks/regulations/research)
- Assumptions with risk rating
- Alternatives considered and rejected
- Residual risks and validation plan

Tool Gates (must pass before merge):
- TG-1 Platform feasibility: iOS/Android background/runtime constraints verified
- TG-2 Health API feasibility: HealthKit/Health Connect capabilities and limits verified
- TG-3 Safety gate: emergency flow includes consent, false-positive mitigation, rate limits
- TG-4 Security/compliance: data handling mapped to HIPAA/GDPR/local obligations
- TG-5 Accessibility gate: WCAG + elderly UX standards mapped to design decisions
- TG-6 Offline resilience: degraded-mode behavior defined for all MVP-critical flows

Merge Criteria (Evidence-Based):
- Requirement coverage mapping (optional/tunable strictness)
- Acceptance evidence quality (BDD or equivalent testability)
- Verification readiness (test/lint/security plans for implementable scope)
- Operational readiness evidence (logging, alerting, auditability)
- Risk-tier routing:
  - T0: lightweight review
  - T1: standard review
  - T2: strict review + human sign-off

Execution Phases:
1. Scope and assumptions lock
2. Requirements + personas + journeys
3. Architecture + integration contracts + data models
4. Voice/UX design + safety flows
5. Security/privacy/compliance design
6. MVP plan + QA strategy + risk register
7. Critic pass + gate report + final merge package

Required Final Deliverables:
- D1 PRD
- D2 Architecture Spec
- D3 Safety/Emergency Spec
- D4 Security/Privacy Spec
- D5 MVP Plan + Roadmap
- D6 Test/Validation Strategy
- D7 Risk Register + Open Questions
- D8 Gate Results Report (PASS/FAIL + remediation)

Hard Rules:
- Do not present assumptions as facts.
- Do not use confidence percentage as a standalone gate.
- Block progression when critical tool gates fail.
```

---

## Recommended Use
- Use **Basic** for fast ideation and one-shot design.
- Use **AI-Optimized** for reliable structured outputs from general LLM runs.
- Use **Advanced** for agentic workflows, governance-heavy environments, or high-stakes planning.
