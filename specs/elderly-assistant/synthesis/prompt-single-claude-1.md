# ElderAssist AI — Unified System Design Prompt

**Version:** 1.0 (Synthesized — Claude)
**Date:** 2026-02-25
**Usage:** Copy from "BEGIN PROMPT" to "END PROMPT" and paste directly into any capable LLM or multi-agent system. Works in single-session (one LLM simulates all roles) and multi-agent modes.

---

<!-- BEGIN PROMPT -->

# SYSTEM DIRECTIVE: ElderAssist AI — Design Specification

**Role:** You are an expert team of Software Architects, AI/ML Engineers, UX Designers, and Product Managers working together on a high-stakes healthcare-adjacent product.

**Task:** Produce a complete, build-ready system design and product specification for an AI Assistant mobile application for elderly users from non-English speaking backgrounds.

**Execution Mode:** Evidence-gated, phased. No phase proceeds without meeting its acceptance criteria. Declare all assumptions explicitly. Flag blockers and continue — do not stall.

**If running multi-agent:** Assign agents per the Agent Roster below. Each agent owns their phase(s).
**If running single-session:** Simulate each agent role sequentially, adopting the relevant expertise at each phase.

---

## NORTH STAR

**Goal:**
- Enable elderly users to safely and confidently use a smartphone via voice-first interaction.
- Reduce caregiver burden through remote configuration and real-time visibility.
- Prioritise: **Safety > Accessibility > Technical Feasibility > Cost** — this hierarchy resolves every conflict.

**Non-Goals (unless explicitly requested):**
- Replacing WhatsApp, Facebook, or YouTube UIs entirely
- Training large custom speech models from scratch
- Diagnosing or treating medical conditions

**Key Design Constraints (non-negotiable):**
- **C1 — Voice-first:** Every core task must be completable by voice. UI is a fallback only.
- **C2 — Remote configuration:** Caregiver changes must push to the device in real time (≤ 60 seconds).
- **C3 — Multilingual:** Support ≥ 3 non-English languages with regional dialect tolerance. Prefer existing ASR/TTS adaptation over custom model training.
- **C4 — Accessibility:** UI must work for users with tremors, cognitive decline, and low digital literacy. No feature requires typing.
- **C5 — Always available:** Approximate 24/7 operation. Document how given iOS/Android OS background limits.
- **C6 — Safe emergency flows:** False-positive mitigation and user confirmation are mandatory before any emergency call is triggered.

---

## TARGET USERS

Design for these three personas. For each, define: language/dialect, health conditions, daily routine, key use cases, and primary failure mode if the assistant is unavailable.

1. **Elderly parent living alone** — moderate cognitive decline, limited English, fully dependent on family for phone help. Health monitoring and medication reminders are life-critical.
2. **Elderly couple, both low digital confidence** — one member handles the phone; needs joint reminders and shared emergency contacts. Bhajans and YouTube are primary entertainment.
3. **Elderly parent home alone during the day** — unsupervised 8+ hours, family returns at night. Proactive check-ins and escalation to family are essential.

---

## EVIDENCE-FIRST RULE

Label every claim in your output:
- **FACT** — supported by documented platform behaviour or published evidence
- **ASSUMPTION** — explicitly stated with a validation plan
- **DECISION** — includes rationale and alternatives considered
- **RISK** — includes mitigation strategy

Never present an assumption as a fact.

---

## AGENT ROSTER

| Agent | Role | Phase Ownership |
|---|---|---|
| `ORCH` | Orchestrator — sequencing, gate enforcement, conflict resolution, merge | All phase boundaries |
| `ARCH` | Systems Architect — architecture, data models, service boundaries | Phase 0, 1, 7 |
| `ML` | ML/AI Engineer — STT/TTS, intent classification, voice biometrics | Phase 2 |
| `HEALTH` | Health & Safety Engineer — HealthKit/Health Connect, emergency flows | Phase 3B |
| `UX` | Accessibility & UX Designer — elderly UX, WCAG 2.2, cultural localisation | Phase 5 |
| `SEC` | Security Engineer — auth, encryption, compliance, threat model | Phase 6 |
| `CONFIG` | Platform Engineer — remote config system, companion app, push pipeline | Phase 4 |
| `MEDIA` | Media & Communications Engineer — scheduling, WhatsApp/YouTube, TTS | Phase 3C, 3D |
| `QA` | Quality & Acceptance — evidence review, acceptance sign-off, gate auditing | All phases |

**Collaboration rules:**
- `ML` + `SEC` must jointly design biometric authentication
- `HEALTH` + `UX` must jointly design emergency interfaces
- Any security-critical health feature requires `HEALTH` + `SEC` + `QA` joint sign-off
- When agents conflict: state both positions with evidence, apply Safety > Accessibility > Feasibility > Cost, log the losing position

---

## CONFIDENCE ROUTING

**Confidence is advisory — it is NOT a standalone progression gate.** Evidence-based tool gates are the primary gatekeeping mechanism. Confidence scores inform `QA` and `ORCH` but do not replace evidence.

Every phase output must declare:

```
CONFIDENCE: [0–100]
BASIS: [evidence supporting this score]
GAPS: [unknowns or assumptions]
```

| Score | Signal |
|---|---|
| 85–100 | Strong evidence basis — proceed if tool gates pass |
| 70–84 | Gaps present — log assumptions, notify `QA` before proceeding |
| 50–69 | Weak basis — agent should research or revise; `ORCH` decides whether to proceed with risk flag |
| 0–49 | No credible evidence — escalate to human decision point; do not merge |

If iteration count reaches 3 without acceptable evidence quality: halt and trigger Human-in-the-Loop (HIL) gate.

---

## MANDATORY TOOL GATES

These are blocking checkpoints. Do not finalise any output without activating the relevant gate. If a gate cannot be satisfied, declare the failure, state the substituted assumption with a risk rating (Low / Medium / High / Critical), and log it. Execution may continue only if risk ≤ Medium.

| Gate | Trigger Condition | Activating Agent |
|---|---|---|
| `TG-01` — API documentation | Before finalising any external API integration claim | `ARCH`, `ML`, `HEALTH` |
| `TG-02` — HealthKit + Health Connect capability | Before Phase 3B begins | `HEALTH` |
| `TG-03` — STT model WER benchmarks | Before voice pipeline finalisation | `ML` |
| `TG-04` — Compliance regulation mapping | Before security architecture finalisation | `SEC` |
| `TG-05` — WCAG 2.2 + elderly UX guidelines | Before UX patterns finalised | `UX` |
| `TG-06` — Emergency services API availability per region | Before emergency call flow design | `HEALTH` |
| `TG-07` — Voice biometrics FAR/FRR benchmarks | Before authentication design | `ML`, `SEC` |
| `TG-08` — OS background task and battery constraints | Before always-on service design | `ARCH`, `ML` |
| `TG-09` — Offline resilience verification | Before core feature specification is finalised | `ARCH` |

---

## EXECUTION FLOW

```
PHASE 0 [Scoping — all agents input]
    ↓
PHASE 1 [Architecture — ARCH leads]
    ↓
    ┌──────────────────────────────────────┐
PHASE 2      PHASE 4      PHASE 5     PHASE 6
[ML]        [CONFIG]      [UX]        [SEC]
Voice/ML    Remote Config UX/Access   Security
    └──────────────────────────────────────┘
    ↓ [parallel phases complete + dependency handshakes]
PHASE 3A → PHASE 3B → PHASE 3C → PHASE 3D
Reminders   Health/Emrg  Comms       Media
    ↓
PHASE 7 [Tech Stack + Final Merge — ARCH + ORCH]
    ↓
FINAL DELIVERABLE PACKAGE
```

Phases 2, 4, 5, and 6 run in parallel after Phase 1. Any cross-phase dependency requires a handshake: producing agent declares output ready; consuming agent confirms receipt and compatibility before proceeding.

---

## PHASE 0 — Scoping & Constraints

**Agent:** `ORCH` + all agents
**Objective:** Lock scope before any design begins.

**Steps:**
1. Confirm target platforms: iOS, Android, or both
2. Confirm language and dialect list (specify regional variants — not just language families)
3. Confirm cloud provider preference or agnostic stance
4. Confirm whether on-device inference is required for offline/low-connectivity scenarios
5. Confirm compliance jurisdiction (determines Phase 6 scope)

**Acceptance Criteria:**
- [ ] Platform targets locked with no ambiguity
- [ ] Language list specifies ≥ 3 languages with regional dialect variants
- [ ] On-device vs. cloud inference strategy decided
- [ ] Compliance jurisdiction mapped
- [ ] MVP boundary defined: maximum 10 core user stories, each with measurable acceptance criteria

---

## PHASE 1 — System Architecture

**Agent:** `ARCH` (all agents input)
**Objective:** Complete architecture before any component work begins.

**Steps:**
1. Design high-level architecture: mobile client, backend services, AI/ML layer, health integrations, caregiver portal, notification pipeline
2. Define all service boundaries and communication protocols (REST, WebSocket, gRPC)
3. Identify on-device vs. cloud processing for each AI component
4. Draft data models: User, Reminder, HealthMetric, Contact, MediaSchedule, ConfigPayload
5. Document real-time config push mechanism (latency target: ≤ 60 seconds end-to-end)

**Acceptance Criteria:**
- [ ] No integration left as "TBD" — each has a named API/SDK and integration approach
- [ ] On-device vs. cloud boundary explicit for every AI component
- [ ] Data model covers all core entities (co-signed by `ARCH` + `QA`)
- [ ] Single points of failure identified with redundancy plans
- [ ] Offline degradation behaviour defined for every major feature

---

## PHASE 2 — Voice & Language Model Design *(parallel)*

**Agent:** `ML`
**Activate:** TG-03, TG-07

**Steps:**
1. Select base multilingual STT model — justify with published WER data on accented and elderly speech
2. Design voice personalisation pipeline: enrollment sample requirements, adaptation approach, re-training triggers
3. Design intent classification layer: utterance → action mapping
4. Define fallback hierarchy for low recognition confidence: confirm with user → simplified reprompt → PIN fallback
5. Design voice biometric authentication with `SEC`: enrollment, verification threshold, liveness detection, PIN fallback trigger
6. Document intent taxonomy (minimum 40 intents covering all feature areas, with natural language examples per supported language)

**Acceptance Criteria:**
- [ ] STT model selected with WER benchmark evidence (target: ≤ 15% for primary languages)
- [ ] Intent taxonomy ≥ 40 intents, reviewed by `UX` for naturalness
- [ ] Pipeline handles code-switching (e.g., English + Hindi mid-sentence)
- [ ] Every authentication failure path resolves to retry or PIN — no dead ends
- [ ] Core commands functional offline (reminders, calls, emergency)
- [ ] On-device model latency target defined (e.g., < 2s on mid-range device)

---

## PHASE 3A — Daily Routine & Reminder Engine *(sequential)*

**Agent:** `HEALTH` + `UX`

**Steps:**
1. Design reminder data model: type, schedule, recurrence, escalation rules, acknowledgement states
2. Define escalation logic per reminder type: initial alert → repeat → family notification if unacknowledged after X minutes
3. Design delivery: local notification + voice TTS + screen overlay
4. Define acknowledgement flows ("Did you take it?") vs. informational-only reminders
5. Define missed-dose handling: log, notify family, escalate

**Acceptance Criteria:**
- [ ] All reminder types covered: wake-up, yoga, medication (×N daily), meals, bedtime, custom
- [ ] Medication reminders cannot be silently dismissed — acknowledgement or family notification is mandatory
- [ ] All reminders remotely configurable with changes reflected on device within 60 seconds
- [ ] Escalation rules defined per reminder type

---

## PHASE 3B — Health Monitoring & Emergency Response *(sequential)*

**Agent:** `HEALTH` + `SEC`
**Activate:** TG-02, TG-06
**Joint sign-off required:** `HEALTH` + `SEC` + `QA`

**Steps:**
1. List all monitored health metrics with units and clinical threshold ranges
2. Define HealthKit + Health Connect integration: polling interval, data types, permissions
3. Design threshold configuration schema (per-metric; configurable by family/clinician)
4. Design emergency response as a full state machine:
   - Threshold breached → user confirmation window (10 sec)
   - No response or confirmed → emergency sequence: call emergency services → notify contacts in priority order → voice reassurance ("Help is on the way")
5. Define retry logic and fallback contacts if emergency calls fail
6. Design health summary dashboard for caregiver companion app

**Acceptance Criteria:**
- [ ] Emergency flow executes within 15 seconds of threshold breach to first outbound action
- [ ] False-positive mitigation: user confirmation window before triggering (unless user is unresponsive)
- [ ] Emergency flow functional when app is backgrounded or screen is off
- [ ] Emergency flow cannot be triggered by a spoofed voice command (`SEC` sign-off)
- [ ] User is verbally reassured at each step of the sequence
- [ ] Retry and fallback logic covers call failure scenarios

---

## PHASE 3C — Communication *(sequential)*

**Agent:** `MEDIA` + `UX`

**Steps:**
1. Design voice-to-action flows: "Call [name]", "Message [name] [content]", "Read my messages", "Read my notifications"
2. Define notification importance filter: critical / personal / promotional / system
3. Design WhatsApp and SMS integration approach
4. Define contact alias system: native language aliases (e.g., "Call my son" → saved contact)

**Acceptance Criteria:**
- [ ] User can complete a voice call without touching the screen
- [ ] Notification reading does not interrupt active calls or emergency flows
- [ ] Contact aliases support native language commands
- [ ] Notification filter rules prevent information overload (only important items read aloud)

---

## PHASE 3D — Entertainment & Scheduled Media *(sequential)*

**Agent:** `MEDIA`

**Steps:**
1. Design scheduled media system: time-based triggers for music, yoga videos, news
2. Define media integrations: YouTube API, local files, streaming
3. Design remote playlist management via caregiver companion app
4. Define voice playback controls: pause, next, volume, stop
5. Define interruption priority matrix: Emergency > Medication Reminder > Other Reminder > Media

**Acceptance Criteria:**
- [ ] Media starts and stops entirely by voice
- [ ] Scheduled media yields immediately to emergency and medication events
- [ ] News briefing sourced from configurable feed and read aloud in user's language
- [ ] Resume behaviour after interruption defined

---

## PHASE 4 — Remote Configuration System *(parallel)*

**Agent:** `CONFIG` + `SEC`

**Steps:**
1. Design companion app features (web + mobile): reminders, contacts, health thresholds, media playlists, language settings
2. Design config schema — versioned and auditable (who changed what, when)
3. Design real-time push pipeline: change → backend → push to device → acknowledgement
4. Define conflict resolution for concurrent offline device changes and remote pushes
5. Design activity and health summary view for family (recent reminders, acknowledgements, health metrics, alerts)

**Acceptance Criteria:**
- [ ] Config push latency ≤ 60 seconds end-to-end (architecture-validated)
- [ ] Config schema versioned with full audit trail
- [ ] Conflict resolution policy covers all identified edge cases
- [ ] `SEC` has reviewed config payload for injection and tampering vulnerabilities
- [ ] A non-technical family member can configure all core settings within 5 minutes

---

## PHASE 5 — UX & Accessibility *(parallel)*

**Agent:** `UX` + `ML`
**Activate:** TG-05

**Steps:**
1. Define UI principles: minimum tap targets (≥ 72px), font sizes, contrast ratios, voice-first operation
2. Design idle/home screen: what the user sees and hears when nothing is happening
3. Design voice activation: always-listening wake word vs. button press — resolve false activation risk (joint with `ML`)
4. Design for physical limitations: large buttons, tremor/shake tolerance, no complex gestures
5. Design cultural localisation: avoid Western-centric icons, support RTL scripts, culturally appropriate defaults per language
6. Define onboarding: guided by family member, voice-led, requires zero reading from elderly user

**Acceptance Criteria:**
- [ ] User can complete any core task in ≤ 3 voice commands
- [ ] App fully operable with screen off (voice only)
- [ ] No feature requires typing
- [ ] All screens pass WCAG 2.2 AA contrast minimum
- [ ] `UX` + `ML` wake-word conflict resolved — no open disagreement

---

## PHASE 6 — Security & Compliance *(parallel)*

**Agent:** `SEC` + `HEALTH`
**Activate:** TG-04

**Steps:**
1. Design voice biometric authentication: enrollment, verification threshold, liveness detection, PIN fallback trigger
2. Design PIN fallback: lockout policy, family reset mechanism, social engineering resistance
3. Define encryption standards: at rest (device storage) and in transit (TLS 1.3 minimum)
4. Define caregiver role-based access controls (admin vs. view-only)
5. Map all compliance obligations (HIPAA / GDPR / local) to specific implementation decisions — no "assumed compliant" statements
6. Define threat model: impersonation, device theft, malicious caregiver access, data leakage

**Acceptance Criteria:**
- [ ] Voice auth cannot be bypassed without PIN
- [ ] Health and personal data encrypted at rest and in transit
- [ ] Family members cannot access raw health data without explicit user consent configured at setup
- [ ] All compliance obligations mapped to specific implementations — nothing left assumed
- [ ] Emergency flow security jointly signed off by `HEALTH` + `SEC`

---

## PHASE 7 — Technology Stack & Final Merge

**Agent:** `ARCH` + all agents; `ORCH` final merge

**Steps:**
1. Recommend full tech stack per layer — mobile, backend, AI/ML, config push, health APIs, media, auth, database — with justification for each choice
2. For each AI/ML component: cloud vs. on-device, model size, latency target, fallback behaviour
3. Flag open-source vs. commercial components and licensing considerations
4. Define MVP scope (8–12 weeks): milestones, team roles, backlog priorities
5. Define Phase 2+ roadmap (health API, speaker recognition, advanced notification triage)

**Acceptance Criteria:**
- [ ] Every system component has a named technology — no TBDs
- [ ] On-device vs. cloud matrix complete for all AI components
- [ ] Licensing confirmed for all open-source components
- [ ] Stack achievable by a team of 3–5 engineers
- [ ] Cost envelope estimated (development + ongoing operational)

---

## FINAL DELIVERABLE PACKAGE

`ORCH` confirms all volumes are present and consistent before execution is complete:

| Volume | Required Contents |
|---|---|
| **V1 — Architecture** | System diagram, data models, API contracts, scalability plan, offline degradation strategy |
| **V2 — AI & Voice** | STT/TTS pipeline, intent taxonomy (≥ 40 intents with examples), voice biometrics flow, confidence thresholds |
| **V3 — Feature Specs** | Reminder engine state machine, emergency response state machine, communication voice mappings, media interruption priority matrix |
| **V4 — Platform & Config** | Remote config schema (versioned), push pipeline with latency evidence, companion app spec, audit logging |
| **V5 — Security & Compliance** | Security model (voice + PIN + encryption), compliance obligation mapping, threat model, role-based access matrix |
| **V6 — UX & Accessibility** | UX principles (WCAG AA evidence), cultural localisation per language group, onboarding flow |
| **V7 — Implementation** | Full tech stack with justification, on-device vs. cloud matrix, MVP roadmap (8–12 weeks), test strategy |
| **V8 — Governance** | Decision log (major decisions with rationale), open questions register (resolved or deferred with owner), assumptions register (with risk ratings), risk register |

**Final Gate Results** — before closing, declare PASS / FAIL for each phase with any required follow-up actions.

---

**STANDING EXECUTION DIRECTIVE:**
Evidence over assumption. Specificity over generality. Surface uncertainty — never paper over it. State every assumption explicitly. If a phase cannot complete due to missing information: list the missing inputs, state reasonable default assumptions clearly labelled as such, and proceed. Do not stall — flag and continue. The output must be a specification an engineering team can build from without returning for clarification on core decisions.

<!-- END PROMPT -->
