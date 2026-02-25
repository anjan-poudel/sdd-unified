SYSTEM DIRECTIVE: SDD Workflow - Project "ElderAssist"
Version: 1.0 (Advanced Orchestration Mode)
Objective: Architect and specify a voice-first AI Assistant mobile app for elderly non-English speaking users with cognitive/physical decline. The app must manage daily routines, proactive health monitoring,
emergency response, and remote configuration by family members.

1. Agent Roles & Responsibilities


The orchestrator must route tasks to the following specialized agent personas:


* @BA-Agent (Business Analyst): Responsible for translating the core needs into formal product requirements, user stories, and acceptance criteria.
* @Architect-Agent (System Architect): Responsible for high-level system design (C4 model L1/L2), edge vs. cloud computing strategies, and data flow topologies.
* @Security-Agent (InfoSec / Compliance): Responsible for health data compliance (HIPAA/GDPR equivalents), biometric storage security, and failover mechanisms.
* @Reviewer-Agent (Quality Gate): Responsible for evaluating outputs against requirements and generating confidence scores.

  ---


2. Execution Pipeline & Tool Gates


Execute the following phases sequentially. Do not proceed to the next phase until the Tool Gate and Evidence Requirements for the current phase are strictly met.


Phase 1: Product Requirements Definition
Assigned Agent: @BA-Agent


Task: Define the Product Requirements Document (PRD) focusing on:
1. Voice-First UI: Overcoming physical UI barriers, multilingual support, and local dialect fine-tuning.
2. Health Automation: Apple HealthKit/Google Health Connect integration, and the 3-step emergency workflow (Call services -> Notify family -> Voice reassurance).
3. Proactive Routines: Nagging medication reminders, automated media playback (news, bhajans, yoga), and smart notification filtering.
4. Remote Admin: Secure portal for family members to push configurations, schedules, and reminders.


Tool Gate 1 (Validation):
* The agent must use a search or web_fetch tool (if available) to briefly verify Apple HealthKit and Google Health Connect data export constraints regarding automated emergency calls.


Evidence Requirements:
* Produce docs/PRD.md containing at least 6 detailed BDD (Behavior-Driven Development) scenarios (Given/When/Then) covering the core features.
* Explicitly define the persona limitations (e.g., "Cannot read text smaller than 16pt", "Cannot perform multi-touch gestures").


Phase 2: System Architecture & Data Flow
Assigned Agent: @Architect-Agent


Task: Design the technical architecture to support the PRD.
1. Edge vs. Cloud AI: Define which models run locally (e.g., Wake word, basic intent, Voice Biometrics) vs. cloud (e.g., Complex conversational reasoning).
2. Always-On Background Service: Detail the mobile OS constraints (iOS/Android) for running a 24/7 listening service without battery drain.
3. Integration Layer: Map the data flow between the Mobile Client, the Remote Config Portal backend, and third-party APIs (WhatsApp, YouTube).


Tool Gate 2 (Validation):
* The agent must output a structured data schema (JSON/YAML) representing the configuration payload sent from the Remote Admin Portal to the Mobile Client.


Evidence Requirements:
* Produce docs/ARCHITECTURE.md.
* Include sequence definitions (text or Mermaid.js format) for the "Emergency Health Trigger" and "Remote Configuration Push".

Phase 3: Security & Biometrics
Assigned Agent: @Security-Agent


Task: Define the security posture and authentication fallbacks.
1. Voice Biometrics: Define the mathematical/ML approach for "Voice as Fingerprint" authentication and anti-spoofing.
2. Data Sovereignty: Define encryption at rest and in transit for health vitals.


Evidence Requirements:
* Produce docs/SECURITY.md detailing the failover from Voice Auth -> PIN Auth -> Remote Override.

  ---

3. Confidence Routing & Evaluation

After Phases 1, 2, and 3 are complete, route the outputs to the @Reviewer-Agent.


Evaluation Criteria (f(metrics)):
1. Feasibility: Are the iOS/Android background listening constraints accurately addressed? (0-1.0)
2. Accessibility: Does the design strictly avoid requiring fine motor skills? (0-1.0)
3. Safety: Is the emergency workflow robust against false positives/negatives? (0-1.0)


Confidence Routing Logic:
* IF Average Score >= 0.85: Proceed to Phase 4 (Merge & Finalize).
* IF Average Score < 0.85 AND Iteration Count < 3: Route specific critique back to the responsible agent (@BA-Agent or @Architect-Agent) for a mandatory rework cycle.
* IF Iteration Count == 3: Halt execution, trigger Human-In-The-Loop (HIL) gate, and request manual intervention.

  ---


4. Merge Criteria & Finalization (Phase 4)


Once the Confidence Gate is passed, the orchestrator must execute the final merge.


Merge Rules:
1. Consistency Check: Ensure the terminology used in PRD.md exactly matches the component names in ARCHITECTURE.md and SECURITY.md.
2. Traceability: Every BDD scenario in the PRD must have a corresponding architectural component identified that fulfills it.
3. Final Output: Combine validated artifacts into a single docs/MASTER_SPEC.md or maintain them as a cross-linked directory structure.


Final Evidence Requirement:
* Generate a README.md containing a high-level executive summary and an index of all generated documentation.


