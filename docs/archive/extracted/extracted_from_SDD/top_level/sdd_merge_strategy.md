# SDD Unified Framework: Merge Strategy

## 1. Executive Summary

This document outlines the step-by-step strategy for merging the `sdd/` and `sdd-2/` directories into a new, unified framework named `sdd_unified/`. The strategy is based on the analysis and recommendations presented in the `sdd_framework_comparison.md` document.

The core principle is to adopt the flexible **capability model** from `sdd-2` as the foundational architecture while retaining the prescriptive **process model** from `sdd` as a high-level, user-facing abstraction.

**This plan does not involve modifying the original `sdd/` or `sdd-2/` directories.** It exclusively details the creation and population of the new `sdd_unified/` directory.

## 2. Unified Directory Structure

The `sdd_unified/` directory will be structured to reflect the new, synthesized model. It prioritizes clarity by separating the core orchestration engine from the high-level workflows and examples.

```
sdd_unified/
├── ARCHITECTURE.md
├── PLAYBOOK.md
│
├── agents/
│   └── roles/
│       ├── architect.yaml
│       ├── ba.yaml
│       ├── coder.yaml
│       ├── le.yaml
│       └── pe.yaml
│
├── core/
│   ├── commands/
│   │   ├── architect/
│   │   │   └── design-solution.yaml
│   │   ├── ba/
│   │   │   └── define-requirements.yaml
│   │   ├── coder/
│   │   │   └── implement-feature.yaml
│   │   ├── feature/
│   │   │   └── init.yaml
│   │   ├── le/
│   │   │   └── create-plan.yaml
│   │   └── pe/
│   │       └── review-design.yaml
│   └── templates/
│       └── feature.manifest.yaml.template
│
├── docs/
│   ├── advanced_guides/
│   │   ├── index.md  // Placeholder for advanced orchestration patterns
│   │   └── adr/
│   │       └── ADR-001-Code-Generation-Strategy.md
│   └── getting_started/
│       ├── index.md // Placeholder for tutorial content
│       └── feature_development_workflow.md
│
└── use_cases/
    └── examples/
        └── feature-001-user-authentication/
            ├── .sdd-manifest.yaml
            ├── design/
            │   ├── l1_architecture.md
            │   └── l2_component_design.md
            ├── implementation/
            │   └── l3_plan.md
            ├── review/
            │   ├── l1_review_auto.md
            │   └── l1_review_human.md
            └── spec/
                ├── requirements.md
                └── spec.md
```

## 3. Step-by-Step Merge Plan

The following steps should be executed in order to populate the `sdd_unified/` directory.

### Step 1: Create the Root Directory Structure

- Create the main `sdd_unified/` directory.
- Create the following subdirectories inside `sdd_unified/`:
  - `agents/roles/`
  - `core/commands/`
  - `core/templates/`
  - `docs/advanced_guides/adr/`
  - `docs/getting_started/`
  - `use_cases/examples/`

### Step 2: Copy Core Architectural and Foundational Files

- **ARCHITECTURE.md**: Copy [`sdd/ARCHITECTURE.md`](sdd/ARCHITECTURE.md) to [`sdd_unified/ARCHITECTURE.md`](sdd_unified/ARCHITECTURE.md).
- **Agents**: Copy the entire [`sdd/agents/roles/`](sdd/agents/roles/) directory to [`sdd_unified/agents/roles/`](sdd_unified/agents/roles/).
- **Commands**: Copy the entire [`sdd/commands/`](sdd/commands/) directory to [`sdd_unified/core/commands/`](sdd_unified/core/commands/).
- **Templates**: Copy the entire [`sdd/templates/`](sdd/templates/) directory to [`sdd_unified/core/templates/`](sdd_unified/core/templates/).

### Step 3: Consolidate Documentation and Playbooks

- **Create Unified PLAYBOOK.md**: Create a new file at [`sdd_unified/PLAYBOOK.md`](sdd_unified/PLAYBOOK.md). This file will synthesize the concepts from both playbooks:
  - It will introduce the core capability model (from `sdd-2`).
  - It will present the "feature-development" workflow as the primary, high-level use case (from `sdd`).
  - It will guide users to the `docs/` for detailed tutorials and advanced patterns.
- **Merge Documentation**:
  - Copy [`sdd/docs/ADR-001-Code-Generation-Strategy.md`](sdd/docs/ADR-001-Code-Generation-Strategy.md) to [`sdd_unified/docs/advanced_guides/adr/ADR-001-Code-Generation-Strategy.md`](sdd_unified/docs/advanced_guides/adr/ADR-001-Code-Generation-Strategy.md).
  - Create a new file [`sdd_unified/docs/getting_started/feature_development_workflow.md`](sdd_unified/docs/getting_started/feature_development_workflow.md) that is a slightly edited version of `sdd/PLAYBOOK.md`, framed as a tutorial.
  - Create placeholder files `index.md` in `sdd_unified/docs/advanced_guides/` and `sdd_unified/docs/getting_started/`.

### Step 4: Relocate Example Feature

- **Copy and Rename Feature**: Copy the [`sdd/features/feature-001-user-authentication-example/`](sdd/features/feature-001-user-authentication-example/) directory to [`sdd_unified/use_cases/examples/feature-001-user-authentication/`](sdd_unified/use_cases/examples/feature-001-user-authentication/). This move reframes the feature as a specific *example* of a *use case* rather than a core part of the framework itself.

### Step 5: Identify Obsolete Files (To Be Excluded)

The following files and directories from `sdd/` and `sdd-2/` are now considered obsolete and **should not be copied** to `sdd_unified/`:

- `sdd/PLAYBOOK.md` (Superseded by `sdd_unified/PLAYBOOK.md` and `docs/getting_started/feature_development_workflow.md`)
- `sdd-2/PLAYBOOK.md` (Superseded by `sdd_unified/PLAYBOOK.md` and `docs/advanced_guides/`)
- `sdd/features/` (The concept is replaced by `sdd_unified/use_cases/`)
- `sdd-2/` (The entire directory is conceptually merged, and its identical assets are sourced from `sdd/` for simplicity).
- All other miscellaneous documentation and research files in `sdd/docs/` and `sdd/research/` are not part of the core framework and are excluded from this merge plan.

## 4. Final Verification

Upon completion of these steps, the `sdd_unified/` directory will represent the complete, merged framework, ready for further development and use. The structure aligns with the strategic recommendations, providing a clear separation between the core engine, high-level abstractions, and concrete examples.