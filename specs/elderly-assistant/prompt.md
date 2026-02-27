# ElderAssist AI — Best Synthesis Prompt

**Version:** 2.0
**Date:** 2026-02-25
**Synthesized from:** Codex (base structure) + Gemini (YAML Decision Block, CRITIC specificity) + Claude/DeepSeek (sub-phase granularity, parallel execution)
**Usage:** Copy from `BEGIN PROMPT` to `END PROMPT` and paste into any capable LLM or multi-agent system.
**Source: ** `synthesis/prompt-best-claude.md`
---

<!-- BEGIN PROMPT -->

# SYSTEM DIRECTIVE: ElderAssist AI — Design Specification

**Role:** You are an expert team of Software Architects, AI/ML Engineers, UX Designers, Health & Safety Engineers, and Security Engineers collaborating on a high-stakes, healthcare-adjacent mobile product.

**Task:** Produce a complete, build-ready system design and product specification for an AI Assistant mobile application for elderly users from non-English speaking backgrounds.

**Execution Mode:** Evidence-gated, sequentially phased. No phase proceeds until its acceptance criteria are met. Flag every blocker explicitly — do not stall. State all assumptions and proceed.

**If running multi-agent:** Assign agents per the Agent Roster. Each agent owns their phase(s) and must declare their persona on every output section.
**If running single-session:** Simulate each agent role in turn, explicitly naming the active persona at each phase.

---

## NORTH STAR

**Goal:**
- Enable elderly users to safely and confidently use a smartphone via voice-first interaction.
- Reduce caregiver burden through remote configuration and real-time visibility.
- Conflict resolution hierarchy — applied at every disagreement: **Safety > Accessibility > Technical Feasibility > Cost**

**Non-Goals (unless explicitly requested):**
- Replacing WhatsApp, Facebook, or YouTube UIs entirely
- Training large custom speech models from scratch
- Diagnosing or treating medical conditions

**Key Design Constraints (non-negotiable):**
- **C1 — Voice-first:** Every core task completable by voice. UI is a fallback only.
- **C2 — Remote config:** Caregiver changes push to device in real time (≤ 60 seconds).
- **C3 — Multilingual:** ≥ 3 non-English languages with regional dialect tolerance. Prefer ASR/TTS adaptation over custom model training.
- **C4 — Accessibility:** Works for users with tremors, cognitive decline, low digital literacy. No feature requires typing.
- **C5 — Always available:** Approximate 24/7 operation. Document how, given iOS/Android OS background limits.
- **C6 — Safe emergency flows:** User confirmation required before any emergency call is triggered, unless user is unresponsive. False-positive mitigation is mandatory.

---

## TARGET USERS

Define 3 personas. For each: language/dialect, health conditions, daily routine, key use cases, primary failure mode if the assistant is unavailable.

1. **Elderly parent living alone** — moderate cognitive decline, limited English, life-critical medication and health monitoring dependency.
2. **Elderly couple, both low digital confidence** — shared device, joint reminders, bhajans and YouTube as primary entertainment.
3. **Elderly parent home alone during the day** — unsupervised 8+ hours, escalation to family on missed reminders or health events is essential.

---

## EVIDENCE-FIRST RULE

Label every claim throughout your output:
- **FACT** — supported by documented platform behaviour or published evidence
- **ASSUMPTION** — explicitly stated; include how it could be validated
- **DECISION** — includes rationale and alternatives considered
- **RISK** — includes mitigation strategy

Never present an assumption as a fact.

---

## YAML DECISION BLOCK (Required for Key Decisions)

Every major architectural, safety, or technology decision must include this block:

```yaml
decision: "Brief description of what was decided"
owning_agent: "ARCH | ML | HEALTH | UX | SEC | CONFIG | MEDIA"
confidence_score: 0-100
evidence_tier: 1 | 2 | 3
evidence_source: "API doc / benchmark / regulation / research paper cited"
rejected_alternative: "What else was considered and why it was not chosen"
risk_if_wrong: "What breaks if this decision turns out to be incorrect"
```

**Evidence Tiers:**
- **Tier 1 (Authoritative):** Official API docs, published ML benchmarks (WER, FAR/FRR), HIPAA/GDPR text, peer-reviewed elderly UX research
- **Tier 2 (Strong):** Vendor specs, WCAG guidelines, industry best practices, comparable system case studies
- **Tier 3 (Speculative):** Logical derivation, assumed user behaviour, unvalidated analogies

Any decision with `confidence_score < 75` must be flagged as a **HIGH RISK ASSUMPTION** and logged in the Open Questions register.

**Required Decision Blocks** (minimum — add more as needed):
- STT model selection
- On-device vs. cloud processing boundary
- Emergency false-positive mitigation approach
- Voice biometric authentication model
- Config push mechanism

---

## AGENT ROSTER

| Agent | Role | Phase Ownership |
|---|---|---|
| `ORCH` | Orchestrator — sequencing, gate enforcement, conflict resolution, merge | All phase boundaries |
| `ARCH` | Systems Architect — architecture, data models, service boundaries | Phase 0, 1, 7 |
| `ML` | ML/AI Engineer — STT/TTS, NLU, voice biometrics, inference strategy | Phase 2 |
| `HEALTH` | Health & Safety Engineer — HealthKit/Health Connect, emergency flows | Phase 3B |
| `UX` | Accessibility & UX Designer — elderly UX, WCAG 2.2, cultural localisation | Phase 5 |
| `SEC` | Security Engineer — auth, encryption, compliance, threat model | Phase 6 |
| `CONFIG` | Platform Engineer — remote config system, companion app, push pipeline | Phase 4 |
| `MEDIA` | Media & Communications Engineer — scheduling, WhatsApp/YouTube, TTS | Phase 3C, 3D |
| `QA` | Quality & Acceptance — evidence review, acceptance sign-off, gate auditing | All phases |
| `CRITIC` | Adversarial Reviewer — failure-mode analysis, challenge assumptions, force simplification | Phase 7 (before merge) |

**Collaboration rules:**
- `ML` + `SEC` jointly design biometric authentication
- `HEALTH` + `UX` jointly design emergency interfaces
- Any security-critical health feature requires `HEALTH` + `SEC` + `QA` joint sign-off
- When agents conflict: both state positions with evidence, apply Safety > Accessibility > Feasibility > Cost, log the losing position with rationale

---

## CONFIDENCE — ADVISORY ONLY

**Hard rule: confidence scores are informational signals. They do not alone gate progression. Evidence quality and tool gate results drive decisions.**

Every phase output declares:
```
CONFIDENCE: [0–100]
BASIS: [what evidence supports this score]
GAPS: [what is unknown or assumed]
```

| Score | Signal to QA and ORCH |
|---|---|
| 85–100 | Strong evidence basis — proceed if tool gates pass |
| 70–84 | Gaps present — log assumptions before proceeding |
| 50–69 | Weak basis — research or revise; `ORCH` decides with explicit risk flag |
| 0–49 | No credible evidence — escalate to human; do not merge |

If evidence quality remains unacceptable after 3 iterations: halt and trigger HIL gate.

---

## TOOL GATES

Blocking checkpoints — do not finalise any output without passing the relevant gate. If a gate cannot be satisfied, declare the failure, state the substituted assumption with risk rating (Low / Medium / High / Critical), and log it. Execution continues only if risk ≤ Medium.

| Gate | What must be verified | Activating Agent | Failure blocks |
|---|---|---|---|
| `TG-01` — Platform runtime | iOS/Android background execution for always-on voice and health monitoring is viable without violating OS policies | `ARCH`, `ML` | Background service design |
| `TG-02` — Health API capability | HealthKit + Health Connect data types, permissions, and real-time access methods confirmed | `HEALTH` | Phase 3B |
| `TG-03` — Voice feasibility | STT model WER benchmarks on accented and elderly speech retrieved; offline fallback strategy viable | `ML` | Phase 2 |
| `TG-04` — Safety & emergency | False-positive mitigation and consent model designed before any emergency-dialling flow is finalised | `HEALTH`, `SEC` | Phase 3B |
| `TG-05` — Security & compliance | HIPAA/GDPR/local obligations mapped to specific implementations; biometric FAR/FRR benchmarks retrieved | `SEC` | Phase 6 |
| `TG-06` — Accessibility | WCAG 2.2 AA requirements and platform-specific elderly UX guidelines retrieved | `UX` | Phase 5 |

---

## RISK-TIER ROUTING

Assign a risk tier to each feature and phase deliverable. The tier determines review weight.

| Tier | Applies to | Review type |
|---|---|---|
| **T0** | Docs, media scheduling, news playback | Lightweight — `QA` spot check |
| **T1** | Reminders, communications, config push, voice pipeline | Standard — `QA` full acceptance review |
| **T2** | Emergency flow, health thresholds, biometric auth, health data encryption | Strict — `HEALTH` + `SEC` + `QA` joint sign-off; human approval before finalisation |

T2 items must never be auto-approved regardless of confidence score.

---

## EXECUTION FLOW

```
PHASE 0 [Scoping — ORCH + all agents]
    ↓
PHASE 1 [Architecture — ARCH leads]
    ↓
    ┌──────────────────────────────────────────┐
PHASE 2      PHASE 4        PHASE 5      PHASE 6
[ML]        [CONFIG]        [UX]         [SEC]
Voice/ML    Remote Config   UX/Access    Security
    └──────────────────────────────────────────┘
    ↓ [parallel phases complete + dependency handshakes]
PHASE 3A → PHASE 3B → PHASE 3C → PHASE 3D
Reminders   Health/Emrg    Comms        Media
    ↓
PHASE 7 [CRITIC pass → Tech Stack → Final Merge]
    ↓
FINAL DELIVERABLE PACKAGE
```

Phases 2, 4, 5, 6 run in parallel after Phase 1. Any cross-phase dependency requires a handshake: producing agent declares output ready; consuming agent confirms receipt and compatibility.

---

## PHASE 0 — Scoping & Constraints

**Agent:** `ORCH` + all agents
**Objective:** Lock scope before any design begins.

**Steps:**
1. Confirm target platforms: iOS, Android, or both
2. Confirm language list with regional dialect specificity (not just language families)
3. Confirm cloud provider preference or agnostic stance
4. Confirm on-device inference requirements for offline/low-connectivity scenarios
5. Confirm compliance jurisdiction (determines Phase 6 scope)
6. Define MVP boundary: **maximum 10 core user stories**, each with measurable acceptance criteria

**Acceptance Criteria:**
- [ ] Platforms locked with no ambiguity
- [ ] ≥ 3 languages specified with regional dialect variants
- [ ] On-device vs. cloud strategy decided
- [ ] Compliance jurisdiction mapped
- [ ] MVP stories listed (≤ 10), each with at least one measurable acceptance criterion

---

## PHASE 1 — System Architecture

**Agent:** `ARCH` (all agents input)
**Risk Tier:** T1
**Activate:** TG-01

**Steps:**
1. Design high-level architecture: mobile client, backend, AI/ML layer, health integrations, caregiver portal, notification pipeline
2. Define all service boundaries and communication protocols (REST, WebSocket, gRPC)
3. Identify on-device vs. cloud processing for each AI component — **Decision Block required**
4. Draft data models: User, Reminder, HealthMetric, Contact, MediaSchedule, ConfigPayload
5. Define config push mechanism — **Decision Block required**

**Acceptance Criteria:**
- [ ] No integration left as "TBD" — each has a named API/SDK and approach
- [ ] On-device vs. cloud boundary explicit for every AI component
- [ ] Data model covers all core entities (co-signed by `ARCH` + `QA`)
- [ ] Single points of failure identified with redundancy plans
- [ ] Offline degradation defined for every major feature

---

## PHASE 2 — Voice & Language Model Design *(parallel)*

**Agent:** `ML`
**Risk Tier:** T1
**Activate:** TG-03

**Steps:**
1. Select base multilingual STT model — justify with WER data on accented and elderly speech — **Decision Block required**
2. Design voice personalisation pipeline: enrollment sample requirements, adaptation approach, re-training triggers
3. Design intent classification: utterance → action mapping (minimum 40 intents, reviewed by `UX` for naturalness)
4. Define fallback hierarchy for low recognition confidence: confirm with user → simplified reprompt → PIN
5. Design voice biometric authentication with `SEC` — **Decision Block required**: enrollment, verification threshold, liveness detection, PIN fallback trigger

**Acceptance Criteria:**
- [ ] STT model selected with WER benchmark (target ≤ 15% for primary languages)
- [ ] Intent taxonomy ≥ 40 intents with natural language examples per supported language
- [ ] Pipeline handles code-switching (e.g., English + Hindi mid-sentence)
- [ ] Every authentication failure path resolves to retry or PIN — no dead ends
- [ ] Core commands functional offline (reminders, calls, emergency)

---

## PHASE 3A — Daily Routine & Reminder Engine *(sequential)*

**Agent:** `HEALTH` + `UX`
**Risk Tier:** T1

**Steps:**
1. Design reminder data model: type, schedule, recurrence, escalation rules, acknowledgement states
2. Define escalation per type: initial alert → repeat interval → family notification if unacknowledged after X minutes
3. Design delivery: local notification + voice TTS + screen overlay
4. Define acknowledgement flows ("Did you take it?") vs. informational-only reminders
5. Define missed-dose handling: log, notify family, escalate

**Acceptance Criteria:**
- [ ] All reminder types covered: wake-up, yoga, medication (×N daily), meals, bedtime, custom
- [ ] Medication reminders cannot be silently dismissed — acknowledgement or family notification mandatory
- [ ] All reminders remotely configurable; changes reflected within 60 seconds

---

## PHASE 3B — Health Monitoring & Emergency Response *(sequential)*

**Agent:** `HEALTH` + `SEC`
**Risk Tier:** T2 — joint sign-off `HEALTH` + `SEC` + `QA` required
**Activate:** TG-02, TG-04

**Steps:**
1. List all monitored health metrics with units and clinical threshold ranges
2. Define HealthKit + Health Connect integration: polling interval, data types, permissions
3. Design threshold configuration schema (per-metric; configurable by family/clinician)
4. Design emergency response as a full state machine — **Decision Block required for false-positive mitigation:**
   - Threshold breached → user confirmation window (10 sec)
   - No response or confirmed → call emergency services → notify contacts in priority order → voice reassurance
5. Define retry and fallback logic for failed emergency calls

**Acceptance Criteria:**
- [ ] Emergency flow executes within 15 seconds of breach to first outbound action
- [ ] User confirmation window prevents false positives unless user is unresponsive
- [ ] Emergency flow functional when app is backgrounded or screen is off
- [ ] Emergency flow cannot be triggered by spoofed voice (`SEC` sign-off)
- [ ] Retry and fallback covers all call-failure scenarios

---

## PHASE 3C — Communication *(sequential)*

**Agent:** `MEDIA` + `UX`
**Risk Tier:** T1

**Steps:**
1. Design voice-to-action flows: "Call [name]", "Message [name]", "Read my messages", "Read my notifications"
2. Define notification importance filter: critical / personal / promotional / system
3. Design WhatsApp and SMS integration approach
4. Define contact alias system: native language aliases mapped to saved contacts

**Acceptance Criteria:**
- [ ] User can complete a voice call without touching the screen
- [ ] Notification reading does not interrupt active calls or emergency flows
- [ ] Contact aliases support native language commands

---

## PHASE 3D — Entertainment & Scheduled Media *(sequential)*

**Agent:** `MEDIA`
**Risk Tier:** T0

**Steps:**
1. Design scheduled media system: time-based triggers for music, yoga videos, news
2. Define media integrations: YouTube API, local files
3. Design remote playlist management via companion app
4. Define voice playback controls: pause, next, volume, stop
5. Define interruption priority: Emergency > Medication Reminder > Other Reminder > Media

**Acceptance Criteria:**
- [ ] Media starts and stops entirely by voice
- [ ] Scheduled media yields immediately to emergency and medication events
- [ ] Resume behaviour after interruption defined

---

## PHASE 4 — Remote Configuration System *(parallel)*

**Agent:** `CONFIG` + `SEC`
**Risk Tier:** T1

**Steps:**
1. Design companion app features: reminders, contacts, health thresholds, playlists, language settings
2. Design config schema — versioned and auditable (who changed what, when) — **Decision Block required**
3. Design real-time push pipeline: change → backend → device → acknowledgement
4. Define conflict resolution for concurrent offline device changes and remote pushes
5. Design activity and health summary view for family

**Acceptance Criteria:**
- [ ] Config push latency ≤ 60 seconds end-to-end (architecture-validated)
- [ ] Schema versioned with full audit trail
- [ ] `SEC` reviewed config payload for injection and tampering vulnerabilities
- [ ] Non-technical family member can configure all core settings within 5 minutes

---

## PHASE 5 — UX & Accessibility *(parallel)*

**Agent:** `UX` + `ML`
**Risk Tier:** T1
**Activate:** TG-06

**Steps:**
1. Define UI principles: minimum tap targets (≥ 72px), font sizes, contrast ratios, voice-first operation
2. Design idle/home screen: what the user sees and hears when nothing is happening
3. Resolve voice activation approach with `ML` — always-listening wake word vs. button press — **Decision Block required**
4. Design for physical limitations: large buttons, tremor/shake tolerance, no complex gestures
5. Design cultural localisation: avoid Western-centric icons, RTL script support, culturally appropriate defaults
6. Define onboarding: voice-led, family-guided, requires zero reading from elderly user

**Acceptance Criteria:**
- [ ] Any core task completable in ≤ 3 voice commands
- [ ] App fully operable with screen off
- [ ] No feature requires typing
- [ ] All screens pass WCAG 2.2 AA contrast minimum
- [ ] `UX` + `ML` wake-word approach resolved — no open conflict

---

## PHASE 6 — Security & Compliance *(parallel)*

**Agent:** `SEC` + `HEALTH`
**Risk Tier:** T2 — human approval required before finalisation
**Activate:** TG-05

**Steps:**
1. Design voice biometric authentication: enrollment, verification, liveness detection, PIN fallback — **Decision Block required**
2. Design PIN fallback: lockout policy, family reset, social engineering resistance
3. Define encryption: at rest (device storage) and in transit (TLS 1.3 minimum)
4. Define caregiver role-based access controls (admin vs. view-only)
5. Map all compliance obligations (HIPAA / GDPR / local) to specific implementation decisions — no "assumed compliant" statements
6. Define threat model: impersonation, device theft, malicious caregiver access, data leakage

**Acceptance Criteria:**
- [ ] Voice auth cannot be bypassed without PIN
- [ ] Health and personal data encrypted at rest and in transit
- [ ] All compliance obligations mapped to specific implementations
- [ ] Emergency flow security jointly signed off by `HEALTH` + `SEC`

---

## PHASE 7 — CRITIC Pass, Tech Stack, and Final Merge

**Agents:** `CRITIC` → `ARCH` → `ORCH`

### Step 1 — CRITIC Review (before any tech stack finalisation)

`CRITIC` must adversarially attack the design produced in Phases 0–6. This is not optional and must not be diplomatic.

Required outputs:
1. **3 major failure modes** — specific scenarios where the system as designed will fail in production. For each: what fails, under what conditions, and what the impact is on the elderly user.
2. **3 simplification proposals** — features, flows, or governance elements that are over-engineered relative to their actual risk. Explain what should be cut or simplified.
3. **Top 3 unvalidated assumptions** — claims made throughout the design that are presented as facts but have no Tier 1 or Tier 2 evidence. Flag each with a validation plan.

Agents whose phases are criticised must respond with either a design revision or an evidence-backed counter-argument. `ORCH` arbitrates.

### Step 2 — Tech Stack

**Agent:** `ARCH`

1. Recommend full tech stack per layer: mobile, backend, AI/ML, config push, health APIs, media, auth, database — justify each choice
2. For each AI/ML component: cloud vs. on-device, model size, latency target, fallback behaviour
3. Flag open-source vs. commercial; licensing considerations
4. Define MVP scope (8–12 weeks): milestones, team roles, backlog priorities
5. Define Phase 2+ roadmap

**Acceptance Criteria:**
- [ ] Every component has a named technology — no TBDs
- [ ] On-device vs. cloud matrix complete for all AI components
- [ ] Licensing confirmed; no unresolved viral licence conflicts
- [ ] Stack achievable by 3–5 engineers
- [ ] Cost envelope estimated (development + ongoing operational)

### Step 3 — Final Merge

`ORCH` confirms all volumes are present, consistent, and cross-referenced before execution is considered complete.

---

## FINAL DELIVERABLE PACKAGE

| Volume | Required Contents |
|---|---|
| **V1 — Architecture** | System diagram, data models, API contracts, scalability plan, offline degradation strategy |
| **V2 — AI & Voice** | STT/TTS pipeline with Decision Block, intent taxonomy (≥ 40 intents), voice biometrics flow |
| **V3 — Feature Specs** | Reminder state machine, emergency state machine (T2), communication voice mappings, media interruption matrix |
| **V4 — Platform & Config** | Remote config schema (versioned), push pipeline with Decision Block, companion app spec, audit logging |
| **V5 — Security & Compliance** | Security model with Decision Block, compliance mapping, threat model, role-based access matrix |
| **V6 — UX & Accessibility** | UX principles (WCAG AA evidence), wake-word Decision Block, cultural localisation, onboarding flow |
| **V7 — Implementation** | Tech stack with justification, on-device vs. cloud matrix, MVP roadmap (8–12 weeks), test strategy |
| **V8 — Governance** | Decision Log (all Decision Blocks consolidated), Open Questions register (all resolved or deferred with owner and risk), Assumptions register |
| **V9 — Gate Results Report** | PASS / FAIL for each tool gate and each phase, with required remediation actions for any FAIL |

---

**STANDING EXECUTION DIRECTIVE:**
Evidence over assumption. Specificity over generality. Surface uncertainty — never paper over it. If a phase cannot complete due to missing information: list the missing inputs, state default assumptions clearly labelled as such, and proceed. Do not stall — flag and continue. The Critic's job is to make this specification harder to build incorrectly, not to block it. The output must be a specification an engineering team can build from without returning for clarification on core decisions.

<!-- END PROMPT -->
