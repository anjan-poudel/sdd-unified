# ElderAssist AI: Synthesized Prompt Variants

**Synthesized from:** Gemini 3, Claude 4.6, GPT-5.2, DeepSeek v3.1 — all three prompt levels per model
**Date:** 2026-02-25
**Purpose:** Cross-LLM best-of synthesis for Basic, AI-Optimised, and Advanced prompt variants

---

## Synthesis Notes

Each variant takes the best structural and substantive contributions from all four LLMs:

| Contributor | Key strength preserved |
|---|---|
| **Gemini** | Clean domain framing; confidence routing logic; merge/consistency criteria |
| **Claude** | Phase 0 scoping gate; sub-phase granularity (3A–3D); "flag and continue" execution note; voice-as-convenience-factor nuance |
| **GPT-5.2** | North Star + non-goals; evidence-first FACTS/ASSUMPTIONS/DECISIONS/RISKS taxonomy; Gate Results summary; pragmatic voice model caveat |
| **DeepSeek** | Authority boundaries per agent; 6-tier confidence scoring; tiered evidence weights; YAML schemas; 4-level escalation path; power/offline tool gates |

---

---

# VARIANT 1 — BASIC

---

**Role:** You are an expert Software Architect and AI Product Manager.

**Task:** Design a comprehensive system architecture and product specification for an AI Assistant mobile application tailored for elderly users from non-English speaking backgrounds.

---

## Context & Target Audience

- **Users:** Elderly parents who find modern smartphones overwhelming due to language barriers, unfamiliar UI symbolism, cognitive decline (e.g., memory loss), or physical limitations (e.g., trembling hands).
- **Primary Goal:** A frictionless, voice-first, always-on assistant that manages daily routines, health monitoring, communication, and entertainment — without requiring the user to navigate complex app interfaces.
- **Caregiver Role:** Family members must be able to remotely configure the system to remove technical burden from the elderly user.

---

## User Personas

Design for these three representative users:

1. **Elderly parent living alone** — moderate cognitive decline, limited English, relies entirely on family for phone help.
2. **Elderly couple, both low digital confidence** — one member handles the phone; needs joint reminders and shared emergency contacts.
3. **Elderly parent at home during the day, family returns at night** — unsupervised for 8+ hours; health monitoring and proactive reminders are critical.

For each, define: language/dialect, health conditions, daily routine, key assistant use cases, and primary failure mode if the assistant is unavailable.

---

## Core Feature Areas

### 1. Voice-First Interaction
- Full phone control by voice: check calendar, make calls, send messages, ask for help.
- Multilingual support with regional dialect tolerance out of the box.
- Voice personalisation via enrollment samples to adapt to the user's accent and speech pacing.
- **Note:** Prefer speaker adaptation and voice profile approaches over training a custom model unless clearly justified.

### 2. Daily Routine & Reminders
- Proactive, persistent voice + text reminders: wake-up, medication (nagging escalation until acknowledged), meals, exercise, sleep.
- Confirmation flows ("Did you take it?") with missed-dose handling and family notification on failure to respond.
- Google Calendar integration for appointments and important dates.

### 3. Health Monitoring & Emergency Response
- Bidirectional sync with Apple HealthKit and Google Health Connect.
- Threshold-based alerts: when a critical vital (e.g., blood pressure) is breached — (1) confirm with user, (2) if unresponsive or confirmed, call emergency services, (3) notify pre-nominated family contacts in priority order, (4) provide continuous voice reassurance ("Help is on the way").
- All emergency thresholds and contacts configurable by family.

### 4. Communication & Notifications
- Voice-based calls and messages (WhatsApp, SMS, phone).
- Smart notification filtering: read aloud only important messages; silently log the rest.
- Contact aliases supporting native language commands (e.g., "Call my son").

### 5. Entertainment & Scheduled Media
- Scheduled playback: devotional music, yoga videos, news headlines at predefined times.
- On-demand media via voice ("Play bhajans", "Open YouTube").
- Media yields immediately to emergency and medication reminder events.

### 6. Remote Configuration (Critical)
- Family caregiver portal (web + mobile) to push schedules, reminders, emergency contacts, health thresholds, language settings, and media playlists to the device in real time.
- All changes reflected on device within 60 seconds.
- Simplified in-app configuration also available for direct user control.

### 7. Security & Authentication
- Voice biometrics as a **convenience factor** (not the sole authentication method).
- Numeric PIN as mandatory fallback.
- Health and personal data encrypted at rest and in transit.
- Consent model for notification reading and health monitoring.

### 8. Runtime & Reliability
- 24/7 always-on background service.
- Offline-capable for core features (reminders, basic voice commands, emergency).
- Graceful degradation when backend or network is unavailable.

---

## Required Deliverables

Provide a detailed breakdown covering:

1. **System architecture** — mobile client, backend services, AI/ML pipeline, health integrations, caregiver portal
2. **Voice pipeline design** — ASR, NLU, intent classification, TTS; on-device vs. cloud tradeoffs; dialect handling
3. **Emergency response workflow** — full state machine with all states, transitions, and exit conditions
4. **Remote configuration system** — config schema, push mechanism, conflict resolution
5. **Security model** — voice biometrics + PIN fallback + data encryption + caregiver access controls
6. **UX principles** — elderly-specific accessibility, WCAG considerations, no-typing requirement
7. **MVP plan** — 8–12 week scope with phased roadmap
8. **Critical review** — assumptions that might be wrong, where the system could fail, what should be simplified

---

## Output Format

Use headings, bullet points, and concise tables. Be specific and implementation-oriented. Where choices exist, present options with tradeoff analysis. State all assumptions explicitly.

---

---

# VARIANT 2 — AI-OPTIMISED

---

# BUILD SPEC: ElderAssist AI (Agentic Execution Mode)

**Execution Mode:** Sequential phases with acceptance-gated progression
**Orchestration Rule:** Complete all checklist items and meet acceptance criteria before advancing to the next phase. Flag blockers explicitly — do not stall. State assumptions and proceed.

---

## North Star

**Goal:** Enable elderly users (non-English speaking backgrounds) to safely and confidently use a smartphone via voice-first interaction, while reducing caregiver burden through remote configuration and visibility.

**Non-Goals (unless explicitly requested):**
- Fully replacing WhatsApp, Facebook, or YouTube UIs
- Training large custom speech models from scratch
- Diagnosing or treating medical conditions

**Key Design Constraints (non-negotiable):**
- C1: Primary interactions must be completable by voice; UI is fallback only
- C2: Caregiver remote configuration must push changes to device in real time
- C3: Multilingual support required; prefer reuse of existing ASR/TTS over custom training
- C4: UI must be accessible to users with tremors, cognitive decline, and low digital literacy
- C5: System must approximate 24/7 availability; explain how given OS limits
- C6: Emergency calls/notifications must include false-positive mitigation and consent controls

---

## Evidence-First Rule

Separate your outputs into:
- **FACT:** Supported by documented platform behaviour or published evidence
- **ASSUMPTION:** Explicitly stated; flag how it could be validated
- **DECISION:** With rationale and alternatives considered
- **RISK:** With mitigation strategy

Never present an assumption as a fact.

---

## PHASE 0 — Scoping & Constraints

**Objective:** Confirm foundations before any design work begins.

**Steps:**
1. Confirm target platforms: iOS, Android, or both
2. Confirm minimum language and dialect list (specify regional variants, not just language family)
3. Confirm cloud provider preference or agnostic stance
4. Confirm whether on-device inference is required for offline/low-connectivity scenarios
5. Confirm regulatory requirements (HIPAA, GDPR, or local equivalents) based on target geography

**Acceptance Criteria:**
- [ ] Platform targets locked with no ambiguity
- [ ] Language list includes ≥ 3 languages with dialect specificity
- [ ] Cloud + on-device inference strategy decided
- [ ] Compliance scope documented
- [ ] All agents / phases have confirmed scope understanding

---

## PHASE 1 — System Architecture

**Objective:** Produce a complete architecture before any component work begins.

**Steps:**
1. Design high-level architecture covering: mobile client, backend services, AI/ML layer, health integrations, caregiver portal, notification pipeline
2. Define all service boundaries and communication protocols (REST, WebSocket, gRPC)
3. Identify which processing is on-device vs. cloud for each AI component
4. Draft data models for: User, Reminder, HealthMetric, Contact, MediaSchedule, ConfigPayload
5. Document real-time config push mechanism with latency target (≤ 60 seconds end-to-end)

**Checklist:**
- [ ] All major components labelled with clear responsibilities
- [ ] On-device vs. cloud boundary explicit for every AI component
- [ ] All external API integrations listed (HealthKit, Health Connect, Google Calendar, WhatsApp, YouTube)
- [ ] Config push mechanism selected and justified
- [ ] Data models drafted for all core entities

**Acceptance Criteria:**
- [ ] No integration left as "TBD" — each has a named API/SDK and integration approach
- [ ] Single points of failure identified with redundancy plans
- [ ] Offline degradation behaviour defined for every major feature

---

## PHASE 2 — Voice & Language Model Design

**Objective:** Design the personalised voice recognition and NLU pipeline.

**Steps:**
1. Select base multilingual STT model — justify dialect coverage with published WER data
2. Design voice personalisation pipeline: minimum sample requirements, adaptation approach, re-training triggers
3. Design intent classification layer: map utterances → action types
4. Define fallback hierarchy for low recognition confidence: confirm with user → simplified reprompt → PIN fallback
5. Design voice biometric authentication: enrolment, verification threshold, liveness detection, PIN fallback trigger
6. Document supported command taxonomy (minimum 40 intent types at launch)

**Checklist:**
- [ ] STT model selected with dialect coverage documented
- [ ] Voice personalisation pipeline fully specced (inputs → process → outputs)
- [ ] Intent taxonomy documented (≥ 40 intents across all feature areas)
- [ ] Confidence thresholds defined for recognition, authentication, and fallback
- [ ] On-device model size and latency targets defined (e.g., < 2s on mid-range device)
- [ ] Voice biometric enrolment and verification flow step-by-step

**Acceptance Criteria:**
- [ ] Pipeline handles code-switching (e.g., English + Hindi mid-sentence)
- [ ] Authentication flow has no dead ends — every failure resolves to retry or PIN
- [ ] Core commands work offline (reminders, calls, emergency)

---

## PHASE 3A — Daily Routine & Reminder Engine

**Steps:**
1. Design reminder data model: type, schedule, recurrence, escalation rules, acknowledgement states
2. Define escalation logic per reminder type: initial alert → repeat interval → family notification if unacknowledged after X minutes
3. Design delivery mechanism: local notification + voice TTS + screen overlay
4. Define acknowledgement vs. informational-only reminders

**Checklist:**
- [ ] All reminder types listed: wake-up, yoga, medication (×N daily), meals, bedtime, custom
- [ ] Escalation rules defined per type
- [ ] Voice acknowledgement flow designed ("Yes I've taken it" → mark complete)
- [ ] Missed reminder behaviour defined: log, notify family, escalate

**Acceptance Criteria:**
- [ ] Medication reminders cannot be silently dismissed — acknowledgement or family notification is mandatory
- [ ] All reminders remotely configurable with changes reflected within 60 seconds

---

## PHASE 3B — Health Monitoring & Emergency Response

**Steps:**
1. List all monitored health metrics with units and normal/threshold ranges
2. Define HealthKit + Health Connect integration: polling interval, data types, permissions
3. Design threshold configuration schema (per-metric min/max; who can set — family/clinician)
4. Design emergency response as a full state machine:
   - Threshold breached → user confirmation (10 sec) → no response or confirmed → emergency sequence
   - Emergency sequence: call emergency services → notify contacts in priority order → voice reassurance
5. Define retry logic and fallback contacts if initial calls fail
6. Design health summary dashboard for caregiver companion app

**Checklist:**
- [ ] All monitored metrics listed with clinical references for thresholds
- [ ] HealthKit + Health Connect permission and sync flow documented
- [ ] Emergency state machine fully described (all states, transitions, exits)
- [ ] Family notification payload defined
- [ ] Retry and fallback logic documented

**Acceptance Criteria:**
- [ ] Emergency flow executes within 15 seconds of threshold breach to first outbound action
- [ ] User is verbally reassured at each step
- [ ] Emergency flow functional when app is backgrounded or screen is off
- [ ] False-positive mitigation: user confirmation window before triggering

---

## PHASE 3C — Communication

**Steps:**
1. Design voice-to-action flows: "Call [name]", "Message [name] [content]", "Read my messages", "Read my notifications"
2. Define notification importance filter (critical / personal / promotional / system)
3. Design WhatsApp and SMS integration approach
4. Define contact alias system (e.g., "Call my son" → saved contact; supports native language aliases)

**Checklist:**
- [ ] Voice command → action mapping for all communication intents
- [ ] Notification filter rules defined
- [ ] Contact alias system designed
- [ ] TTS voice speed and language configurable per user

**Acceptance Criteria:**
- [ ] User can complete a voice call without touching the screen
- [ ] Notification reading does not interrupt active calls or emergency flows
- [ ] Contact aliases support native language commands

---

## PHASE 3D — Entertainment & Scheduled Media

**Steps:**
1. Design scheduled media system: time-based triggers for music, yoga videos, news
2. Define media source integrations (YouTube API, local files)
3. Design remote playlist management
4. Define voice control during playback (pause, next, volume, stop)
5. Define interruption priority: emergency > medication reminder > media

**Checklist:**
- [ ] All media types listed: music, yoga/exercise video, news briefing, custom
- [ ] YouTube and local playback integration specced
- [ ] Remote playlist configuration flow documented
- [ ] Resume behaviour after interruption defined

**Acceptance Criteria:**
- [ ] Media starts and stops entirely by voice
- [ ] Scheduled media yields immediately to emergency and medication events
- [ ] News briefing sourced from configurable feed and read in user's language

---

## PHASE 4 — Remote Configuration System

**Objective:** Design the caregiver interface and backend that lets family configure the elderly user's app.

**Steps:**
1. Design companion app features: reminder management, contacts, health thresholds, media playlists, language settings
2. Design config schema — versioned and auditable (who changed what, when)
3. Design real-time push pipeline: change → backend → push → device acknowledgement
4. Define conflict resolution if device has pending offline changes when remote config arrives
5. Design activity/health summary view for family

**Acceptance Criteria:**
- [ ] Config push latency ≤ 60 seconds end-to-end
- [ ] Config schema versioned with full audit trail
- [ ] Conflict resolution policy covers all identified edge cases
- [ ] A non-technical family member can configure all core settings within 5 minutes

---

## PHASE 5 — UX & Accessibility

**Steps:**
1. Define UI principles: minimum tap targets (≥ 72px), font sizes, contrast ratios, voice-only operation
2. Design idle/home screen state: what the user sees and hears when nothing is happening
3. Design voice activation: always-listening wake word vs. button press (consider false activation risk)
4. Design for physical limitations: large buttons, tremor/shake tolerance, no complex gestures
5. Design cultural localisation: avoid Western-centric icons, support RTL scripts, culturally appropriate defaults
6. Define onboarding: guided by family member, voice-led, requires zero reading from elderly user

**Acceptance Criteria:**
- [ ] User can complete any core task in ≤ 3 voice commands
- [ ] App fully operable with screen off (voice only)
- [ ] No feature requires the user to type
- [ ] All screens pass WCAG 2.2 AA contrast minimum

---

## PHASE 6 — Security Model

**Steps:**
1. Design voice biometric auth: enrolment, verification, liveness detection, confidence thresholds
2. Design PIN fallback: lockout policy, family reset mechanism
3. Define encryption standards: at rest (device) and in transit (TLS 1.3 minimum)
4. Define repeated failed authentication behaviour
5. Define caregiver access controls: role-based (admin vs. view-only)

**Acceptance Criteria:**
- [ ] Voice auth cannot be bypassed without PIN
- [ ] Health and personal data encrypted at rest and in transit
- [ ] Family members cannot access raw health data without explicit consent configured at setup
- [ ] Compliance requirements (HIPAA/GDPR/local) mapped to specific implementation decisions

---

## PHASE 7 — Tech Stack & Implementation Plan

**Steps:**
1. Recommend full tech stack with justification per layer: mobile, backend, AI/ML, config push, health APIs, media, auth
2. For each AI/ML component: cloud vs. on-device, model size, latency, fallback
3. Flag open-source vs. commercial and licensing considerations
4. Define MVP scope (8–12 weeks): milestones, team roles, backlog
5. Define Phase 2+ roadmap

**Acceptance Criteria:**
- [ ] Every component has a named technology — no TBDs
- [ ] On-device vs. cloud matrix complete for all AI components
- [ ] Stack achievable by team of 3–5 engineers
- [ ] Licensing flags clear

---

## FINAL DELIVERABLE CHECKLIST

Before concluding, confirm all are present:

- [ ] System architecture (all components, boundaries, protocols)
- [ ] Voice pipeline spec with STT model selection and benchmark justification
- [ ] Intent taxonomy (≥ 40 commands)
- [ ] Emergency response state machine
- [ ] Remote config schema and push flow
- [ ] Full tech stack with justifications
- [ ] UX principles and accessibility spec
- [ ] Security model
- [ ] MVP implementation plan (8–12 weeks)
- [ ] Open questions log — decisions requiring human input before build begins
- [ ] Gate Results: PASS / FAIL for each phase

---

**Execution Note:** If a phase cannot be completed due to missing information, list the specific missing inputs, propose reasonable default assumptions clearly labelled as such, and proceed. Do not stall — flag and continue.

---

---

# VARIANT 3 — ADVANCED

---

# AGENTIC BUILD SPEC v4 — ElderAssist AI
## Multi-Agent, Evidence-Gated, Confidence-Routed, Decision-Logged

**Execution Mode:** Multi-agent, evidence-gated, confidence-routed
**Orchestration Principle:** No artifact proceeds without explicit evidence linkage. All assumptions must be logged and risk-rated. Confidence scores below threshold trigger automatic rerouting. Execution never silently propagates low-quality outputs.

---

## NORTH STAR

**Goal:**
- Enable elderly users to safely and confidently use a smartphone via voice-first interaction.
- Reduce caregiver burden through remote configuration and real-time visibility.
- Prioritise safety, privacy, reliability, and accessibility.

**Non-Goals (unless explicitly requested):**
- Fully replacing WhatsApp, Facebook, or YouTube UIs
- Training large custom speech models from scratch
- Diagnosing or treating medical conditions
- Multi-tenant caregiver management (Phase 2+)

**Priority Hierarchy (applied at every conflict):** Safety > Accessibility > Technical Feasibility > Cost

---

## AGENT ROSTER & AUTHORITY MATRIX

| Agent ID | Role | Primary Scope | Authority Boundaries |
|---|---|---|---|
| `ORCH` | Orchestrator | Phase sequencing, gate enforcement, conflict resolution, Decision Log, final merge | May override agent decisions ONLY when Safety > Accessibility conflict; must log rationale. Cannot override hard gates. |
| `ARCH` | Systems Architect | Overall architecture, data models, service boundaries, integration contracts | Cannot define UX patterns; must collaborate with `UX` on interface contracts |
| `ML` | ML/AI Engineer | STT/TTS pipeline, intent classification, voice biometrics, inference strategy | Cannot define security protocols; must collaborate with `SEC` on biometric implementation |
| `HEALTH` | Health & Safety Engineer | HealthKit/Health Connect integration, emergency state machine, threshold logic | Cannot define UX flows; must provide requirements to `UX` for emergency interfaces |
| `UX` | Accessibility & UX Designer | Elderly-focused interface, cultural localisation, WCAG 2.2, onboarding flow | Cannot define technical implementation; provides specs to `ARCH`/`ML` |
| `SEC` | Security Engineer | Auth model, encryption, compliance (HIPAA/GDPR), threat modelling | Cannot override emergency protocols for security; must collaborate with `HEALTH` on balanced approach |
| `CONFIG` | Platform Engineer | Remote configuration system, companion app, push pipeline, audit logging | Cannot define user-facing features; implements configuration delivery only |
| `MEDIA` | Media & Communications Engineer | Entertainment scheduling, WhatsApp/YouTube integration, TTS customisation | Cannot define emergency interruption priorities; must accept `HEALTH` priority rules |
| `QA` | Quality & Acceptance | Evidence package review, confidence auditing, acceptance sign-off | Has veto power on any deliverable with insufficient evidence; cannot define requirements |

**Required Collaborations:**
- Pair reviews: `ML` + `SEC` (biometrics), `HEALTH` + `UX` (emergency interfaces), `ARCH` + `CONFIG` (config architecture)
- Triad sign-offs: Any security-critical health feature requires `HEALTH` + `SEC` + `QA` joint approval
- Conflict escalation: Agent → Pair review → `ORCH` → Human decision point

---

## CONFIDENCE SCORING PROTOCOL

Every agent output must include an explicit confidence declaration:

```
CONFIDENCE: [0–100]
BASIS: [evidence supporting this score]
GAPS: [unknowns or explicit assumptions]
ROUTE: [see table below]
```

| Score | Label | Definition | Routing Action |
|---|---|---|---|
| 95–100 | Verified | Direct evidence from authoritative source, no material assumptions | ✅ Auto-approve; gate check runs |
| 85–94 | High Confidence | Strong evidence; minor assumptions explicitly logged | ✅ Proceed with assumptions logged |
| 75–84 | Medium Confidence | Single strong source; significant assumptions; risk mitigation stated | ⚠️ Conditional proceed; `QA` review required |
| 65–74 | Low Confidence | Weak evidence; major assumptions; high risk | 🔁 Reroute for additional research before resubmission |
| 50–64 | Speculative | Mostly assumption-based; no authoritative source | 🔁 Mandatory reroute; evidence gathering required |
| 0–49 | Unsubstantiated | No credible evidence; critical unknowns | 🚫 Hard stop; `ORCH` escalates to human decision point |

**Confidence Routing Logic:**
- If phase average score ≥ 85: proceed to next phase
- If phase average score < 85 AND iteration count < 3: route critique to responsible agent(s) for mandatory rework
- If iteration count = 3: halt, trigger HIL gate, escalate to human with full iteration history

**Rule:** Confidence scores must never be inflated to pass a gate. `QA` audits all scores ≥ 90 on critical-path items. Any score that cannot be substantiated by cited evidence is downgraded automatically.

---

## EVIDENCE CLASSIFICATION SYSTEM

**Tier 1 (Weight: 10x) — Primary Sources:**
- Official API documentation (Apple HealthKit, Google Health Connect, WhatsApp Business API)
- Published benchmark studies (WER for multilingual STT; FAR/FRR for biometrics)
- Regulatory compliance documents (HIPAA, GDPR, local health data laws)
- Peer-reviewed research on elderly UX, cognitive accessibility, or elderly speech characteristics

**Tier 2 (Weight: 5x) — Secondary Sources:**
- Vendor technical specifications (STT/TTS engine capabilities, latency benchmarks)
- Industry best practice documents (WCAG 2.2, OWASP security frameworks)
- Case studies of comparable deployed systems

**Tier 3 (Weight: 2x) — Supporting:**
- Community documentation, analogous system analysis, logical derivation from first principles

**Tier 4 (Weight: 1x) — Anecdotal:**
- Unverified claims, assumptions pending validation

**Minimum Evidence Requirements per Phase:**

| Phase | Tier 1 Min | Total Min | Special Requirement |
|---|---|---|---|
| 0 — Scoping | 2 | 8 | Must include stakeholder need validation |
| 1 — Architecture | 5 | 20 | Must include scalability and failure mode analysis |
| 2 — Voice/ML | 8 | 25 | Must include model comparison tables and WER data |
| 3A — Reminders | 3 | 12 | Must include elderly cognitive study references |
| 3B — Health/Emergency | 10 | 30 | Must include clinical guideline and legal references |
| 3C — Communications | 4 | 15 | Must include privacy impact assessment |
| 3D — Media | 3 | 10 | Must include bandwidth and offline analysis |
| 4 — Remote Config | 4 | 18 | Must include conflict resolution evidence |
| 5 — UX | 6 | 20 | Must include WCAG 2.2 compliance mapping |
| 6 — Security | 8 | 25 | Must include threat model matrix |
| 7 — Tech Stack | 5 | 18 | Must include license compatibility matrix |

---

## MANDATORY TOOL GATES

| Gate ID | Tool / Process | Triggering Agent | Gate Condition | Failure Impact |
|---|---|---|---|---|
| `TG-01` | API documentation retrieval | `ARCH`, `ML`, `HEALTH` | Before finalising any external API integration claim | Blocks integration design |
| `TG-02` | HealthKit + Health Connect capability verification | `HEALTH` | Before Phase 3B begins | Blocks health feature design |
| `TG-03` | STT model benchmarking (WER, dialect coverage) | `ML` | Before voice pipeline finalisation | Blocks model selection |
| `TG-04` | Regulatory compliance mapping | `SEC` | Before security architecture finalisation | Blocks compliance design |
| `TG-05` | WCAG 2.2 + elderly UX guidelines retrieval | `UX` | Before UX patterns finalised | Blocks interface design |
| `TG-06` | Emergency services API availability per region | `HEALTH` | Before emergency call flow design | Blocks emergency design |
| `TG-07` | Voice biometrics FAR/FRR benchmarking | `ML`, `SEC` | Before authentication design | Blocks auth design |
| `TG-08` | Dependency license audit | `ARCH` | Before tech stack finalisation | Blocks stack selection |
| `TG-09` | OS background task / battery impact analysis | `ML`, `ARCH` | Before background operation design | Blocks runtime design |
| `TG-10` | Offline capability verification per feature | `ARCH` | Before core feature specification | Blocks offline strategy |

**Tool Gate Failure Protocol:**

- **Level 1 (Missing data):** Agent documents search methodology, lists alternatives attempted, proposes assumption with risk rating (Low/Medium/High/Critical). `ORCH` decides: proceed with risk flag, or halt. Execution may continue only if risk ≤ Medium.
- **Level 2 (Conflicting data):** Agent presents all conflicting sources with evidence tier weighting applied. `QA` arbitrates if confidence < 80.
- **Level 3 (No data available):** Immediate halt of affected phase branch. Escalate to human decision point. Log as blocking OQ. Consider architectural pivot if issue is critical.

---

## EVIDENCE PACKAGE SCHEMA

Every phase deliverable must include:

```yaml
phase: "Phase_ID"
agent: "Agent_ID"
deliverable: "Concise description"
confidence:
  score: 0-100
  basis: "Explanation of score"
  tier_breakdown:
    tier1: [count]
    tier2: [count]
    tier3: [count]
    tier4: [count]
evidence:
  - id: "EVID-001"
    type: "api_doc | benchmark | regulation | research | case_study"
    source: "Citation or URL"
    relevance: "How this supports the decision"
assumptions:
  - id: "ASM-001"
    description: "What is being assumed"
    risk: "low | medium | high | critical"
    mitigation: "How risk will be managed"
    validation_plan: "How assumption will be validated"
tool_gates:
  - gate_id: "TG-XX"
    result: "pass | fail | partial"
    notes: "Issues encountered"
gaps:
  - id: "GAP-001"
    description: "What is not known"
    impact: "What decisions this affects"
    blocking: true | false
peer_reviews:
  - reviewer: "Agent_ID"
    confidence: 0-100
    approved: true | false
    comments: "Feedback"
```

---

## EXECUTION FLOW

```
PHASE 0 [ORCH + all agents — scope locked]
    ↓ [MERGE GATE 0]
PHASE 1 [ARCH leads; all agents input — architecture locked]
    ↓ [MERGE GATE 1]
    ┌──────────────────────────────────────────────────────┐
PHASE 2       PHASE 4         PHASE 5         PHASE 6
[ML]         [CONFIG]         [UX]            [SEC]
[Voice/ML]   [Remote Config]  [UX/Access]     [Security]
    └──────────────────────────────────────────────────────┘
    ↓ [all parallel phases merged — dependency handshakes complete]
PHASE 3A → PHASE 3B → PHASE 3C → PHASE 3D   [Sequential — dedicated agents]
    ↓ [MERGE GATE 3]
PHASE 7 [ARCH + all agents; ORCH final merge]
    ↓
FINAL DELIVERABLE PACKAGE
```

**Parallel Phase Rule:** Phases 2, 4, 5, and 6 execute simultaneously after Phase 1 merges. Any cross-phase dependency requires a **dependency handshake**: producing agent declares output ready; consuming agent confirms receipt and compatibility before proceeding.

---

## UNIVERSAL MERGE CRITERIA (All Phases)

- [ ] All agent outputs for the phase are present
- [ ] Every output includes a completed Evidence Package
- [ ] No output has a confidence score < 75
- [ ] All required tool gates for the phase completed with results attached
- [ ] `QA` has reviewed and signed off on acceptance criteria
- [ ] Open Questions Register updated with any new blockers
- [ ] No critical assumption is unlogged
- [ ] Required pair reviews completed; conflicts resolved or escalated
- [ ] Decision Log updated with all major decisions

---

## PHASE-SPECIFIC MERGE CRITERIA (Summary)

| Phase Gate | Key Additional Criteria |
|---|---|
| **Phase 0 → 1** | Platform confirmed; language list specific (not just family — regional variants); compliance jurisdiction mapped |
| **Phase 1 → Parallel** | Service boundaries named (no TBDs); data model co-signed by `ARCH` + `QA`; no circular inter-phase dependencies |
| **Phase 2 → Phase 3** | STT model selected with WER benchmark; intent taxonomy ≥ 40 intents reviewed by `UX`; offline core commands confirmed |
| **Phase 3A–D → Phase 7** | All sub-phases individually signed off; `HEALTH` + `MEDIA` interruption priorities resolved in writing |
| **Phase 4 → Phase 7** | Config push latency ≤ 60s with benchmark evidence; `SEC` reviewed config payload for injection vulnerabilities |
| **Phase 5 → Phase 7** | All screens pass WCAG AA; `UX` + `ML` wake-word conflict resolved; cultural localisation references cited |
| **Phase 6 → Phase 7** | Emergency flow security signed off by `HEALTH` + `SEC`; compliance obligations mapped to specific implementations |
| **Phase 7 Final** | All prior criteria satisfied; full stack named; licensing clear; cost envelope estimated |

---

## CONFLICT RESOLUTION PROTOCOL

When two agents produce conflicting outputs:

1. Both agents state position with supporting evidence
2. `ORCH` identifies decision criteria and applies weighted priority: **Safety > Accessibility > Feasibility > Cost**
3. `ORCH` applies the weighted decision
4. The losing position is logged in the Decision Log with rationale — it is not discarded
5. If `ORCH` confidence < 70, the conflict is escalated as a blocking OQ to a human decision point

---

## OPEN QUESTIONS REGISTER

`ORCH` maintains throughout execution:

```
OQ-[ID] | Phase Raised | Agent | Question | Blocking? | Assumption Used | Risk | Status
```

**Rules:**
- Every gap from every Evidence Package generates an OQ entry
- Blocking OQs halt the relevant phase branch until resolved
- Non-blocking OQs require a stated assumption and risk rating
- All OQs resolved or formally deferred (with owner) before Final Deliverable is issued

---

## ESCALATION PATH

| Level | Trigger | Action |
|---|---|---|
| 1 | Agent-level conflict or low confidence | Agent → Pair review attempt |
| 2 | Pair unresolved after 2 cycles | Pair → `ORCH` mediation |
| 3 | `ORCH` confidence < 70 or blocking OQ | `ORCH` → Human decision point; execution halted on branch |
| 4 | Fundamental feasibility issue | Architecture pivot consideration; full impact analysis required |

---

## FINAL DELIVERABLE PACKAGE

`ORCH` confirms all volumes complete before execution is considered done:

| Volume | Contents |
|---|---|
| **V1: Architecture & Design** | System architecture, data models, API contracts, scalability plan |
| **V2: AI & Voice** | STT/TTS pipeline spec, intent taxonomy (≥ 40 intents), voice biometrics flow, confidence thresholds |
| **V3: Feature Specs** | Reminder engine state machine, emergency response state machine, communication flows, media interruption priority matrix |
| **V4: Platform & Config** | Remote config schema (versioned), push pipeline, companion app spec, audit logging |
| **V5: Security & Compliance** | Security model, compliance mapping, threat model, incident response |
| **V6: UX & Accessibility** | UX principles (WCAG AA evidence), cultural localisation per language, onboarding flow |
| **V7: Implementation Guide** | Tech stack (with licensing + cost), on-device vs. cloud matrix, MVP roadmap (8–12 weeks), test strategy |
| **V8: Governance** | Decision Log, Open Questions Register (all resolved), Assumptions Register (with validation status), Risk Register |

---

**STANDING EXECUTION DIRECTIVE:** Evidence over assumption. Specificity over generality. Surface uncertainty — never paper over it. Produce a specification that an engineering team can build from without returning for clarification on core decisions.
