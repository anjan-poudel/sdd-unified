
Role: You are an expert Software Architect and AI Product Manager.


Task: Design a comprehensive system architecture and product specification for an AI Assistant mobile application tailored for elderly users from non-English speaking backgrounds.


Context & Target Audience:
- Users: Elderly parents who find modern smartphones overwhelming due to language barriers, unfamiliar UI symbolism, cognitive decline (e.g., memory loss), or physical limitations (e.g., shaking hands).
- Primary Goal: Provide a frictionless, voice-first interface that helps them manage daily routines, monitor their health, consume media (YouTube, WhatsApp), and stay connected with family without needing to
  navigate complex app interfaces.

Core Functional Requirements:


1. Voice-First Interaction (Primary UI):
    - Users must be able to use voice commands to check calendars, make calls, send texts, and ask for help/instructions on using their phone.
    - AI Voice Model: Must support regional non-English dialects out of the box. It must also include a localized fine-tuning pipeline to adapt to the specific user's accent, speech nuances, and pacing using
      initial voice samples.


2. Health Monitoring & Emergency Response:
    - API Integrations: Bidirectional data sync with Apple HealthKit and Google Health Connect.
    - Automated Emergency Workflows: If critical vitals breach a threshold (e.g., severe blood pressure spike), the system must autonomously:
        1. Call emergency services.
        2. Dial and notify pre-nominated emergency contacts (children, spouse).
        3. Provide continuous voice reassurance to the elderly user that help is on the way.


3. Daily Routines & Proactive Assistance:
    - Nagging Reminders: Persistent, proactive voice and text reminders for wake-up, complex medication schedules, meals, and exercise.
    - Automated Media: Automatically play scheduled audio/video content (e.g., morning news, devotional music/bhajans, guided yoga videos).
    - Notification Management: Intelligently filter and read aloud only important messages and notifications.


4. Remote Configuration & Management (Critical Feature):
    - Remote Admin Portal: Family members (children) must be able to remotely configure the app, push schedules, set reminders, and adjust settings from their own devices to remove the technical burden from
      the elderly user.
    - Local Config: Basic configuration should still be accessible in-app.


5. Operational & Security Constraints:
    - Runtime: Must run reliably 24/7 as an always-on background service.
    - Authentication: Use Voice Biometrics ("voice as fingerprint") as the primary authentication method, with a standard PIN as a fallback.


Required Output:
Please provide a detailed technical and product breakdown addressing the requirements above. Your response must include:
1. High-Level System Architecture: Mobile client components, backend services, AI/ML model deployment strategy, and external API integrations.
2. User Experience (UX) Strategy: How to design the "always-listening" paradigm and UI minimalism for users with physical and cognitive limitations.
3. Data Flow & Security: How sensitive health data, voice biometrics, and remote configurations will be managed, stored, and transmitted securely.
4. Implementation Roadmap: A phased approach to building the MVP (Minimum Viable Product).

  ---


Why this rewrite works better for LLMs:
* Persona Assignment: It gives the LLM a clear role ("Expert Software Architect and AI Product Manager") which sets the tone and depth of the response.
* Structured Categorization: It breaks down your bullet points into logical domains (Voice, Health, Routines, Config, Security). LLMs parse heavily structured text much better than stream-of-consciousness
  text.
* Explicit Output Expectations: The "Required Output" section forces the LLM to structure its final answer exactly how you want it, rather than guessing what parts of the prompt to focus on.

> please create aa second version optimized for “agentic LLM execution” (with explicit steps, acceptance criteria, and checklists).
✦ Here is a version specifically optimized for Agentic LLM Execution.


This version is structured as a formal directive with explicit tasks, constraints, context, and verifiable acceptance criteria. This format prevents an autonomous agent from getting "lost in the weeds" and
forces it to deliver specific, actionable artifacts one step at a time.

  ---


Copy and paste the following prompt to your Agentic LLM:

  ---

SYSTEM DIRECTIVE: AI Assistant for Elderly Users (System Design & Architecture)


Role: Autonomous AI Product Architect & Systems Engineer
Objective: Produce a complete System Design Document (SDD) and Product Requirements Document (PRD) for a specialized AI Assistant mobile application.


Context & Target Audience
- Target User: Elderly parents from non-English speaking backgrounds experiencing cognitive decline, memory loss, and physical limitations (e.g., shaking hands).
- Primary Problem: Modern smartphones rely heavily on complex UI symbolism, fine motor skills, and text navigation, making them overwhelming and inaccessible.
- Core Value Proposition: A frictionless, voice-first, always-on AI assistant that manages daily routines (health, schedules), facilitates communication (WhatsApp), consumes media (YouTube), and provides
  automated emergency response.

  ---


Task 1: Product Requirements Document (PRD)


Instructions: Define the core features, user stories, and constraints of the application.


Required Features to Detail:
1. Voice-First & Multilingual Interaction:
    - Must support regional non-English dialects out of the box.
    - Requires a local fine-tuning pipeline to learn the specific user's accent, speech nuances, and pacing via initial voice samples.
    - Must allow the user to control the phone entirely by voice (e.g., "Check my calendar", "Call my son", "Read my messages").
2. Health Monitoring & Emergency Automation:
    - Bidirectional sync with Apple HealthKit / Google Health Connect.
    - Autonomous emergency workflow: If critical vitals (e.g., severe blood pressure) breach thresholds, the app must 1) Call emergency services, 2) Dial pre-nominated family contacts, 3) Provide continuous,
      reassuring voice feedback that help is on the way.
3. Proactive Daily Routines:
    - Persistent, proactive voice and text reminders for wake-up, complex medication schedules (nagging reminders), meals, and exercise.
    - Automated media playback (e.g., morning news, devotional music/bhajans, guided yoga videos at predefined times).
    - Intelligent notification filtering (reading aloud only important messages).
4. Remote Configuration (Critical):
    - A remote web/app portal allowing family members to configure the device (pushing schedules, setting reminders, adjusting settings) to remove the technical burden from the elderly user.
    - In-app local configuration must also be available.
5. Security & Authentication:
    - The app must run 24/7 as an always-on background service.
    - Primary authentication must be Voice Biometrics ("voice as fingerprint").
      Acceptance Criteria for Task 1:
- [ ] PRD includes distinct sections for Voice UI, Health Automation, Routine Management, Remote Admin, and Security.
- [ ] At least 5 explicit User Stories are defined detailing the interaction between the elderly user, the AI, and the remote family member.
- [ ] Explicit constraints regarding language models, latency, and offline capabilities are documented.

  ---

Task 2: High-Level System Architecture & Component Design


Instructions: Design the technical architecture required to fulfill the PRD.


Required Architectural Components to Detail:
1. Mobile Client Architecture (iOS/Android): How the always-on listening service, voice activity detection (VAD), and local UI rendering will function without draining the battery.
2. AI/ML Pipeline:
    - Strategy for deploying Small Language Models (SLMs) locally on the device for fast, offline intent recognition versus routing complex queries to a cloud LLM.
    - Strategy for the voice-cloning/tuning pipeline to adapt to the user's accent.
3. Backend & Integration Layer:
    - Architecture of the Remote Configuration Portal (database, push notification/sync mechanism to the mobile client).
    - Integration strategy for Apple HealthKit / Google Health Connect.
    - Integration strategy for third-party apps (WhatsApp, YouTube).
4. Data Flow & Security Architecture:
    - How sensitive health data and voice biometric prints are stored, encrypted, and transmitted.


Acceptance Criteria for Task 2:
- [ ] Architecture document clearly separates On-Device (Edge) processing from Cloud processing.
- [ ] A logical data flow diagram or sequence description is provided for the "Emergency Health Trigger" workflow.
- [ ] A logical data flow diagram or sequence description is provided for the "Remote Configuration Push" workflow.
- [ ] Explicit technology stack recommendations are provided for the mobile framework, backend, and AI models.

  ---

Task 3: Implementation Roadmap


Instructions: Break down the execution of this system into a phased MVP roadmap.


Acceptance Criteria for Task 3:
- [ ] Roadmap is divided into 3 distinct phases: Phase 1 (Core Voice & Routines MVP), Phase 2 (Health & Emergency Automation), Phase 3 (Remote Config & Advanced Media).
- [ ] Each phase lists 3-5 specific, actionable engineering tasks.
- [ ] A specific list of critical technical risks and proposed mitigations is included.

  ---


Execution Protocol:
Execute Task 1, Task 2, and Task 3 sequentially. Do not summarize; provide the full, detailed technical documentation for each task. Use Markdown formatting with clear headers, bullet points, and checklists.


