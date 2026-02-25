Here's the agentic execution version:

---

# BUILD SPEC: AI Assistant App for Elderly Users (Non-English Speaking Background)

**Execution Mode:** Agentic — work through each phase sequentially. Complete all checklist items and meet acceptance criteria before proceeding to the next phase. Flag blockers explicitly.

---

## PHASE 0 — Project Scoping & Constraints

**Objective:** Establish foundations before any design or implementation work begins.

**Steps:**
1. Confirm target platforms: iOS, Android, or both
2. Confirm primary languages/dialects to support (e.g., Hindi, Punjabi, Cantonese, Greek — list all)
3. Confirm cloud provider preference (AWS / GCP / Azure / agnostic)
4. Confirm whether on-device inference is required for offline/low-connectivity scenarios
5. Confirm regulatory requirements (HIPAA, GDPR, or local equivalents) based on target geography

**Acceptance Criteria:**
- [ ] Platform targets are locked
- [ ] Minimum 3 supported languages/dialects identified
- [ ] Cloud + on-device inference strategy decided
- [ ] Compliance scope documented

---

## PHASE 1 — System Architecture Design

**Objective:** Produce a complete system architecture before any component work begins.

**Steps:**
1. Design high-level architecture diagram covering: mobile client, backend services, AI/ML layer, health integrations, remote config service, notification pipeline, and companion (family) app
2. Define all service boundaries and communication protocols (REST, WebSocket, gRPC)
3. Identify which processing is on-device vs. cloud (voice recognition, LLM inference, health monitoring)
4. Define data models for: user profile, health thresholds, reminder schedules, contact lists, media playlists, config payloads
5. Document the real-time config push mechanism (e.g., Firebase Remote Config, WebSocket, push notification with payload)

**Checklist:**
- [ ] Architecture diagram produced with all major components labelled
- [ ] On-device vs. cloud processing boundaries explicitly defined
- [ ] All external API integrations listed (Apple HealthKit, Google Health Connect, Google Calendar, WhatsApp, YouTube)
- [ ] Config push mechanism selected and justified
- [ ] Data models drafted for all core entities

**Acceptance Criteria:**
- [ ] Architecture reviewed for single points of failure — redundancy documented
- [ ] No integration is left as "TBD" — each has a named API/SDK and integration approach
- [ ] Offline degradation behaviour defined for each feature

---

## PHASE 2 — Voice & Language Model Design

**Objective:** Design the personalised voice recognition and natural language understanding pipeline.

**Steps:**
1. Select base multilingual speech-to-text model (e.g., Whisper large-v3, Azure Speech, Google STT) — justify dialect coverage
2. Design voice personalisation pipeline:
    - Define minimum voice sample requirements (duration, sentence variety, format)
    - Define fine-tuning or adapter approach for accent/dialect personalisation
    - Define re-training trigger (e.g., after X failed recognitions)
3. Design intent classification layer on top of STT output (map utterances → actions)
4. Define fallback hierarchy when recognition confidence is low:
    - Confirm with user → simplified reprompt → escalate to PIN input
5. Design voice biometric authentication flow:
    - Enrolment (number of samples, quality thresholds)
    - Verification (match threshold, anti-spoofing)
    - PIN fallback trigger conditions
6. Document supported command taxonomy (full list of voice commands the assistant must understand at launch)

**Checklist:**
- [ ] Base STT model selected with dialect coverage matrix documented
- [ ] Voice personalisation pipeline fully specced (inputs → process → outputs)
- [ ] Intent taxonomy documented (minimum 40 intent types across all feature areas)
- [ ] Confidence threshold values defined for recognition, authentication, and fallback triggers
- [ ] On-device model size and latency targets defined (e.g., <2s response on mid-range device)
- [ ] Voice biometric enrolment and verification flow documented step by step

**Acceptance Criteria:**
- [ ] Pipeline handles code-switching (e.g., user mixing English and Hindi mid-sentence)
- [ ] Authentication flow has no dead ends — every failure path resolves to either retry or PIN
- [ ] Offline voice recognition is functional for core commands (reminders, calls, emergency)

---

## PHASE 3 — Core Feature Implementation Specs

Work through each sub-feature below in order. Each must be fully specced before moving to the next.

---

### 3A — Daily Routine & Reminder Engine

**Steps:**
1. Design reminder data model (type, schedule, recurrence, escalation rules, acknowledgement states)
2. Define escalation logic for medication reminders: initial alert → repeat interval → notify family if unacknowledged after X minutes
3. Design the reminder delivery mechanism (local notification + voice TTS + screen overlay)
4. Define which reminders require acknowledgement vs. are informational only

**Checklist:**
- [ ] All reminder types listed: wake-up, yoga, medication (×N daily), meals, bedtime, custom
- [ ] Escalation rules defined per reminder type
- [ ] Acknowledgement flow designed (voice "yes I've taken it" → mark complete)
- [ ] Missed reminder behaviour defined (log, notify family, escalate)

**Acceptance Criteria:**
- [ ] Medication reminders cannot be silently dismissed — acknowledgement or family notification is mandatory
- [ ] All reminders are remotely configurable with changes reflected on device within 60 seconds

---

### 3B — Health Monitoring & Emergency Response

**Steps:**
1. Map all health metrics to be monitored (blood pressure, heart rate, blood glucose, SpO2 — confirm full list)
2. Define read/write integration with Apple HealthKit and Google Health Connect (polling interval, data types, permissions)
3. Define threshold configuration schema (per-metric min/max, who can set thresholds — family/doctor)
4. Design emergency response flow as a state machine:
    - Threshold breached → confirm with user (10 sec) → no response or confirmed → trigger emergency sequence
    - Emergency sequence: call emergency services + notify family contacts in priority order + voice reassurance to user
5. Define what happens if emergency call fails (retry logic, fallback contacts)
6. Design health data dashboard for the companion (family) app

**Checklist:**
- [ ] All monitored health metrics listed with units and threshold ranges
- [ ] HealthKit + Health Connect permission and sync flow documented
- [ ] Emergency state machine fully diagrammed (all states, transitions, and exit conditions)
- [ ] Family notification payload defined (what information is sent, in what format)
- [ ] Retry and fallback logic for failed emergency calls documented

**Acceptance Criteria:**
- [ ] Emergency flow executes in under 15 seconds from threshold breach to first outbound action
- [ ] User is verbally reassured at each step of the emergency sequence
- [ ] Emergency flow is functional even when app is in background or screen is off

---

### 3C — Communication (Calls, Messages, Notifications)

**Steps:**
1. Design voice-to-action flow for: "Call [name]", "Message [name] [content]", "Read my messages", "Read my notifications"
2. Define notification importance filter (rules for what gets read aloud vs. silently logged)
3. Design WhatsApp and SMS integration (deep links, accessibility APIs, or direct API where available)
4. Define contact list management — how contacts are added, named (with aliases for voice matching), and prioritised

**Checklist:**
- [ ] Voice command → action mapping documented for all communication intents
- [ ] Notification filter rules defined (categories: critical / personal / promotional / system)
- [ ] Contact alias system designed (e.g., "Call my son" maps to a saved contact)
- [ ] Read-aloud TTS voice and speed configurable per user

**Acceptance Criteria:**
- [ ] User can complete a voice call without touching the screen
- [ ] Notification reading does not interrupt active calls or emergency flows
- [ ] Contact aliases support the user's native language (e.g., "Apne bete ko call karo")

---

### 3D — Entertainment & Scheduled Media

**Steps:**
1. Design scheduled media system (time-based triggers for music, yoga videos, news)
2. Define media source integrations (YouTube API, local files, streaming services)
3. Design playlist management (how family configures playlists remotely)
4. Define voice control commands during playback (pause, next, volume, stop)

**Checklist:**
- [ ] All scheduled media types listed: music, yoga/exercise video, news briefing, custom
- [ ] YouTube and local media playback integration specced
- [ ] Remote playlist configuration flow documented
- [ ] Playback interrupted by reminders or emergency — resume behaviour defined

**Acceptance Criteria:**
- [ ] Media starts and stops entirely via voice
- [ ] Scheduled media yields immediately to emergency or medication reminder events
- [ ] News briefing is sourced from a configurable, reliable feed and read aloud in the user's language

---

## PHASE 4 — Remote Configuration System (Companion App)

**Objective:** Design the interface and backend that lets family members configure the elderly user's app remotely.

**Steps:**
1. Design companion app features (web + mobile): reminder management, contact management, health thresholds, media playlists, notification filters, language settings
2. Design config data schema — must be versionable and auditable (who changed what, when)
3. Design real-time config push pipeline (change on companion app → backend → push to device → acknowledgement)
4. Define conflict resolution if device has pending offline changes when a remote config arrives
5. Design activity/health summary view for family (recent reminders, acknowledgements, health metrics, missed events)

**Checklist:**
- [ ] Full list of remotely configurable settings documented
- [ ] Config schema versioned and auditable
- [ ] Push latency target defined (≤60 seconds end-to-end)
- [ ] Conflict resolution policy documented
- [ ] Family activity dashboard wireframed

**Acceptance Criteria:**
- [ ] A family member with no technical knowledge can configure all core settings within 5 minutes
- [ ] All config changes are logged with timestamp and author
- [ ] Device reflects config changes without requiring a restart

---

## PHASE 5 — UX & Accessibility Design

**Objective:** Ensure the interface is usable by elderly users with cognitive, physical, and cultural barriers.

**Steps:**
1. Define UI principles: minimum tap targets, font sizes, contrast ratios, icon-free navigation (text or voice only where possible)
2. Design the idle/home screen state — what the user sees and hears when nothing is happening
3. Design voice activation flow — always-listening wake word vs. button press (consider false activation risks)
4. Design for physical limitations: large buttons, shake/tremor tolerance, no complex gestures
5. Design cultural and language localisation: avoid Western-centric icons, support RTL scripts, culturally appropriate defaults
6. Define onboarding flow for the elderly user (guided by family member, voice-led setup)

**Checklist:**
- [ ] Minimum tap target size defined (≥ 72px recommended)
- [ ] All screens pass WCAG AA contrast minimum
- [ ] Wake word selected and false-activation rate target defined
- [ ] Tremor/shake tolerance specced (e.g., ignore inputs < X ms or < Y pixel movement)
- [ ] Culturally specific UI decisions documented per supported language group
- [ ] Onboarding flow requires zero reading ability from the elderly user

**Acceptance Criteria:**
- [ ] User can complete any core task (call, reminder check, medication acknowledgement) in ≤ 3 voice commands
- [ ] App is fully operable with screen off (voice only)
- [ ] No feature requires the user to type

---

## PHASE 6 — Security Model

**Steps:**
1. Design voice biometric authentication: enrolment, verification, confidence thresholds, liveness detection
2. Design PIN fallback: 4–6 digit, lockout policy, family reset mechanism
3. Define data encryption standards: at rest (device storage) and in transit (TLS 1.3 minimum)
4. Define what happens on repeated failed authentication attempts
5. Define family account access controls (which family members can change which settings)

**Checklist:**
- [ ] Voice biometric enrolment steps documented (minimum samples, quality gate)
- [ ] PIN fallback flow documented including reset path
- [ ] Encryption standards documented for all data categories
- [ ] Failed authentication lockout policy defined
- [ ] Role-based access for companion app defined (e.g., admin vs. view-only family member)

**Acceptance Criteria:**
- [ ] Voice auth cannot be bypassed without PIN
- [ ] Health and personal data encrypted at rest and in transit
- [ ] Family members cannot access raw health data without explicit user consent configured at setup

---

## PHASE 7 — Tech Stack Recommendations

**Steps:**
1. Recommend a full tech stack for each layer, with justification:
    - Mobile client (React Native / Flutter / native)
    - Backend (language, framework, hosting)
    - AI/ML (STT model, LLM, voice biometrics, intent classification)
    - Real-time config push (Firebase / WebSocket / other)
    - Health integrations (HealthKit, Health Connect SDKs)
    - Media (YouTube API, TTS engine)
    - Auth and security
2. For each AI/ML component, specify: cloud vs. on-device, model size, latency, and fallback
3. Identify open-source vs. commercial components and flag licensing considerations

**Checklist:**
- [ ] Every system component from Phase 1 architecture has a named technology assigned
- [ ] On-device vs. cloud decision documented per AI component
- [ ] Licensing and cost implications flagged for all commercial APIs
- [ ] No component left as "TBD"

**Acceptance Criteria:**
- [ ] Recommended stack is achievable by a team of 3–5 engineers
- [ ] All components have active maintenance and community/vendor support
- [ ] Stack supports both iOS and Android without duplicate codebases where possible

---

## FINAL DELIVERABLE CHECKLIST

Before concluding, confirm all of the following have been produced:

- [ ] System architecture diagram (described in full)
- [ ] Voice model pipeline spec
- [ ] Intent taxonomy (40+ commands)
- [ ] Emergency response state machine
- [ ] Remote config schema and push flow
- [ ] Full tech stack with justifications
- [ ] UX principles and accessibility spec
- [ ] Security model
- [ ] Open questions log — anything that requires a human decision before build can begin

---

**Execution Note:** If any phase cannot be completed due to missing information, list the specific missing inputs required, propose reasonable default assumptions, and proceed with those assumptions clearly stated. Do not stall — flag and continue.