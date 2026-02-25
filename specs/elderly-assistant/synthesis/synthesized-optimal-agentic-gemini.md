# SYNTHESIZED OPTIMAL AGENTIC SPEC: AI Assistant for Elderly Non-English Speaking Users

**Execution Mode:** Sequential Phase Execution, Evidence-Gated, Adversarially Reviewed
**Orchestration Principle:** This prompt combines the sequential stability of artifact generation with strict, tiered evidence requirements and adversarial self-correction. No assumption may be presented as fact.

---

## 1. NORTH STAR & OBJECTIVES
**Goal:** Design an implementation-ready AI Assistant for elderly non-English speaking users. The system must provide voice-first daily routine support, health monitoring, and communication, while allowing full remote configuration by caregivers.
**Success Criteria:** High accessibility, offline resilience, zero-hallucination emergency flows, and strict privacy controls.

---

## 2. AGENT PERSONAS (The Committee)
You will simulate a committee of experts. For each section of your output, explicitly state which persona(s) are driving the design.
*   **Planner (`PLAN`):** Drives sequencing, scope control, and artifact generation.
*   **Systems Architect (`ARCH`):** Defines service boundaries, APIs, data flows, and offline strategy.
*   **ML/Voice Engineer (`ML`):** Designs STT/TTS pipelines, dialect tolerance, and biometrics.
*   **Health & Safety (`HEALTH`):** Manages emergency escalation, clinical thresholds, and HealthKit/Health Connect integration.
*   **UX/Accessibility (`UX`):** Ensures WCAG compliance, elderly-friendly interaction patterns, and localized cultural design.
*   **Security & Privacy (`SEC`):** Owns threat modeling, consent flows, and caregiver authentication.
*   **The Critic (`CRITIC`):** Adversarial reviewer responsible for finding failure modes, challenging assumptions, and forcing simplification.

---

## 3. THE EVIDENCE & CONFIDENCE ENGINE (Strict Rules)
You must separate **FACTS** from **ASSUMPTIONS**. Every major architectural or safety decision must include a structured Confidence Block.

### Evidence Tiers
*   **Tier 1 (Authoritative):** Official API docs, HIPAA/GDPR text, published ML benchmarks (e.g., WER scores).
*   **Tier 2 (Strong):** Vendor specifications, WCAG guidelines, established design patterns.
*   **Tier 3 (Speculative):** Logical derivations, assumed user behavior.

### Confidence Scoring (0-100)
Any decision scoring below **75** must be flagged as a **High Risk Assumption**.

**Required YAML Format for Key Decisions:**
```yaml
decision: "Brief description"
owning_persona: "ARCH | ML | SEC"
confidence_score: 85
evidence_tier: 1
evidence_source: "e.g., Apple HealthKit Background Delivery Docs"
rejected_alternative: "What was considered and why it was rejected"
```

---

## 4. TOOL GATES (Execution Blockers)
You must conceptually pass these gates before finalizing the design. If you lack real-time search, you must state exactly what evidence you *would* retrieve to pass the gate.
*   **Gate 1 (Platform Constraints):** Must prove background execution for continuous voice/health monitoring is viable on iOS/Android.
*   **Gate 2 (Safety/Emergency):** Must define false-positive mitigation and consent models before designing emergency dialing.
*   **Gate 3 (Voice Feasibility):** Must define how the system handles offline/low-connectivity voice commands.

---

## 5. REQUIRED ARTIFACTS (The Output)
Your final output must be a single, cohesive document containing the following artifacts, generated in this exact order.

### Phase 1: Foundation (Driven by `PLAN` & `UX`)
*   **A1. Product Definition & Personas:** Core constraints and 3 distinct elderly personas.
*   **A2. Core Use Cases & MVP Scope:** Strict limit of 8-10 MVP features (Reminders, Calling, Calendar, Health Alerts, Remote Config).

### Phase 2: Architecture & AI (Driven by `ARCH` & `ML`)
*   **A3. Logical Architecture:** Component diagram description, data flows, and on-device vs. cloud processing boundaries.
*   **A4. Voice Pipeline Design:** STT/TTS selection, multilingual/dialect approach, and offline command fallback. *Must include a Decision YAML for the STT approach.*
*   **A5. Remote Configuration System:** How caregiver settings sync to the device instantly.

### Phase 3: Safety & Security (Driven by `HEALTH` & `SEC`)
*   **A6. Emergency Escalation State Machine:** Step-by-step flow from health anomaly detection to caregiver/emergency notification. *Must include a Decision YAML for false-positive mitigation.*
*   **A7. Security & Privacy Model:** Threat model, biometric fallback (PIN), and data encryption standards.

### Phase 4: Execution & Review (Driven by `PLAN` & `CRITIC`)
*   **A8. Implementation Roadmap:** 8-12 week MVP plan with tech stack recommendations.
*   **A9. The Critic's Review:** `CRITIC` must explicitly attack the proposed architecture. Identify 3 major failure modes in the design and propose concrete simplifications.
*   **A10. Open Questions & Assumptions Log:** A strict list of all Tier 3 assumptions that require real-world validation before coding begins.

---

## 6. EXECUTION INSTRUCTIONS
Begin execution immediately. Proceed sequentially from Phase 1 to Phase 4. Do not skip any artifacts. Ensure all Key Decisions use the required YAML format. Embrace the `CRITIC` persona fiercely at the end.