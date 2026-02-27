## which one do you recommend and why?

⏺ Having read both carefully, here is my honest assessment:
                                                                                                                                                                                                                 
---                                                                                                                                                                                                              
### Recommendation: Codex synthesis — with one addition from Claude

#### Why codex wins on structure and principles

1. Confidence-as-advisory is the right call (most important difference)
   My Claude version uses confidence scores as hard routing gates (85+ = proceed). This is a known failure mode — LLMs reliably inflate self-reported confidence to pass gates. The codex correctly identifies this
   and uses evidence-based tool gates as the primary progression mechanism, with confidence as an informational signal only. This matches how the sdd-unified project itself works: evidence over assertion.

2. The CRITIC agent fills a genuine gap
   My version has QA but no adversarial pass. The codex's CRITIC role — explicitly tasked with failure-mode analysis and simplification — catches over-engineering and false feasibility claims that all other
   agents are incentivised to overlook. This is the most practically valuable addition.

3. MVP scope guardrail prevents a common failure
   "Max 10 core user stories" in Phase 0 is a concrete guardrail against the most common LLM failure in this kind of prompt: producing an exhaustive wish-list instead of a scoped MVP. My version has no equivalent
   control.

4. Leaner structure is more reliably executable
   6 phases vs. 8 phases. Codex consolidates without losing coverage. Lighter prompts produce more consistent outputs across different LLMs — less machinery to get lost in.

  ---
### Where Claude synthesis is better

Sub-phase granularity (3A–D) is the one thing worth keeping
Codex merges voice+UX together and doesn't decompose feature specs into sub-domains. Claude's 3A (Reminders), 3B (Health/Emergency), 3C (Comms), 3D (Media) forces each domain to be fully specified
independently. This matters because health/emergency and daily reminders have very different acceptance criteria, risk profiles, and agent ownership — merging them loses precision. The codex loses this.

Tiered evidence weighting is more rigorous, but optional
Claude's Tier 1/2/3/4 with multipliers gives agents a clear framework for what counts as strong evidence. Useful for high-stakes runs; too much machinery for everyday use.

  ---
### Bottom line

Use the codex version as your base. Add Claude's sub-phase decomposition (3A–D) for the feature specs section. Drop the rest of Claude's governance overhead.

The single most important principle the codex gets right that mine doesn't: evidence gates drive progression, not confidence scores. That one decision makes the codex prompt significantly more reliable in
practice.
