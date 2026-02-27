# ElderAssist AI — Design Brief (Human Version)

**Version:** 1.0
**Date:** 2026-02-26
**Audience:** Human designers, architects, product managers, and engineers
**Purpose:** A plain-language version of the full system design brief for the ElderAssist AI mobile application.

---

## What We're Building and Why

We want to build a voice-first AI assistant for elderly parents who find smartphones overwhelming. These are people who want to stay connected with their families, manage their health, and enjoy entertainment — but struggle because modern smartphone interfaces assume English literacy, fine motor control, and familiarity with app conventions that many elderly people simply don't have.

The assistant should feel like having a patient, knowledgeable helper always nearby: one that speaks their language, remembers their routine, watches out for their health, and never judges them for asking the same question twice.

Family members — usually adult children living elsewhere — need to be able to set everything up and keep it running remotely, without burdening their parents with configuration tasks.

---

## Who We're Designing For

Think through at least three realistic users. For each, be specific: what language do they speak and what regional dialect? What health conditions do they live with? What does their typical day look like? What would they actually try to use the app for, and what would happen if the app wasn't there?

**User 1 — Elderly parent living alone.** Moderate memory decline, limited English, relies entirely on family for any phone help. Missing a medication dose or a health alert could be life-threatening.

**User 2 — Elderly couple sharing a device.** Both have low digital confidence. One manages the phone for both. They mainly want to play devotional music, watch bhajans on YouTube, and video-call their children. They share reminders and emergency contacts.

**User 3 — Elderly parent at home during the day while family is at work.** Unsupervised for eight or more hours. No one nearby to notice if something goes wrong. Health monitoring, proactive check-ins, and the ability to escalate to family quickly are essential.

---

## What We're NOT Building

Be explicit about scope. Unless someone specifically asks for these:

- We are not replacing WhatsApp, YouTube, or Facebook — we are providing voice-controlled access to them.
- We are not training a custom speech model from scratch. We should adapt existing multilingual ASR/TTS systems to the user's voice and accent.
- We are not building a medical diagnostic tool. The system can read health data from the phone's health platform and trigger alerts, but it makes no clinical judgements.

---

## Design Principles (Non-Negotiable)

These constraints must hold throughout the entire design. When something conflicts with them, they take priority in this order: **safety first, then accessibility, then technical feasibility, then cost**.

1. **Voice is the primary interface.** Every core task — reminders, calls, messages, calendar queries, media — must be completable by voice alone. The visual UI exists as a fallback for users who want it, not as a requirement.

2. **Family should be able to run the app remotely.** A caregiver using a companion web or mobile app must be able to change reminders, update emergency contacts, adjust health thresholds, and configure media playlists — and those changes should appear on the elderly user's device within 60 seconds.

3. **The app must speak the user's language.** Support at least three non-English languages with real regional dialect tolerance (not just language family — actual dialects). The voice and interface should feel natural to someone who has never learned to use a smartphone in English.

4. **The interface must work for impaired users.** Large tap targets, high contrast, no complex gestures, tremor tolerance. A user with shaking hands and moderate cognitive decline should be able to use this without frustration.

5. **The app must be reliably available.** Approximate 24/7 availability. Be honest about where iOS and Android impose limits on background execution, and design specifically around those limits rather than ignoring them.

6. **Emergency actions must never fire accidentally.** Before the app calls emergency services or sends emergency alerts, it must give the user a chance to confirm or cancel. False positives could cause serious harm — panic, unnecessary ambulance calls, loss of trust. Design every emergency flow with this in mind.

7. **Voice authentication is a convenience feature, not a security layer.** The app should use voice recognition to identify the user, but voice alone is not sufficient for high-stakes actions. A PIN fallback is mandatory.

---

## What the System Must Do

### Daily Routine and Reminders
The app should proactively remind the user about their daily routine. Wake-up, medication (with persistent, escalating reminders that won't stop until acknowledged), meals, exercise, and bedtime. Medication reminders in particular should never be silently dismissible — if the user doesn't respond, the family should be notified.

The user should be able to say things like "Did I take my morning tablets?" and get a clear answer. All reminder schedules should be configurable remotely by family.

### Health Monitoring and Emergency Response
Connect to Apple HealthKit and Google Health Connect to read health metrics — blood pressure, heart rate, blood glucose, SpO2. When a reading crosses a configured threshold, the app should first ask the user if they are okay, give them a few seconds to respond, and then — if there's no response or they confirm something is wrong — automatically call emergency services, notify family contacts in priority order, and speak reassuring messages to the user ("Help is on the way").

This flow must work even when the screen is off or the app is running in the background. It must be impossible to trigger with a spoofed voice command.

### Communication
The user should be able to make calls, send messages, and hear their important notifications — all by voice. They should be able to say "Call my son" or the equivalent in their language, and the app should understand and act. Notifications should be filtered so only important ones are read aloud, not every app badge.

### Entertainment and Scheduled Media
Play devotional music, yoga videos, and news briefings at scheduled times, and on demand by voice. The family should be able to configure playlists remotely. Entertainment must yield immediately to medication reminders and emergency events — it should never block something important.

### Remote Configuration
The family companion app (web and mobile) is a first-class part of this product, not an afterthought. Family members need to be able to manage the elderly user's schedule, contacts, health thresholds, media content, and language settings without touching the elderly user's device directly. Every configuration change must be auditable — who changed what, when.

---

## How to Approach the Design Work

Work through these areas in order. Don't move to the next area until you've satisfied the acceptance conditions for the current one.

### 1. Lock the scope first
Before designing anything, decide: which platforms (iOS, Android, both)? Which languages and dialects specifically? What are the compliance obligations for the target geography (HIPAA, GDPR, local equivalents)? And critically — list the MVP user stories, capped at ten. Each story should be specific enough that you can write a test for it.

### 2. Design the full system architecture
Map out every major component: the mobile app, the backend, the AI and voice pipeline, the health integration layer, the notification system, the caregiver companion app. Be explicit about which parts run on the device versus in the cloud, and why. Define what happens when the network is unavailable — for every major feature, not just in general terms. No integration point should be left as "TBD."

### 3. Design the voice and language pipeline (can be done in parallel with 4, 5, 6)
Choose a base speech-to-text model and justify it with published accuracy data for accented and elderly speech. Describe how you will adapt it to the individual user's voice and dialect. Map out every intent the system needs to understand — aim for at least 40 distinct command types across all feature areas, with natural language examples in each supported language. Define what happens when the system doesn't understand — how it asks for clarification, when it gives up, and how it falls back to PIN entry.

### 4. Design the remote configuration system (can be done in parallel with 3, 5, 6)
The config schema must be versioned and fully auditable. Define the push pipeline — how does a change made on the companion app reach the device within 60 seconds? What happens if the device is offline when the change is pushed? What happens if the family member and the elderly user both make conflicting changes simultaneously? Who can see what — not all family members should have the same level of access.

### 5. Design the UX and accessibility layer (can be done in parallel with 3, 4, 6)
Define the visual and interaction principles. Minimum tap target sizes, font sizes, contrast ratios. How does the app behave when nothing is happening — what does the user see and hear? Resolve the wake-word question: always-listening (with false activation risk) or button-press (with motor control demands)? Design for users who physically cannot perform fine motor gestures. Think carefully about cultural context — icons and metaphors that are obvious in one culture can be confusing or offensive in another. Every screen should meet WCAG 2.2 AA contrast requirements.

### 6. Design the security model (can be done in parallel with 3, 4, 5)
Define the voice biometric enrollment process — how many samples, what quality threshold, how does the system re-enroll if accuracy degrades over time? Define the PIN fallback in detail: lockout policy, how a family member can reset it, how to prevent social engineering attacks on the reset process. Map every compliance obligation — HIPAA, GDPR, or local equivalents — to a specific implementation decision. "We assume we're compliant" is not acceptable. Model the threat scenarios: what happens if someone impersonates the elderly user? What if a malicious family member abuses caregiver access? What if the device is stolen?

### 7. Design each feature area in detail (after architecture is settled)
Work through each feature domain separately — reminders, health and emergency, communications, media. Each has different risk levels. The emergency response system deserves the most careful attention: draw out the full state machine, every state, every transition, every exit condition. Verify it works under all realistic failure conditions (calls that don't connect, contacts who don't answer, device in background). The reminder engine needs a clear escalation model. Communications needs a contact alias system that works in the user's native language.

### 8. Recommend technology choices
For each layer of the system — mobile framework, backend, AI/ML components, config push, health APIs, media — recommend a specific technology and explain why. For each AI component, be explicit about whether it runs on-device or in the cloud, what model or library you're recommending, what the latency target is, and what the fallback is if it's unavailable. Check licensing for every open-source component. Estimate development and ongoing operational costs.

### 9. Define the MVP and roadmap
Identify the smallest version of this product that demonstrates the core value: voice control, medication reminders, emergency flow, and remote configuration. Map an 8–12 week delivery plan with milestones, the team roles needed, and the priority order for the backlog. Then sketch what Phase 2 looks like — advanced health integration, speaker personalisation, smarter notification filtering.

---

## Key Decisions to Document

For every major architectural, safety, or technology decision, write down:

- **What you decided** — briefly
- **Why** — what evidence or reasoning supports it
- **What you considered instead** — the alternatives and why you rejected them
- **What breaks if you're wrong** — the downstream consequences if this decision turns out to be incorrect

At minimum, document decisions on: which STT model to use, where the on-device/cloud boundary sits, how emergency false positives are mitigated, which voice biometric approach to use, and how the config push mechanism works.

---

## Before You Finalise Each Area — Verify These

These are the things most likely to cause real-world failure if left unchecked:

- **Background execution**: Have you confirmed that iOS and Android actually allow the background behaviour your design requires? Both platforms have significant restrictions. Document the specific APIs and strategies you're relying on.
- **Health API capabilities**: Have you confirmed what HealthKit and Health Connect actually expose? Not all health metrics are available, not all devices report in real time. Your emergency flow must be designed around what these APIs actually do.
- **STT accuracy on real users**: Have you found published benchmark data for your chosen STT model on accented or elderly speech? A model that performs well on broadcast English may fail badly on the actual users this app serves.
- **Emergency calling legality and availability**: Is programmatic emergency calling actually available in the target regions? This varies significantly by country. Document what fallback exists where it isn't.
- **Security and compliance**: Have you looked up the actual regulatory requirements for the target regions rather than assuming? Map each obligation to a specific implementation decision.
- **Accessibility standards**: Have you pulled the WCAG 2.2 AA requirements and platform-specific elderly UX guidelines? Don't design from memory.

If you can't satisfy any of these, say so explicitly, state the assumption you're working with instead, and flag the risk level.

---

## Challenge Your Own Design

Before you finish, put on an adversarial hat and attack what you've designed. Don't be diplomatic.

**Identify three specific failure modes.** Not vague risks like "voice recognition might fail" — specific scenarios. What happens when a user with a heavy accent tries to trigger an emergency in a noisy kitchen and the system misunderstands them? What happens if the caregiver app pushes a config change that conflicts with something the elderly user just set locally? Be concrete about what fails, under what conditions, and what the consequence is for the elderly user.

**Identify three things that are over-engineered.** What have you designed that adds complexity without proportionate value for the MVP? What could be simplified or cut for the first version without meaningfully reducing quality?

**Identify three assumptions you've treated as facts.** Claims made in the design that have no strong published evidence behind them. For each, say how you'd validate the assumption before building starts.

After identifying these, either revise the design or make an explicit, reasoned case for why the identified issues are acceptable as-is.

---

## What to Deliver

When you're done, the output should include:

1. **Product definition** — problem statement, design principles, and the three user personas
2. **System architecture** — component diagram description, service boundaries, data models, on-device vs. cloud decisions, offline degradation strategy
3. **Voice and AI pipeline** — STT/TTS approach, intent taxonomy (40+ commands with examples), voice biometrics flow, personalisation pipeline
4. **Feature specifications** — reminder escalation flow, emergency response state machine, communication voice commands, media scheduling and interruption priorities
5. **Remote configuration system** — config schema, push pipeline, companion app feature list, audit logging approach
6. **UX and accessibility specification** — design principles, cultural localisation decisions, onboarding flow, WCAG compliance approach
7. **Security model** — authentication design, encryption standards, compliance mapping, threat scenarios and mitigations
8. **Technology recommendations** — full stack with justifications, on-device vs. cloud matrix, licensing notes, cost estimate
9. **MVP plan** — 8–12 week milestone plan, team roles, backlog, Phase 2 roadmap
10. **Test strategy** — how each MVP feature will be tested, including accessibility and real-world usability testing with elderly users
11. **Risk register** — top risks with mitigations and owners
12. **Open questions** — anything that requires a human decision or real-world validation before build begins, with a clear flag for what's blocking and what isn't
13. **Gate results** — for each of the six verification checks above, a clear PASS or FAIL with the evidence, and for any FAIL, what needs to be resolved before proceeding

---

*Keep the output specific and implementation-oriented. Avoid generic advice. Where a choice exists, present the options with trade-off analysis and then make a recommendation. Everything should be concrete enough that an engineer can pick it up and start building.*
