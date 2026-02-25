Here's the advanced agentic execution version:

---

# AGENTIC BUILD SPEC v3 — AI Assistant App for Elderly Users (Non-English Speaking Background)

**Execution Mode:** Multi-agent, evidence-gated, confidence-routed
**Orchestration Rule:** No phase, task, or merge may proceed without satisfying all gate conditions. Agents must declare confidence scores explicitly. Low-confidence outputs are rerouted — never silently passed forward.

---

## AGENT ROSTER & RESPONSIBILITIES

Each agent operates independently within its domain. The Orchestrator manages sequencing, gates, and merges.

| Agent ID | Role | Scope |
|---|---|---|
| `ORCH` | Orchestrator | Sequencing, gate enforcement, conflict resolution, final merge |
| `ARCH` | Systems Architect | Architecture, data models, service boundaries, integration contracts |
| `ML` | ML/AI Engineer | Voice models, STT, intent classification, biometrics, inference strategy |
| `HEALTH` | Health & Safety Engineer | HealthKit/Health Connect, emergency flows, threshold logic |
| `UX` | Accessibility & UX Designer | Interface design, elderly UX, cultural localisation, onboarding |
| `SEC` | Security Engineer | Auth, encryption, access control, compliance |
| `CONFIG` | Platform Engineer | Remote config system, companion app, push pipeline, audit logging |
| `MEDIA` | Media & Comms Engineer | Entertainment, scheduling, WhatsApp/YouTube integration, TTS |
| `QA` | QA & Acceptance | Cross-phase validation, acceptance criteria sign-off, regression flags |

**Orchestrator Rules:**
- `ORCH` must be invoked at every phase boundary
- `ORCH` resolves conflicts between agents using the merge criteria defined in each phase
- `ORCH` may not override a hard gate — it must surface the blocker and halt that branch
- `ORCH` maintains a live **Decision Log** and **Open Questions Register** throughout execution

---

## CONFIDENCE ROUTING PROTOCOL

Every agent output must include an explicit confidence declaration using the following schema:

```
CONFIDENCE: [score 0–100]
BASIS: [what evidence supports this score]
GAPS: [what is unknown or assumed]
ROUTE: [see table below]
```

| Confidence Score | Routing Action |
|---|---|
| 90–100 | ✅ Proceed — output accepted, gate check runs |
| 70–89 | ⚠️ Conditional proceed — gaps must be logged, assumptions stated, `QA` notified |
| 50–69 | 🔁 Reroute — agent must research, revise, or request missing inputs before resubmitting |
| 0–49 | 🚫 Hard stop — `ORCH` escalates to human decision point; execution halts on this branch |

**Rule:** Confidence scores must never be inflated to pass a gate. `QA` agent audits all scores ≥ 90 on critical path items. Any score that cannot be substantiated by cited evidence is downgraded automatically.

---

## TOOL GATES

Tool gates are mandatory checkpoints. An agent may not produce a final output for a phase without activating the required tools and attaching their results as evidence.

### Defined Tool Gates

| Gate ID | Tool | Triggering Agent | Gate Condition |
|---|---|---|---|
| `TG-01` | Web search / API docs retrieval | `ARCH`, `ML`, `HEALTH` | Must be run before finalising any external API integration claim |
| `TG-02` | HealthKit + Health Connect API spec lookup | `HEALTH` | Required before Phase 3B begins |
| `TG-03` | STT model benchmarking lookup | `ML` | Must retrieve published WER scores for candidate models on multilingual/accented speech |
| `TG-04` | Compliance regulation lookup | `SEC` | Must retrieve current HIPAA / GDPR / local health data regulations before Phase 6 |
| `TG-05` | Dependency license check | `ARCH` | Must verify open-source licenses for all proposed components before Phase 7 finalises |
| `TG-06` | UX accessibility standards retrieval | `UX` | Must retrieve WCAG 2.2 and platform-specific elderly UX guidelines before Phase 5 |
| `TG-07` | Emergency services API availability check | `HEALTH` | Must confirm programmable emergency call options per target region (e.g. SOS API, PSAP access) |
| `TG-08` | Voice biometrics library benchmarking | `ML`, `SEC` | Must retrieve FAR/FRR benchmarks for candidate voice biometric libraries |

**Tool Gate Failure Protocol:** If a tool gate cannot be satisfied (e.g., no retrievable data), the agent must declare this explicitly, state what assumption is being substituted, assign it a risk rating (Low / Medium / High / Critical), and log it in the Open Questions Register. Execution may continue only if risk rating is ≤ Medium. High or Critical tool gate failures halt the phase.

---

## EVIDENCE REQUIREMENTS

Every phase deliverable must include an Evidence Package. The package is reviewed by `QA` before merge is approved.

**Evidence Package Schema:**
```
PHASE: [phase ID]
AGENT: [agent ID]
DELIVERABLE: [what was produced]
EVIDENCE:
  - [Source or tool output 1]: [summary of what it confirms]
  - [Source or tool output 2]: [summary of what it confirms]
ASSUMPTIONS:
  - [Assumption]: [risk level] [mitigation]
CONFIDENCE: [score]
GAPS: [unresolved items]
```

**Minimum Evidence Requirements per Phase:**

| Phase | Minimum Evidence Items | Evidence Types Accepted |
|---|---|---|
| 0 — Scoping | 3 | Stakeholder inputs, regulatory docs, platform capability confirmations |
| 1 — Architecture | 5 | API docs, architecture precedents, integration specs, data model validation |
| 2 — Voice/ML | 6 | Model benchmarks, WER data, dialect coverage studies, biometric FAR/FRR data |
| 3A — Reminders | 3 | Health reminder UX research, notification API docs, escalation pattern references |
| 3B — Health/Emergency | 6 | HealthKit/Health Connect API docs, emergency service API confirmations, clinical threshold references |
| 3C — Communications | 3 | WhatsApp API docs, accessibility API capabilities, contact resolution approach |
| 3D — Media | 3 | YouTube API docs, TTS engine comparisons, scheduling architecture references |
| 4 — Remote Config | 4 | Config push latency benchmarks, conflict resolution patterns, audit log schema references |
| 5 — UX | 5 | WCAG 2.2 docs, elderly UX research papers, cultural localisation guidelines, tremor UX studies |
| 6 — Security | 5 | HIPAA/GDPR regulations, biometric security standards, encryption specs, penetration testing checklists |
| 7 — Tech Stack | 4 | Licensing docs, benchmark comparisons, maintenance activity checks, cost modelling |

---

## MERGE CRITERIA

At each phase boundary, `ORCH` runs a merge review. All criteria must be met before outputs from that phase are merged into the working specification and the next phase unlocks.

### Universal Merge Criteria (apply to every phase)

- [ ] All agent outputs for the phase are present
- [ ] Every output includes a completed Evidence Package
- [ ] No output has a confidence score below 70 (below 70 = reroute before merge)
- [ ] All tool gates for the phase have been activated and results attached
- [ ] `QA` has reviewed and signed off on acceptance criteria
- [ ] Open Questions Register has been updated with any new blockers
- [ ] No critical assumption is unlogged

### Phase-Specific Merge Criteria

**Phase 0 merge unlocks Phase 1:**
- [ ] Platform targets (iOS/Android/both) confirmed with no ambiguity
- [ ] Minimum language list ratified with dialect specificity (not just "Hindi" — specify regional variants)
- [ ] Compliance jurisdiction confirmed (determines Phase 6 scope)

**Phase 1 merge unlocks Phases 2, 3, 4, 5, 6 (parallel):**
- [ ] All service boundaries defined with named protocols — no "TBD" interfaces
- [ ] On-device vs. cloud boundary explicitly drawn for every AI component
- [ ] Data model covers all entities — `ARCH` and `QA` must co-sign
- [ ] `ORCH` confirms no circular dependencies between parallel phases

**Phase 2 merge unlocks Phase 3 (all sub-phases):**
- [ ] STT model selected with benchmark evidence (WER on accented/multilingual speech ≤ target)
- [ ] Intent taxonomy contains ≥ 40 intents, reviewed by `UX` for language naturalness
- [ ] Confidence thresholds peer-reviewed by `ML` and `SEC` jointly
- [ ] Offline core command set confirmed and tested path documented

**Phase 3 (all sub-phases) merge unlocks Phase 7:**
- [ ] All sub-phases 3A–3D completed and individually signed off by `QA`
- [ ] No cross-sub-phase conflict exists (e.g., media playback vs. emergency interruption priority)
- [ ] `HEALTH` and `MEDIA` have resolved interruption priority in writing

**Phase 4 merge gate (runs in parallel — must complete before Phase 7):**
- [ ] Config push latency ≤ 60 seconds confirmed by architecture or benchmark evidence
- [ ] Conflict resolution policy covers all identified edge cases
- [ ] `SEC` has reviewed config payload for injection or tampering vulnerabilities

**Phase 5 merge gate (runs in parallel — must complete before Phase 7):**
- [ ] `UX` and `ML` have jointly resolved wake-word activation approach — no open conflict
- [ ] All screens validated against WCAG AA — `QA` signs off
- [ ] Cultural localisation decisions reviewed by a named reference (research paper, community guideline, or subject matter input)

**Phase 6 merge gate (runs in parallel — must complete before Phase 7):**
- [ ] `SEC` and `HEALTH` have jointly signed off emergency flow security (cannot be triggered by spoofed voice)
- [ ] Compliance obligations mapped to specific implementation decisions — nothing left as "assumed compliant"
- [ ] PIN reset path reviewed for social engineering vulnerabilities

**Phase 7 final merge (all phases must be merged before this runs):**
- [ ] Every system component from Phase 1 has a named technology — `ARCH` confirms completeness
- [ ] No licensing conflict exists across the full stack — `TG-05` evidence attached
- [ ] Cost envelope estimated and flagged if any component exceeds sustainable threshold
- [ ] `ORCH` produces Final Deliverable Package (see below)

---

## EXECUTION FLOW

```
PHASE 0 [ORCH + all agents]
    ↓ [MERGE GATE 0]
PHASE 1 [ARCH leads; all agents input]
    ↓ [MERGE GATE 1]
    ┌──────────────────────────────────────┐
PHASE 2     PHASE 4     PHASE 5     PHASE 6
[ML]       [CONFIG]     [UX]        [SEC]
    └──────────────────────────────────────┘
    ↓ [all parallel phases merged]
PHASE 3A → 3B → 3C → 3D  [sequential, dedicated agents]
    ↓ [MERGE GATE 3]
PHASE 7 [ARCH + all agents; ORCH final merge]
    ↓
FINAL DELIVERABLE PACKAGE
```

**Parallel Phase Rule:** Phases 2, 4, 5, and 6 may execute simultaneously after Phase 1 merges. However, any cross-phase dependency (e.g., `ML` output needed by `SEC` for biometrics) must be resolved via a **dependency handshake**: the producing agent declares output ready, the consuming agent confirms receipt and compatibility before proceeding.

---

## OPEN QUESTIONS REGISTER

`ORCH` maintains this register throughout. Format:

```
OQ-[ID] | Phase raised | Agent | Question | Blocking? | Assumption used | Risk | Status
```

**Rules:**
- Every gap from every Evidence Package must generate an OQ entry
- Blocking OQs halt the relevant phase branch until resolved
- Non-blocking OQs must have a stated assumption and risk rating
- All OQs must be resolved or formally deferred (with owner and deadline) before Final Deliverable Package is issued

---

## CONFLICT RESOLUTION PROTOCOL

When two agents produce conflicting outputs (e.g., `ML` and `UX` disagree on wake word activation approach):

1. Both agents state their position with supporting evidence
2. `ORCH` identifies the decision criteria (safety, usability, technical feasibility, cost)
3. `ORCH` applies a weighted decision: **Safety > Accessibility > Technical Feasibility > Cost**
4. The losing position is logged in the Decision Log with rationale — it is not discarded
5. If `ORCH` cannot resolve with confidence ≥ 70, the conflict is escalated to a human decision point and logged as a blocking OQ

---

## FINAL DELIVERABLE PACKAGE

`ORCH` assembles and confirms all of the following before execution is considered complete:

**Architecture & Design**
- [ ] System architecture (all components, boundaries, protocols)
- [ ] Data models for all core entities
- [ ] Service integration contracts (inputs, outputs, error states for every external API)

**AI & Voice**
- [ ] STT pipeline spec with benchmark evidence
- [ ] Intent taxonomy (≥ 40 intents, with natural language examples per language)
- [ ] Voice biometric enrolment and verification flow
- [ ] Confidence routing thresholds for all voice interactions

**Feature Specs**
- [ ] Reminder engine with escalation state machine
- [ ] Emergency response state machine (all states, transitions, exit conditions)
- [ ] Communication voice command mapping
- [ ] Media scheduling and interruption priority matrix

**Platform & Config**
- [ ] Remote config schema (versioned, auditable)
- [ ] Config push pipeline with latency evidence
- [ ] Companion app feature list and wireframe descriptions

**Security & Compliance**
- [ ] Security model (voice biometrics + PIN + encryption)
- [ ] Compliance obligation mapping (HIPAA/GDPR/local)
- [ ] Role-based access control matrix

**UX & Accessibility**
- [ ] UX principles with WCAG AA evidence
- [ ] Cultural localisation decisions per language group
- [ ] Onboarding flow spec

**Tech Stack**
- [ ] Full stack recommendation with justification per component
- [ ] On-device vs. cloud matrix for all AI components
- [ ] Licensing and cost flags

**Governance**
- [ ] Decision Log (all major decisions with rationale)
- [ ] Open Questions Register (all resolved; deferred items have owners)
- [ ] Assumptions Register with risk ratings
- [ ] Known limitations and recommended next steps

---

**STANDING EXECUTION DIRECTIVE:** At every step, prefer evidence over assumption. Prefer specificity over generality. When in doubt, surface the uncertainty — do not paper over it. The goal is a specification that a team of engineers can build from without returning for clarification on core decisions.