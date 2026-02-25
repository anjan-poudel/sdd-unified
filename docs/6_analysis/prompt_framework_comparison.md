# Comparative Analysis of AI Agent Specification Frameworks

This document provides a detailed comparison of three distinct prompt engineering frameworks designed to orchestrate LLMs or multi-agent systems in generating a complex System Design Document for an Elderly AI Assistant. The frameworks analyzed are **Claude (`@specs/elderly-assistant/claude/**`)**, **Codex/GPT (`@specs/elderly-assistant/codex/**`)**, and **DeepSeek (`@specs/elderly-assistant/deepseek/**`)**.

---

### 1. Core Overlaps (The Commonalities)

*   **Product Vision:** All three aim to specify a voice-first, highly accessible application featuring daily routine management, health/emergency monitoring, and remote caregiver configuration.
*   **Safety & Reliability Focus:** All frameworks heavily prioritize offline degradation, clear emergency escalation flows, explicit consent models, and high system availability.
*   **Agentic Methodology:** The advanced versions of all three prompts utilize a **multi-agent / persona-driven** approach (e.g., Architects, UX, QA, Security) to simulate cross-functional expertise.
*   **Evidence-Based Execution:** All frameworks strictly forbid the LLM from passing off assumptions as facts. They implement mandatory "Gates" to enforce validation, testing, and evidence collection before finalizing a design step.

---

### 2. Key Differences in Orchestration & Design

| Feature | Claude Docs (`claude-4.6*`) | Codex/GPT Docs (`gpt-5.2*`) | DeepSeek Docs (`advanced-agentic*`) |
| :--- | :--- | :--- | :--- |
| **Execution Flow** | **State-Machine & Parallel:** DAG flow. Phases run sequentially, branch into parallel tracks, and require "Dependency Handshakes" to merge. | **Strictly Sequential:** Linear step-by-step execution plan (S1 to S9) building out specific sections of a final document. | **Enterprise DAG & Governance:** Similar to Claude but adds Triad/Pair review requirements, exception handling, and granular merge tracking. |
| **Agent Orchestration** | **Orchestrator-Led:** Uses an `ORCH` agent that governs gates, enforces rules, and handles conflict resolution. | **Committee-Led:** Acts as a "committee" guided by a `Planner` role, operating collaboratively. | **Highly Regulated Orchestration:** `ORCH` enforces strict escalation matrices, risk limits, and mandatory peer-review protocols. |
| **Validation & Gating** | **Quantitative:** Explicit Confidence Scores (0-100). Tool gates mandate concrete actions (e.g., "Must retrieve WCAG 2.2 docs"). | **Qualitative:** Conceptual PASS/FAIL gates (e.g., Safety Gate) focused on verifying the completeness of the thought process. | **Weighted & Tiered:** Introduces Evidence Tiers (Tier 1 to 4 with multipliers), Level 1-3 tool gate failure protocols, and strict minimum evidence counts. |
| **Conflict Resolution** | **Algorithmic:** Hardcoded priority matrix: *Safety > Accessibility > Technical Feasibility > Cost*. | **Adversarial:** Relies on a `Critic` agent to perform adversarial reviews and propose simplifications. | **Multi-Level Escalation:** Agent → Pair Review → ORCH → Human Arbitration, heavily relying on YAML Decision Logs. |
| **Deliverable Structure** | **Checklist & Phase Outcomes:** Granular checklist items and acceptance criteria met per feature phase. | **Comprehensive Artifacts:** Focuses on generating 10 specific deliverables (A1-A10) for a cohesive document. | **Structured YAML & Volumes:** Heavily utilizes YAML templates for logging decisions/evidence, culminating in an 8-Volume final package. |

---

### 3. Pros and Cons

#### Claude Workflow (`claude-4.6-advanced.md`)
**Pros:**
*   **Unambiguous Accountability:** Confidence Scores (0-100) and "Evidence Packages" make it highly resistant to LLM hallucination.
*   **Robust Conflict Resolution:** The weighted decision matrix allows the system to autonomously break ties without human intervention.
*   **Realistic Workflow:** Modeling parallel work streams closely mirrors real-world Specification-Driven Development (SDD).

**Cons:**
*   **High Context Overhead:** Maintaining continuous schemas and Decision Logs consumes a large amount of token context.
*   **Brittle Execution:** Strict routing ("0-49 = Hard stop") means the LLM might frequently halt execution if it cannot retrieve specific API docs.

#### Codex/GPT Workflow (`gpt-5.2-advanced-autonomous-workflow.md`)
**Pros:**
*   **Highly Cohesive Output:** Focusing on pre-defined Artifacts (A1-A10) produces a polished, highly readable System Design Document.
*   **Self-Correction:** The dedicated `Critic` role forces the LLM into self-reflection, often catching over-engineered solutions.
*   **Execution Stability:** The linear, sequential plan is easier for an LLM to follow reliably in a single thread without losing track of state.

**Cons:**
*   **Risk of Confident Hallucination:** Qualitative gates rely heavily on the LLM's internal knowledge weights, which can lead to plausible but hallucinated technical claims.
*   **Less Actionable Verification:** Lacks explicit mandates to use search tools for benchmarking data.

#### DeepSeek Workflow (`advanced-agentic.md`)
**Pros:**
*   **Ultimate Enterprise Rigor:** The Tiered Evidence System and Risk Management Framework provide the highest level of auditability and traceability.
*   **Machine-Readable State:** Heavy reliance on YAML templates for Open Questions, Decision Logs, and Evidence Packages makes it highly parsable for external orchestrator scripts (like `sdd-unified`).
*   **Comprehensive Risk Management:** Explicit handling of exception protocols and tiered escalations ensures safety-critical systems are heavily scrutinized.

**Cons:**
*   **Extreme Cognitive Load:** The sheer volume of rules, matrices, tiers, and required YAML schemas is highly likely to exhaust context windows or cause instruction-following degradation in all but the most capable reasoning models.
*   **Agent Paralysis:** Mandatory Triad approvals and high Tier-1 evidence requirements will almost certainly cause execution deadlocks if the agents lack robust, unhindered web access.

---

### Summary Conclusion

*   **Use the Codex/GPT approach** for single-shot, long-context prompt sessions where you need a comprehensive, highly readable, and logically sound end-to-end architecture document quickly.
*   **Use the Claude approach** if you are building an automated, multi-agent pipeline where different LLM calls handle different phases, and you need programmable circuit-breakers to prevent the agents from going off the rails.
*   **Use the DeepSeek approach** strictly within a highly scaffolded execution environment (like a sophisticated Python orchestrator that parses intermediate YAML outputs) for mission-critical, enterprise-grade systems where exhaustive auditability, strict evidence weighting, and formal risk management are legally or operationally required.