# SDD V2 Architecture: Automated, Spec-First Development

This document outlines the architecture for the "V2" of the Specification-Driven Development (SDD) framework. This next-generation design introduces a powerful, automated workflow centered around a "spec-first" philosophy, intelligent caching, and a new Orchestrator Agent.

## 1. Core Principles of SDD V2

The V2 framework is designed to address the key feedback from the initial version, focusing on three primary goals:

1.  **Automation & Intuition**: Radically simplify the developer experience by replacing the manual, multi-step slash-command workflow with a single, high-level entry point.
2.  **Spec as the Single Source of Truth**: Enforce a strict "spec-first" principle, where the specification documents are the only editable artifacts. All changes to the implementation must originate from the spec.
3.  **Efficiency & Optimization**: Introduce an intelligent caching mechanism to avoid redundant work, ensuring that only the steps affected by a spec change are re-executed.

## 2. The Orchestrator Agent: The Heart of V2

At the core of the SDD V2 framework is the new **Orchestrator Agent**. This high-level agent is responsible for automating the entire feature-generation lifecycle, transforming the developer experience from a manual process into a guided, automated journey.

### 2.1. Workflow Initiation

The entire workflow is triggered by a single command:

```
/feature "A high-level description of the new feature."
```

This command invokes the Orchestrator Agent, which takes the high-level requirement and initiates the process defined in the `PLAYBOOK.md`.

### 2.2. Automated, Playbook-Driven Execution

The Orchestrator reads the `PLAYBOOK.md` file to understand the sequence of operations. It then automatically calls the required specialist agents in the correct order: `define` -> `Design L1` -> `Review L1` -> `Design L2` -> `Review L2` -> `Design L3` -> `Review L3` -> `implement` -> `code-review` -> `approve`.

The Orchestrator manages the flow, waiting for a `[SUCCESS]` or `[FAILURE]` signal from each agent before proceeding. If any step fails, the Orchestrator halts the process and reports the failure, allowing the developer to intervene.

### 2.3. Human-in-the-Loop (HITL) Integration

The V2 framework retains the critical principle of human oversight. The Orchestrator enforces mandatory **Human-in-the-Loop** review and approval steps at key stages.

#### Design & Review Cycles (L1-L3)

The single `design` and `design-review` stages are replaced by a three-level iterative process.

*   **L1 Design & Review (High-Level Architecture)**
    > This is like an artist's rendering of a new building; it shows what it will look like from the outside and its place in the city. It sells the vision.
    *   **Author**: `Architect`
    *   **Reviewers**: `Principal Engineer`, `Lead Engineer`, `Business Analyst`
    *   **Process**: After the `Design L1` stage, the Orchestrator pauses for an explicit `/feature review-design --level 1 {approve|reject}` command.
    *   **Outcome**: On rejection, the developer must update the L1 design specifications.

*   **L2 Design & Review (Service-Level Interactions)**
    > This is like an architect's blueprint. It shows floor plans, where the rooms are, how they connect, and where the main electrical and plumbing systems will run.
    *   **Author**: `Principal Engineer`
    *   **Reviewers**: `Lead Engineer`, `Architect`
    *   **Process**: After the `Design L2` stage, the Orchestrator pauses for an explicit `/feature review-design --level 2 {approve|reject}` command.
    *   **Outcome**: On rejection, the developer must update the L2 design specifications.

*   **L3 Design & Review (Detailed Design)**
    > This is like the detailed schematic for the electrician and plumbers, showing exactly which wires and pipes go where.
    *   **Author**: `Lead Engineer`
    *   **Reviewers**: `Principal Engineer`, `Developer`
    *   **Process**: After the `Design L3` stage, the Orchestrator pauses for an explicit `/feature review-design --level 3 {approve|reject}` command.
    *   **Outcome**: On rejection, the developer must update the L3 design specifications.

**Code Review (`code-review`)**:
-   **Trigger**: Occurs after the `implement` stage.
-   **Reviewer**: `Lead Engineer (LE)` is mandatory. For features flagged as complex, a `Principal Engineer (PE)` review can also be optionally triggered.
-   **Process**: The orchestrator will notify the designated reviewers and wait for a `/feature code-review {approve|reject}` command.
-   **Outcome**:
    -   `[APPROVED]`: The workflow proceeds to the final `approve` step.
    -   `[CHANGES_REQUESTED]`: The developer must update the relevant specification file and re-run `/feature update` to regenerate the implementation.

### 2.4. Command Model for Reviews

To support the multi-level review process, the command model is updated as follows:

*   `/feature review-design --level {1|2|3} --action {approve|reject}`: Used by designated reviewers to approve or reject a design at a specific level.
*   `/feature code-review {approve|reject}`: Used by the Lead Engineer to approve or reject the implementation.

This ensures that architectural and implementation decisions are validated and that the developer maintains control over the final product.

## 3. The "Spec-First" Update Loop

The most significant philosophical shift in V2 is the strict enforcement of the **"Spec-First" Update Loop**. This principle establishes the specification as the immutable source of truth for the entire feature.

### 3.1. The `spec/` Directory: The Source of Truth

For any given feature, the `spec/` and `design/` directories (containing `requirements.md`, `l1_architecture.md`, etc.) are the primary artifacts. These files define the intended behavior and structure of the feature.

### 3.2. How to Make Changes

If a developer needs to modify the behavior or implementation of a feature, they **must not** edit the generated code in the `src/` directory directly. Any direct code modifications will be overwritten.

Instead, the correct workflow is:

1.  **Edit the Specification**: The developer modifies the relevant specification file(s) (e.g., `spec/requirements.md` or `design/l1_architecture.md`).
2.  **Re-run the Orchestrator**: The developer then re-runs the orchestrator with an `update` command:
    ```
    /feature update
    ```

The Orchestrator will then re-execute the workflow, applying the changes from the updated specification.

## 4. Intelligent Caching for Optimized Regeneration

To make the "Spec-First" update loop efficient, the Orchestrator Agent implements an **intelligent caching mechanism**. This ensures that only the necessary steps are re-executed when a specification changes.

### 4.1. The Caching Mechanism

1.  **Hash Calculation**: Before executing any step in the playbook (e.g., `implement`), the Orchestrator calculates a cryptographic hash of all the relevant input artifacts for that step. For the `implement` step, this would include the L1, L2, and L3 design documents.
2.  **Cache Storage**: This hash is stored in a `.cache` file located within the feature's directory (e.g., `features/feature-001/.cache`). The cache file maps the step name to the input hash and the path to the output artifacts.
3.  **Cache Check**: On subsequent runs (e.g., after a `/feature update`), the Orchestrator re-calculates the hash of the input artifacts for the current step.
4.  **Skip or Execute**:
    *   If the new hash **matches** the one stored in the `.cache` file, the Orchestrator **skips** the step entirely and uses the cached output artifacts from the previous successful run.
    *   If the new hash **does not match**, it signifies that the specification has changed. The Orchestrator then **executes** the step, generates new output artifacts, and updates the `.cache` file with the new hash.

### 4.2. Example Caching Scenario

Consider a scenario where a developer updates the `design/l2_service_interactions.md` but does not change `design/l1_architecture.md`.

-   When the `/feature update` command is run, the Orchestrator will re-run the workflow.
-   The hash for the `Design L1` step's inputs will match the cache, so the `Design L1` step is **skipped**.
-   The hash for the `Design L2` step's inputs will have changed, so the `Design L2` step is **re-executed**. Subsequent steps (`Review L2`, `Design L3`, etc.) will also be executed.

This intelligent caching dramatically speeds up the development cycle by focusing only on the work that needs to be done.

## 5. Visual Change Indicators

To aid reviewers in understanding the impact of changes, generated design artifacts (documents and diagrams) will use a visual language to indicate the status of components and interactions.

*   **Green:** New component or interaction.
*   **Yellow:** Modified component or interaction.
*   **Grey:** Unchanged component or interaction.

This system provides an at-a-glance summary of what has changed between revisions, enabling more focused and efficient reviews.

## 6. V2 Automated Workflow Diagram

The following Mermaid diagram illustrates the new, automated workflow managed by the Orchestrator Agent, including the multi-level design loops.

```mermaid
graph TD
    subgraph "SDD V2 Automated Workflow"
        A[Start: /feature "requirement"] --> B{Orchestrator Agent};
        B --> C(Execute stage: define);
        C --> D{Check Cache};
        D -- Hash Match --> D_OUT[Use Cached Output];
        D -- Hash Mismatch --> D_RUN[Run BA Agent];
        D_RUN --> D_GEN(Generate requirements.md);
        D_GEN --> D_OUT;
        
        D_OUT --> L1_Design(Execute stage: Design L1);
        L1_Design --> L1_Cache{Check Cache};
        L1_Cache -- Hash Match --> L1_Out[Use Cached Output];
        L1_Cache -- Hash Mismatch --> L1_Run[Run ARCH Agent];
        L1_Run --> L1_Gen(Generate L1 design);
        L1_Gen --> L1_Out;
        L1_Out --> L1_Review(Execute stage: Review L1);
        L1_Review --> L1_Gate{PE/LE/BA Review};
        L1_Gate -- Changes Requested --> L1_Loop(dev: Edit L1 design);

        L1_Gate -- Approved --> L2_Design(Execute stage: Design L2);
        L2_Design --> L2_Cache{Check Cache};
        L2_Cache -- Hash Match --> L2_Out[Use Cached Output];
        L2_Cache -- Hash Mismatch --> L2_Run[Run PE Agent];
        L2_Run --> L2_Gen(Generate L2 design);
        L2_Gen --> L2_Out;
        L2_Out --> L2_Review(Execute stage: Review L2);
        L2_Review --> L2_Gate{LE/ARCH Review};
        L2_Gate -- Changes Requested --> L2_Loop(dev: Edit L2 design);

        L2_Gate -- Approved --> L3_Design(Execute stage: Design L3);
        L3_Design --> L3_Cache{Check Cache};
        L3_Cache -- Hash Match --> L3_Out[Use Cached Output];
        L3_Cache -- Hash Mismatch --> L3_Run[Run LE Agent];
        L3_Run --> L3_Gen(Generate L3 design);
        L3_Gen --> L3_Out;
        L3_Out --> L3_Review(Execute stage: Review L3);
        L3_Review --> L3_Gate{PE/DEV Review};
        L3_Gate -- Changes Requested --> L3_Loop(dev: Edit L3 design);

        L3_Gate -- Approved --> R(Execute stage: implement);
        R --> S{Check Cache};
        S -- Hash Match --> T[Use Cached Output];
        S -- Hash Mismatch --> U[Run LE/CODE Agents];
        U --> V(Generate src/ code);
        V --> T;
        T --> W(Execute stage: code-review);
        W --> X{LE/PE Code Review};
        X -- Changes Requested --> Spec_Loop(dev: Edit spec/*.md);
        X -- Approved --> Z_approve(Execute stage: approve);
        Z_approve --> Z[End];
    end

    subgraph "Spec-First Update Loop"
        L1_Loop -- edits --> Y_update(dev: /feature update);
        L2_Loop -- edits --> Y_update;
        L3_Loop -- edits --> Y_update;
        Spec_Loop -- edits --> Y_update;
        Y_update --> B;
    end

    style B fill:#bbf,stroke:#333,stroke-width:2px
    style L1_Loop fill:#f9f,stroke:#333,stroke-width:2px
    style L2_Loop fill:#f9f,stroke:#333,stroke-width:2px
    style L3_Loop fill:#f9f,stroke:#333,stroke-width:2px
    style Spec_Loop fill:#f9f,stroke:#333,stroke-width:2px
    style Y_update fill:#f9f,stroke:#333,stroke-width:2px