# SDD Frameworks: Comparative Analysis and Unification Strategy

## Executive Summary

A thorough analysis of the `sdd/` and `sdd-2/` directories reveals that they are not two distinct frameworks, but rather **two different conceptual models for the same underlying system**. The foundational components—architecture, agent definitions, and command structures—are identical.

The core divergence lies in their operational philosophy and documentation:

1.  **`sdd` (The Process Framework):** Presents a **prescriptive, linear, process-centric** model. Its playbook guides users through a rigid, step-by-step workflow for the primary use case of feature development. It prioritizes clarity and ease of use for a single, well-defined task.
2.  **`sdd-2` (The Capability Framework):** Presents a **flexible, abstract, capability-centric** model. Its playbook describes a system of composable agents that can be orchestrated to perform multiple, complex use cases (e.g., reverse-engineering, code generation), moving beyond the single-feature workflow.

This document recommends a unification strategy that embraces the powerful, flexible **capability model of `sdd-2` as the core architecture** while packaging the clear, linear **process model of `sdd` as a default, "getting-started" orchestration pattern**. This synthesis will create a unified framework that is both powerful and approachable.

---

## Part 1: The Core Insight — Process vs. Capability

The initial goal was to analyze the differences between two frameworks. However, the investigation uncovered a more fundamental truth: there is only one framework, but it is described in two different ways.

*   `sdd/` describes a **Process**: a fixed sequence of steps to achieve a specific outcome. It answers, "What is the process for creating a feature?"
*   `sdd-2/` describes a **Capability**: a set of tools and patterns that can be combined in various ways to achieve multiple outcomes. It answers, "What are the capabilities of this system?"

This is the foundational conceptual difference. `sdd-2` is a conceptual reframing of `sdd`, revealing the underlying system's potential as a flexible orchestration engine rather than just a single-purpose feature factory.

## Part 2: Comparative Analysis

### 2.1. Architectural Foundation (`ARCHITECTURE.md`)

*   **Finding:** The `ARCHITECTURE.md` files are **identical**.
*   **Analysis:** Both frameworks are built on the exact same 5-layer architecture (Analysis, Specification, Code Generation, Review, Orchestration). They share the same agent types, communication protocols, and state management concepts.
*   **Conclusion:** The conceptual divergence is not at the architectural level. The core blueprint is shared and stable.

### 2.2. Operational Philosophy (`PLAYBOOK.md`)

*   **Finding:** The `PLAYBOOK.md` files are **conceptually divergent**.
*   **`sdd/PLAYBOOK.md`:**
    *   **Focus:** A rigid, sequential, multi-level design workflow (`init` → `define` → `design-l1` → `review-l1`...).
    *   **Abstraction:** Models a production line for a single feature.
    *   **User Experience:** Clear, easy to follow, but inflexible.
*   **`sdd-2/PLAYBOOK.md`:**
    *   **Focus:** A collection of use cases and orchestration patterns (`Reverse Engineering`, `Code Generation from Spec`, `End-to-End Orchestration`).
    *   **Abstraction:** Models a toolkit of composable capabilities.
    *   **User Experience:** Powerful, flexible, but requires a deeper understanding of the system's components.
*   **Conclusion:** The playbooks represent the entire conceptual split. `sdd` documents a single *instance* of a workflow, while `sdd-2` documents the *engine* that can run multiple workflows.

### 2.3. Structural Implementation (`agents/` and `commands/`)

*   **Finding:** The `agents/` and `commands/` directory structures and contents are **identical**.
*   **Analysis:** This is the critical piece of evidence. Both frameworks use the same set of role-based agents (`architect`, `coder`, etc.) and the same role-organized command structure (`commands/architect/design-solution.yaml`).
*   **Conclusion:** This proves the divergence is purely conceptual and not structural. The `sdd-2` playbook describes a more advanced way to *use* the existing commands and agents; it does not introduce new ones. The rigid command structure is a low-level building block used by both models.

## Part 3: Recommendation for a Unified Framework

The goal is to merge the two conceptual models into a single, cohesive framework that leverages the strengths of both.

### Guiding Principle for Unification
From a first-principles perspective, a system should be designed with a **flexible, powerful core** and provide **simple, high-level abstractions** for common use cases. Complexity should be opt-in.

### Recommended Architecture

1.  **Core Engine: The Capability Model (`sdd-2`)**
    *   Adopt the `sdd-2` philosophy as the fundamental architecture. The core of the unified framework should be an **orchestration engine** that operates on abstract concepts: agents, artifacts, and composable patterns. This provides maximum power and flexibility.

2.  **User-Facing Abstraction: The Process Model (`sdd`)**
    *   Retain the clear, linear workflow from `sdd` as a **default, pre-packaged orchestration pattern** called `"feature-development"`.
    *   This pattern will be the primary entry point for new users, offering the simplicity of the original `sdd` framework. It will be implemented as a high-level composition of the core engine's capabilities.
    *   Advanced users can bypass this default pattern and interact directly with the core orchestration engine to create custom workflows, as envisioned by `sdd-2`.

3.  **Unified Documentation**
    *   Create a single, authoritative documentation set.
    *   The "Core Concepts" or "Architecture" section should describe the flexible capability model of the orchestration engine.
    *   A "Getting Started" or "Tutorials" section should walk users through the default "feature-development" workflow, providing a simple on-ramp.
    *   An "Advanced Guides" section should document how to create custom orchestration patterns, fulfilling the promise of the `sdd-2` playbook.

### Justification from First Principles

*   **Single Level of Abstraction:** This approach enforces a clean separation between the low-level abstraction of the orchestration engine and the high-level abstraction of a user-facing workflow. The `feature-development` workflow will be a client of the core engine, not intertwined with it.
*   **Simplicity and Scalability:** The system remains simple for the most common task (the `sdd` model) but scales to handle arbitrary complexity by allowing direct access to the core engine (the `sdd-2` model).
*   **Clarity and Adaptability:** The unified model is clear for beginners and adaptable for experts. It avoids imposing the cognitive overhead of the full orchestration engine on users who just want to build a feature, while still providing that power when needed.