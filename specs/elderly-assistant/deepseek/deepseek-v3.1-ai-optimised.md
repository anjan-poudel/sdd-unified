# AGENTIC EXECUTION SPEC: AI Assistant for Elderly Non-English Speaking Users

**Execution Mode:** Multi-agent, evidence-based, confidence-gated
**Orchestration Principle:** No phase proceeds without meeting all acceptance criteria. Agents must declare confidence scores explicitly. Low-confidence outputs trigger rerouting — never silent propagation.

---

## AGENT ROSTER & RESPONSIBILITIES

| Agent ID | Role | Scope & Deliverables |
|---|---|---|
| `ORCH` | Orchestrator | Sequence management, gate enforcement, conflict resolution, final merge |
| `ARCH` | Systems Architect | Overall architecture, data models, service boundaries, integration contracts |
| `ML` | ML/AI Engineer | Voice models (STT/TTS), intent classification, biometrics, inference strategy |
| `HEALTH` | Health & Safety Engineer | HealthKit/Health Connect integration, emergency workflows, threshold logic |
| `UX` | Accessibility & UX Designer | Elderly-focused UX, cultural localization, onboarding, WCAG compliance |
| `SEC` | Security Engineer | Authentication, encryption, compliance (HIPAA/GDPR), threat modeling |
| `CONFIG` | Platform Engineer | Remote configuration system, companion app, push pipeline, audit logging |
| `MEDIA` | Media & Communications Engineer | Entertainment scheduling, WhatsApp/YouTube integration, TTS, media playback |
| `QA` | Quality & Acceptance | Cross-phase validation, acceptance criteria sign-off, regression checks |

**Orchestrator Rules:**
- `ORCH` must be invoked at every phase boundary
- `ORCH` resolves conflicts using weighted criteria (Safety > Accessibility > Feasibility > Cost)
- `ORCH` maintains a live **Decision Log** and **Open Questions Register**
- No gate may be overridden — blockers must be surfaced and addressed

---

## CONFIDENCE ROUTING PROTOCOL

Every agent output must include explicit confidence declaration:

```
CONFIDENCE: [0-100]
BASIS: [evidence supporting this score]
GAPS: [unknowns or assumptions]
ROUTE: [see routing table]
```

| Confidence | Routing Action |
|---|---|
| 90–100 | ✅ Proceed — output accepted, gate check runs |
| 70–89 | ⚠️ Conditional proceed — gaps logged, assumptions stated, `QA` notified |
| 50–69 | 🔁 Reroute — agent must research, revise, or request missing inputs |
| 0–49 | 🚫 Hard stop — `ORCH` escalates to human decision; execution halts |

**Rule:** Confidence scores must reflect actual evidence. `QA` audits scores ≥ 90 on critical path items.

---

## TOOL GATES (Mandatory Checkpoints)

| Gate ID | Tool | Triggering Agent | Gate Condition |
|---|---|---|---|
| `TG-01` | Web search / API docs retrieval | `ARCH`, `ML`, `HEALTH` | Required before finalizing any external API integration claim |
| `TG-02` | HealthKit + Health Connect API spec lookup | `HEALTH` | Required before Phase 3B begins |
| `TG-03` | STT model benchmarking | `ML` | Must retrieve WER scores for candidate models on multilingual/accented speech |
| `TG-04` | Compliance regulation lookup | `SEC` | Must retrieve HIPAA/GDPR/local health data regulations before Phase 6 |
| `TG-05` | Dependency license check | `ARCH` | Verify open-source licenses for all proposed components |
| `TG-06` | UX accessibility standards retrieval | `UX` | Must retrieve WCAG 2.2 and platform-specific elderly UX guidelines |
| `TG-07` | Emergency services API availability | `HEALTH` | Confirm programmable emergency call options per target region |
| `TG-08` | Voice biometrics benchmarking | `ML`, `SEC` | Retrieve FAR/FRR benchmarks for candidate voice biometric libraries |

**Tool Gate Failure Protocol:** If a gate cannot be satisfied, agent must:
1. Declare failure explicitly
2. State substituted assumption with risk rating (Low/Medium/High/Critical)
3. Log in Open Questions Register
4. Execution may continue only if risk ≤ Medium

---

## EVIDENCE REQUIREMENTS

Every phase deliverable must include an Evidence Package (reviewed by `QA` before merge):

```
PHASE: [phase ID]
AGENT: [agent ID]
DELIVERABLE: [what was produced]
EVIDENCE:
  - [Source/tool output 1]: [summary of confirmation]
  - [Source/tool output 2]: [summary of confirmation]
ASSUMPTIONS:
  - [Assumption]: [risk level] [mitigation]
CONFIDENCE: [score]
GAPS: [unresolved items]
```

**Minimum Evidence Requirements:**

| Phase | Minimum Evidence | Evidence Types |
|---|---|---|
| 0 — Scoping | 3 | Stakeholder inputs, regulatory docs, platform capabilities |
| 1 — Architecture | 5 | API docs, architecture precedents, integration specs, data models |
| 2 — Voice/ML | 6 | Model benchmarks, WER data, dialect coverage, biometric FAR/FRR |
| 3A — Reminders | 3 | Health reminder UX research, notification API docs |
| 3B — Health/Emergency | 6 | Health API docs, emergency service APIs, clinical thresholds |
| 3C — Communications | 3 | WhatsApp API docs, accessibility APIs, contact resolution |
| 3D — Media | 3 | YouTube API docs, TTS engine comparisons, scheduling patterns |
| 4 — Remote Config | 4 | Config push latency benchmarks, conflict resolution patterns |
| 5 — UX | 5 | WCAG 2.2 docs, elderly UX research, cultural localization guidelines |
| 6 — Security | 5 | Compliance regulations, biometric standards, encryption specs |
| 7 — Tech Stack | 4 | Licensing docs, benchmark comparisons, cost modeling |

---

## EXECUTION PHASES & ACCEPTANCE CRITERIA

### PHASE 0: SCOPING & FOUNDATION
**Agents:** `ORCH` + all agents input
**Deliverables:**
- Platform targets confirmed (iOS/Android/both)
- Minimum language list with dialect specificity
- Compliance jurisdiction confirmed
- Stakeholder requirements validated

**Acceptance Criteria:**
- [ ] No ambiguity in platform targets
- [ ] Languages specified with regional variants (not just "Hindi")
- [ ] Compliance jurisdiction mapped to Phase 6 scope
- [ ] All agents have reviewed and confirmed scope understanding

### PHASE 1: SYSTEM ARCHITECTURE
**Lead Agent:** `ARCH` (all agents input)
**Deliverables:**
- High-level system architecture diagram
- Service boundaries with named protocols
- Data models for all core entities
- On-device vs. cloud boundary for AI components

**Acceptance Criteria:**
- [ ] All service boundaries defined with no "TBD" interfaces
- [ ] Data model covers all entities (User, Reminder, HealthMetric, Contact, etc.)
- [ ] `ARCH` and `QA` co-sign data model completeness
- [ ] No circular dependencies between parallel phases

### PHASE 2: VOICE & AI PIPELINE (Parallel)
**Lead Agent:** `ML`
**Deliverables:**
- STT/TTS architecture with benchmark evidence
- Intent taxonomy (≥ 40 intents with natural language examples)
- Voice biometrics enrollment/verification flow
- Confidence thresholds for voice interactions

**Acceptance Criteria:**
- [ ] STT model selected with WER ≤ target for accented/multilingual speech
- [ ] Intent taxonomy reviewed by `UX` for naturalness
- [ ] Confidence thresholds peer-reviewed by `ML` and `SEC`
- [ ] Offline core command set confirmed

### PHASE 3A: REMINDER ENGINE
**Lead Agent:** `HEALTH` + `UX`
**Deliverables:**
- Reminder state machine with escalation logic
- Missed-dose handling workflow
- Calendar integration design
- Notification priority matrix

**Acceptance Criteria:**
- [ ] Escalation logic covers all reminder types
- [ ] Confirmation flows defined for critical reminders (medications)
- [ ] Google Calendar integration approach validated
- [ ] Interruption handling for emergency scenarios

### PHASE 3B: HEALTH & EMERGENCY
**Lead Agent:** `HEALTH` + `SEC`
**Deliverables:**
- Health API integration design (HealthKit/Health Connect)
- Emergency response state machine
- Threshold-based alert logic
- Emergency contact cascade workflow

**Acceptance Criteria:**
- [ ] Health API integration approach validated with `TG-02`
- [ ] Emergency workflow cannot be triggered by spoofed voice
- [ ] Contact cascade includes fallback mechanisms
- [ ] User reassurance messaging defined

### PHASE 3C: COMMUNICATIONS
**Lead Agent:** `MEDIA` + `UX`
**Deliverables:**
- Voice-based messaging/calling architecture
- Smart notification filtering logic
- WhatsApp/SMS integration approach
- Importance detection algorithm

**Acceptance Criteria:**
- [ ] WhatsApp API integration approach validated
- [ ] Notification importance detection logic defined
- [ ] Contact resolution approach for voice commands
- [ ] Privacy controls for message reading

### PHASE 3D: MEDIA & ENTERTAINMENT
**Lead Agent:** `MEDIA` + `UX`
**Deliverables:**
- Media scheduling system design
- YouTube integration approach
- Scheduled news/music playback architecture
- Interruption priority matrix

**Acceptance Criteria:**
- [ ] YouTube API integration approach validated
- [ ] Scheduling system handles timezone differences
- [ ] Media interruption priorities defined (emergency > reminder > media)
- [ ] Offline media playback strategy

### PHASE 4: REMOTE CONFIGURATION (Parallel)
**Lead Agent:** `CONFIG` + `SEC`
**Deliverables:**
- Remote configuration schema (versioned)
- Config push pipeline design
- Companion app feature list
- Conflict resolution policy

**Acceptance Criteria:**
- [ ] Config push latency ≤ 60 seconds (architecture validated)
- [ ] Conflict resolution covers all edge cases
- [ ] `SEC` has reviewed config payload for vulnerabilities
- [ ] Audit logging schema defined

### PHASE 5: UX & ACCESSIBILITY (Parallel)
**Lead Agent:** `UX` + `ML`
**Deliverables:**
- Elderly-focused UX principles
- Cultural localization decisions per language
- Onboarding flow specification
- WCAG 2.2 compliance plan

**Acceptance Criteria:**
- [ ] All screens validated against WCAG AA
- [ ] Cultural localization reviewed with reference sources
- [ ] Wake-word activation approach resolved (no `UX`-`ML` conflict)
- [ ] Onboarding covers voice training and emergency setup

### PHASE 6: SECURITY & COMPLIANCE (Parallel)
**Lead Agent:** `SEC` + `HEALTH`
**Deliverables:**
- Security model (voice biometrics + PIN + encryption)
- Compliance obligation mapping
- Role-based access control matrix
- Threat model and mitigation

**Acceptance Criteria:**
- [ ] Emergency flow security signed off by `SEC` and `HEALTH`
- [ ] Compliance obligations mapped to specific implementations
- [ ] PIN reset path reviewed for social engineering vulnerabilities
- [ ] Data encryption strategy for health data

### PHASE 7: TECH STACK & FINAL MERGE
**Lead Agent:** `ARCH` (all agents input, `ORCH` final merge)
**Deliverables:**
- Complete technology stack recommendation
- Licensing compliance confirmation
- Cost envelope estimation
- Final Deliverable Package

**Acceptance Criteria:**
- [ ] Every system component has named technology
- [ ] No licensing conflicts across stack (`TG-05` evidence attached)
- [ ] Cost envelope within sustainable threshold
- [ ] All previous phase acceptance criteria met

---

## EXECUTION FLOW

```
PHASE 0 [ORCH + all agents]
    ↓ [MERGE GATE 0]
PHASE 1 [ARCH leads; all agents input]
    ↓ [MERGE GATE 1]
    ┌──────────────────────────────────────┐
PHASE 2     PHASE 4     PHASE 5     PHASE 6   [Parallel]
[ML]       [CONFIG]     [UX]        [SEC]
    └──────────────────────────────────────┘
    ↓ [all parallel phases complete]
PHASE 3A → 3B → 3C → 3D  [Sequential sub-phases]
    ↓ [MERGE GATE 3]
PHASE 7 [ARCH + all agents; ORCH final merge]
    ↓
FINAL DELIVERABLE PACKAGE
```

**Parallel Phase Rule:** Phases 2, 4, 5, 6 execute simultaneously after Phase 1. Cross-phase dependencies require **dependency handshake**: producing agent declares output ready, consuming agent confirms compatibility.

---

## MERGE CRITERIA

### Universal Merge Criteria (all phases)
- [ ] All agent outputs for phase present
- [ ] Every output includes completed Evidence Package
- [ ] No output has confidence score < 70
- [ ] All tool gates for phase activated with results attached
- [ ] `QA` has reviewed and signed off acceptance criteria
- [ ] Open Questions Register updated with new blockers
- [ ] No critical assumption unlogged

### Phase-Specific Merge Criteria
- **Phase 0 → 1:** Platform targets unambiguous, language list specific
- **Phase 1 → 2/4/5/6:** Service boundaries defined, data model complete
- **Phase 2 → 3:** STT model selected, intent taxonomy complete
- **Phase 3A-D → 7:** All sub-phases completed, no cross-phase conflicts
- **Phase 4/5/6 → 7:** Individual phase criteria met before Phase 7
- **Phase 7 Final:** All previous criteria met, Final Deliverable Package complete

---

## FINAL DELIVERABLE PACKAGE

`ORCH` assembles and confirms:

### Architecture & Design
- [ ] System architecture (components, boundaries, protocols)
- [ ] Data models for all core entities
- [ ] Service integration contracts (APIs, error states)

### AI & Voice
- [ ] STT/TTS pipeline spec with benchmarks
- [ ] Intent taxonomy (≥ 40 intents with examples)
- [ ] Voice biometrics enrollment/verification flow
- [ ] Confidence routing thresholds

### Feature Specifications
- [ ] Reminder engine with escalation state machine
- [ ] Emergency response state machine
- [ ] Communication voice command mapping
- [ ] Media scheduling with interruption priorities

### Platform & Config
- [ ] Remote configuration schema (versioned, auditable)
- [ ] Config push pipeline with latency evidence
- [ ] Companion app wireframe descriptions

### Security & Compliance
- [ ] Security model (voice + PIN + encryption)
- [ ] Compliance obligation mapping
- [ ] Role-based access control matrix

### UX & Accessibility
- [ ] UX principles with WCAG AA evidence
- [ ] Cultural localization decisions per language
- [ ] Onboarding flow specification

### Tech Stack
- [ ] Full stack recommendation with justification
- [ ] On-device vs. cloud matrix for AI components
- [ ] Licensing and cost analysis

### Governance
- [ ] Decision Log (all major decisions with rationale)
- [ ] Open Questions Register (all resolved; deferred items have owners)
- [ ] Assumptions Register with risk ratings
- [ ] Known limitations and next steps

---

## CONFLICT RESOLUTION PROTOCOL

When agents produce conflicting outputs:
1. Both agents state position with supporting evidence
2. `ORCH` identifies decision criteria (Safety > Accessibility > Feasibility > Cost)
3. `ORCH` applies weighted decision
4. Losing position logged in Decision Log with rationale
5. If `ORCH` confidence < 70, escalate to human decision point

---

## OPEN QUESTIONS REGISTER

`ORCH` maintains throughout execution:
```
OQ-[ID] | Phase | Agent | Question | Blocking? | Assumption | Risk | Status
```

**Rules:**
- Every gap from Evidence Package generates OQ entry
- Blocking OQs halt relevant phase branch
- Non-blocking OQs require stated assumption and risk rating
- All OQs resolved or formally deferred before Final Deliverable

---

**EXECUTION PRINCIPLE:** Evidence over assumption. Specificity over generality. Surface uncertainty — never paper over it. Produce a specification that engineering teams can build from without clarification on core decisions.