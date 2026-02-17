# A Real-World Example: Building a Feature with SDD V2

This document walks through a real-world developer experience of using the Specification-Driven Development (SDD) V2 framework. It demonstrates the seamless, automated, and spec-first workflow that makes V2 so powerful.

Our developer, Alex, has been tasked with adding a dark mode toggle to a web application.

---

### Part 1: The Initial Spark - From Prompt to Automated Specification

Alex's journey begins not with creating files or writing boilerplate, but with a single, clear instruction to the SDD V2 framework.

**1. A Single Command**

Alex types one command in the terminal:

```bash
/feature "Add a dark mode toggle button to the main navigation bar that persists the user's choice"
```

*(Note: The prompt is slightly more descriptive to guide the AI to generate a more complete feature from the start.)*

**2. Automated Orchestration**

Immediately, the `Orchestrator Agent` takes over. Alex watches as the system provides real-time feedback:

```
[Orchestrator] Initiating new feature: "Add a dark mode toggle button..."
[Orchestrator] Reading PLAYBOOK.md...
[Orchestrator] Executing stage: define
[Orchestrator] Running Business Analyst Agent...
[Business Analyst] Analysis complete. requirements.md created.
[Orchestrator] Stage 'define' PASSED. Artifacts created in spec/.
```

So far, the framework has generated the complete specification, creating the following structure:

```
features/dark-mode-toggle/
└── spec/
    └── requirements.md
```

---

### Part 2: The Multi-Level Design & Review Process

With the requirements defined, the workflow moves into the new, three-tiered design phase.

#### Phase 2.1: L1 High-Level Design & Review

First, the high-level architecture is established.

**1. Automated L1 Design**

The `Orchestrator` invokes the `Architect` to create the L1 design.

```
[Orchestrator] Executing stage: design --level 1
[Orchestrator] Running Architect Agent...
[Architect] L1 Design complete. L1_architecture.md created.
[Orchestrator] Stage 'design --level 1' PASSED. Artifacts created in design/.
[Orchestrator] Design generated successfully. Awaiting L1 design review.
[Orchestrator] Please review the documents in `design/`. The artifacts highlight new additions (green), modifications (yellow), and unchanged sections (grey) to aid your review.
[Orchestrator] Run `/feature review-design --level 1 --action approve` to continue or `/feature provide-feedback "your feedback"`.
```

**2. Human-in-the-Loop: L1 Review**

The `Principal Engineer` reviews the `L1_architecture.md`. The anemic, color-coded diffs make it easy to see exactly what the agent is proposing. The architecture looks solid. The PE approves it.

```bash
/feature review-design --level 1 --action approve
```

#### Phase 2.2: L2 Service-Level Design & Review

With the high-level architecture approved, the `Orchestrator` proceeds to the more detailed L2 design.

**1. Automated L2 Design**

The `Lead Engineer` agent is responsible for breaking down the architecture into service-level components.

```
[Orchestrator] L1 design approved by user.
[Orchestrator] Executing stage: design --level 2
[Orchestrator] Running Lead Engineer Agent...
[Lead Engineer] L2 Design complete. L2_components.md created.
[Orchestrator] Stage 'design --level 2' PASSED. Artifacts updated in design/.
[Orchestrator] Awaiting L2 design review.
[Orchestrator] Run `/feature review-design --level 2 --action approve` to continue.
```

**2. Human-in-the-Loop: L2 Review**

The `Principal Engineer` now reviews the `L2_components.md`. The green and yellow highlights show how the new dark mode service will interact with the existing UI components. It's a clean design.

```bash
/feature review-design --level 2 --action approve
```

#### Phase 2.3: L3 Detailed Design & Review

Finally, the process moves to the most granular level of design, preparing for implementation.

**1. Automated L3 Design**

The `Developer` agent creates the detailed implementation plan.

```
[Orchestrator] L2 design approved by user.
[Orchestrator] Executing stage: design --level 3
[Orchestrator] Running Developer Agent...
[Developer] L3 Design complete. L3_plan.md created.
[Orchestrator] Stage 'design --level 3' PASSED. Artifacts updated in design/.
[Orchestrator] Awaiting L3 design review.
[Orchestrator] Run `/feature review-design --level 3 --action approve` to continue.
```

**2. Human-in-the-Loop: L3 Review**

The `Lead Engineer` reviews the `L3_plan.md`. It clearly outlines the functions to be created, the CSS classes to be added, and the `localStorage` logic. It's ready for coding.

```bash
/feature review-design --level 3 --action approve
```

The final design directory now looks like this:

```
features/dark-mode-toggle/
├── spec/
│   └── requirements.md
└── design/
    ├── L1_architecture.md
    ├── L2_components.md
    └── L3_plan.md
```

---

### Part 3: Automated Implementation

With all three levels of design formally approved, the `Orchestrator` proceeds to the implementation stage.

```
[Orchestrator] L3 design approved by user.
[Orchestrator] Executing stage: implement
[Orchestrator] Running Coder Agent...
[Coder] Implementation complete. Code generated in src/ with localStorage persistence.
[Orchestrator] Stage 'implement' PASSED.
```

Without any further intervention, the framework has now created the first draft of the implementation code:

```
features/dark-mode-toggle/
└── src/
    ├── toggle-button.js
    ├── toggle-button.css
    └── index.html
```

---

### Part 4: Human-in-the-Loop: Code Review

The framework is designed for automation, but it knows that human oversight on the final code is critical. The `Orchestrator Agent` pauses again for a code review.

**1. The Review Prompt**

```
[Orchestrator] First draft generated successfully.
[Orchestrator] Awaiting code review.
[Orchestrator] Please review the code in `src/`.
[Orchestrator] Run `/feature code-review approve` to continue or `/feature provide-feedback "your feedback"`.
```

**2. The Review and Feedback**

The reviewer inspects the generated files and provides feedback to make an implicit requirement explicit in the spec.

```bash
/feature provide-feedback "The use of localStorage is a good choice, but this requirement should be explicit in the spec. Please update spec/requirements.md."
```

---

### Part 5: The "Spec-First" Iteration Loop and Final Approval

The feedback triggers the iteration loop, starting with an update to the specification.

**1. The Change: Edit the Specification**

Alex opens `spec/requirements.md` and adds the new requirement.

```markdown
# Updated spec/requirements.md
- A toggle button shall be present in the main navigation bar.
- Clicking the button shall toggle a 'dark-mode' class on the `<body>` element.
- The user's theme preference (light or dark) **shall be saved to `localStorage` to persist across sessions.**
- On page load, the saved preference shall be applied automatically.
```

**2. The Action: Trigger the Update**

```bash
/feature update
```

**3. The Magic: Intelligent, Cached Regeneration and Re-review**

The `Orchestrator Agent` re-evaluates the workflow.

```
[Orchestrator] Initiating update for feature: "dark-mode-toggle"
[Orchestrator] Reading PLAYBOOK.md...

[Orchestrator] Executing stage: define
[Orchestrator] CACHE HIT. Skipping 'define' stage.

[Orchestrator] Executing stage: design --level 1
[Orchestrator] CACHE HIT. Skipping 'design --level 1' stage.

[Orchestrator] Executing stage: design --level 2
[Orchestrator] CACHE HIT. Skipping 'design --level 2' stage.

[Orchestrator] Executing stage: design --level 3
[Orchestrator] CACHE MISS. Specification has changed. Re-running 'design --level 3' stage.
[Orchestrator] Running Developer Agent...
[Developer] L3 Design updated.
[Orchestrator] Awaiting L3 design review...
```

Here, the `Orchestrator` intelligently re-ran only the affected design stage (`L3`) because the change in `requirements.md` was granular enough not to affect L1 or L2. After a quick approval (`/feature review-design --level 3 --action approve`), the `implement` stage is re-run.

```
[Orchestrator] Executing stage: implement
[Orchestrator] Running Coder Agent...
[Coder] Veryfying implementation based on updated spec...
[Coder] No code changes needed. Implementation already matches spec.
[Orchestrator] Stage 'implement' PASSED.

[Orchestrator] Implementation verified. Re-submitting for code review.
[Orchestrator] Run `/feature code-review approve`.
```

The reviewer sees the spec is comprehensive and the code is correct, and approves the feature.

```bash
/feature code-review approve
```
The workflow is complete.