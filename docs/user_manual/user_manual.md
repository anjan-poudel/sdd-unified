# SDD-Unified User Manual

## 1. Introduction

Welcome to the comprehensive user manual for SDD-Unified. This document provides a deep dive into the framework, its architecture, and its practical application in your development workflow.

### What is SDD-Unified?

SDD-Unified is a framework that brings structure, predictability, and rigor to AI-powered software development. It acts as a "steering layer" for AI coding assistants, ensuring they follow a structured, specification-driven development (SDD) process.

By using a system of specialized AI agents, a formal workflow, and iterative reviews, SDD-Unified transforms ad-hoc code generation into a deterministic and verifiable engineering process.

### Who is this for?

This manual is for developers, architects, and team leads who want to:

*   Leverage AI for code generation without sacrificing quality and consistency.
*   Enforce a rigorous, specification-first development process.
*   Automate the creation of high-quality, well-documented, and testable code.
*   Improve collaboration between different roles in the development lifecycle.

### Core Principles

The framework is built on the following principles:

*   **Specification-Driven:** Every piece of code is derived from a clear, unambiguous specification.
*   **Role-Based Specialization:** The development process is broken down into specialized roles, each handled by a dedicated AI agent.
*   **Iterative Design and Review:** The process involves multiple layers of design and review to ensure quality at every stage.
*   **Task-Driven Implementation:** Development is broken down into small, verifiable tasks, each with its own acceptance criteria.
*   **Automation:** The framework automates the workflow, handoffs, and context management between agents.

## 2. Installation and Configuration

### Prerequisites

*   An AI-powered coding assistant that supports custom agents (e.g., Claude Code, Roo Code).
*   A solid understanding of your project's architecture and coding standards.
*   Familiarity with YAML and JSON for configuration.

### Setup Steps

1.  **Copy the Configuration:**
    The first step is to copy the SDD-Unified configuration files into your project.
    ```bash
    mkdir -p /path/to/your/project/.sdd-unified
    cp -r /path/to/sdd-unified/agents /path/to/your/project/.sdd-unified/
    cp -r /path/to/sdd-unified/commands /path/to/your/project/.sdd-unified/
    cp -r /path/to/sdd-unified/templates /path/to/your/project/.sdd-unified/
    ```
    This creates a `.sdd-unified` directory in your project root, containing the definitions for the agents, their commands, and the workflow templates.

2.  **Register the Agents:**
    Next, you need to register the five SDD-Unified agents with your AI coding assistant. Refer to your assistant's documentation for the specific steps, but the general process is to import the agent configuration files located in `.sdd-unified/agents/configs/`.

    The five agents to register are:
    *   `sdd-ba`
    *   `sdd-architect`
    *   `sdd-pe`
    *   `sdd-le`
    *   `sdd-coder`

3.  **Verify the Setup:**
    Ensure that all five agents are available in your AI assistant's agent list. If they are not, double-check the paths and the configuration format required by your tool.

## 3. Core Concepts

Understanding the following core concepts is essential to using SDD-Unified effectively.

### The Five Specialized Agents

SDD-Unified divides the development process among five AI agents, each with a distinct role and expertise.

*   **`sdd-ba` (Business Analyst):** This agent's primary role is to translate user requests and business needs into formal specifications. It creates the initial `requirements.md` and `spec.yaml` files that form the foundation for the rest of the workflow.

*   **`sdd-architect`:** This agent is responsible for the high-level system design. Based on the specifications from the `sdd-ba`, it creates the `l1_architecture.md`, which outlines the overall structure, components, and their interactions.

*   **`sdd-pe` (Principal Engineer):** The `sdd-pe` takes the high-level architecture and creates a more detailed component design. It produces the `l2_component_design.md`, which specifies the internal workings of each component, their APIs, and data structures.

*   **`sdd-le` (Lead Engineer):** This agent is the master planner. It breaks down the component design into a series of small, well-defined implementation tasks. These tasks are written in `l3_plan.md` and include BDD-style acceptance criteria to ensure they are verifiable.

*   **`sdd-coder`:** This is the agent that writes the code. It takes the implementation tasks from the `sdd-le` and generates the source code, tests, and any other required artifacts.

### The Three Layers of Design

The design process in SDD-Unified is structured into three layers, ensuring a gradual and thorough progression from a high-level concept to a detailed implementation plan.

*   **L1: High-Level Architecture:** Created by the `sdd-architect`, this layer defines the macro-level structure of the system.
*   **L2: Component Design:** Developed by the `sdd-pe`, this layer details the internal design of each component.
*   **L3: Implementation Plan:** Produced by the `sdd-le`, this layer consists of the individual tasks for the `sdd-coder`.

### Task-Driven BDD Implementation

Instead of generating a monolithic block of code, the `sdd-coder` works on a series of discrete tasks defined by the `sdd-le`. Each task is accompanied by acceptance criteria in the Gherkin format (Given/When/Then), which provides a clear, verifiable definition of "done" for each task.

This approach offers several advantages:
*   **Clarity:** Each task has a clear and unambiguous goal.
*   **Verifiability:** The BDD criteria make it easy to test and verify each piece of generated code.
*   **Granularity:** It allows for fine-grained progress tracking and makes it easier to isolate and fix issues.

### Iterative Review Cycles

Quality is built into the process through a series of formal review cycles. At the end of each design stage (L1, L2, and L3), the generated artifacts are reviewed by other agents. For example, the L1 architecture is reviewed by the `sdd-ba`, `sdd-pe`, and `sdd-le`.

If a review is rejected, the workflow automatically triggers a "rework" task for the original agent, which must then address the feedback and resubmit its work. This iterative process continues until the design is approved, with built-in circuit breakers to prevent infinite loops.

### Context Management

Seamless handoffs between agents are made possible through a `context.json` file. This file acts as a central manifest for a feature, containing all the key information, decisions, and artifacts generated throughout the workflow. When an agent completes a task, it updates the `context.json`, which is then passed to the next agent in the workflow, ensuring that every agent has the full context of what has been done and why.

## 4. The SDD-Unified Workflow

The SDD-Unified workflow is a structured, multi-stage process that guides a feature from initial concept to final implementation. The following is a detailed breakdown of each step in the standard workflow.

### Step 1: Feature Initialization

A new feature development cycle begins with the creation of a dedicated directory for that feature. This can be done manually or with a helper command.

```bash
mkdir -p features/your-feature-name/{spec,design,implementation,review}
```
This creates a standardized structure to hold all the artifacts that will be generated throughout the workflow.

### Step 2: Requirements Definition

**Agent:** `sdd-ba` (Business Analyst)

The first active agent in the process is the `sdd-ba`. Its job is to take a high-level feature request and transform it into a formal specification.

*   **Input:** A natural language description of the feature.
*   **Process:** The `sdd-ba` analyzes the request, clarifies ambiguities, and defines the functional and non-functional requirements.
*   **Output:**
    *   `spec/requirements.md`: A detailed, human-readable document outlining the requirements.
    *   `spec/spec.yaml`: A machine-readable specification that will be used by the other agents.

### Step 3: High-Level Architecture

**Agent:** `sdd-architect`

With the specification in place, the `sdd-architect` takes over to design the high-level technical solution.

*   **Input:** `spec/spec.yaml`
*   **Process:** The architect designs the overall structure, identifies the key components, and defines their interactions and APIs.
*   **Output:** `design/l1_architecture.md`

### Step 4: L1 Design Review

**Agents:** `sdd-ba`, `sdd-pe`, `sdd-le`

Before proceeding, the high-level architecture must be reviewed. This is a critical quality gate.

*   **Input:** `design/l1_architecture.md`
*   **Process:** Each of the reviewing agents assesses the architecture from its own perspective:
    *   `sdd-ba`: Ensures the design meets the business requirements.
    *   `sdd-pe`: Checks for technical soundness, scalability, and adherence to standards.
    *   `sdd-le`: Evaluates the feasibility of the design for implementation.
*   **Output:** A review file (e.g., `review/l1_review_ba.md`) with a status of "APPROVED" or "REJECTED" with feedback. If rejected, the `sdd-architect` must rework the design.

### Step 5: Component Design

**Agent:** `sdd-pe` (Principal Engineer)

Once the L1 architecture is approved, the `sdd-pe` dives deeper into the technical details of each component.

*   **Input:** `design/l1_architecture.md`
*   **Process:** The `sdd-pe` details the internal logic, data models, class structures, and public interfaces for each component.
*   **Output:** `design/l2_component_design.md`

### Step 6: L2 Design Review

**Agents:** `sdd-architect`, `sdd-le`

Similar to the L1 review, the detailed component design is also subject to a review.

*   **Input:** `design/l2_component_design.md`
*   **Process:**
    *   `sdd-architect`: Ensures the component design aligns with the overall architecture.
    *   `sdd-le`: Assesses the clarity and completeness of the design for implementation planning.
*   **Output:** A review file with an "APPROVED" or "REJECTED" status.

### Step 7: Implementation Planning

**Agent:** `sdd-le` (Lead Engineer)

With a fully approved design, the `sdd-le` creates a step-by-step implementation plan.

*   **Input:** `design/l2_component_design.md`
*   **Process:** The `sdd-le` breaks the component design down into small, discrete implementation tasks. Each task is written with clear, BDD-style acceptance criteria.
*   **Output:** One or more task files in `implementation/tasks/`, (e.g., `task-001.md`).

### Step 8: L3 Plan Review

**Agent:** `sdd-pe`

The implementation plan is reviewed by the `sdd-pe` to ensure it accurately reflects the design and is sufficiently detailed for the coder.

*   **Input:** The task files in `implementation/tasks/`.
*   **Process:** The `sdd-pe` checks if the tasks cover all aspects of the component design and if the BDD criteria are clear and testable.
*   **Output:** A review file with an "APPROVED" or "REJECTED" status.

### Step 9: Code Implementation

**Agent:** `sdd-coder`

This is the stage where code is finally written.

*   **Input:** The implementation tasks from the `implementation/tasks/` directory.
*   **Process:** The `sdd-coder` takes one task at a time and generates the corresponding source code, unit tests, and any other necessary files. The coder's goal is to produce code that satisfies the BDD criteria of the task.
*   **Output:** Source code files in your project's `src` directory (or other configured output path).

### Step 10: Implementation Review

**Agent:** `sdd-le`

Each completed task is reviewed by the `sdd-le`.

*   **Input:** The generated source code for a specific task.
*   **Process:** The `sdd-le` reviews the code for correctness, adherence to coding standards, and fulfillment of the task's BDD criteria.
*   **Output:** A review file. If the code is rejected, the `sdd-coder` will rework it based on the feedback.

### Step 11: Feature Completion

Once all tasks have been implemented and approved, the feature is considered complete. The result is a new piece of functionality in your codebase that has been specified, designed, implemented, and reviewed through a rigorous and automated process.

## 5. Project Scenarios and Best Practices

SDD-Unified is a versatile framework that can be adapted to different project contexts. This section provides specific guidance for using it in greenfield (new) and brownfield (existing) projects, and how to manage the common challenge of specification drift.

### Using SDD-Unified in Greenfield Projects

Starting a new project from scratch is the ideal scenario for SDD-Unified, as you can establish a specification-driven culture from day one.

**Strategy:**

1.  **Foundation First:** Use the SDD-Unified workflow to define the core architectural components of your application *before* writing significant amounts of business logic. This could include setting up the web server, defining the database schema, establishing the authentication layer, and creating the basic CI/CD pipeline.
2.  **Define Core Patterns:** Have the `sdd-architect` and `sdd-pe` agents create and document the primary design patterns that will be used throughout the application (e.g., repository pattern, service layer, dependency injection setup). This creates a reusable and consistent structure for all future features.
3.  **Build Feature by Feature:** Once the foundational infrastructure is in place, use the standard, end-to-end SDD-Unified workflow for every new feature. This ensures that your codebase grows in a structured and predictable way, with a corresponding specification for every piece of functionality.
4.  **Full Workflow:** For greenfield projects, always favor the full, five-agent workflow. The initial investment in a thorough design and review process will pay significant dividends in the long run by ensuring quality and consistency.

### Using SDD-Unified in Brownfield Projects

Integrating a specification-driven approach into an existing project requires a more nuanced strategy. The goal is to introduce the rigor of SDD-Unified without having to re-engineer the entire application at once.

**Strategy:**

1.  **Start with New Features:** The easiest way to introduce SDD-Unified is to apply it only to *new* features. Do not attempt to retroactively create specifications for the entire existing codebase. Instead, let the specification-driven part of your application grow organically over time.
2.  **"Bubble" Context:** For a new feature that needs to interact with the existing (non-specified) codebase, the `sdd-architect`'s first task should be to define the boundaries. The L1 architecture should explicitly document the interfaces between the new, SDD-managed components and the legacy parts of the system. This creates a "bubble" of specification-driven code within the larger application.
3.  **Refactoring as a Feature:** If you need to refactor a part of the legacy codebase, treat the refactoring effort itself as a feature within SDD-Unified.
    *   The `sdd-ba` would define the requirements (e.g., "The user authentication module must be refactored to use our new service pattern.").
    *   The `sdd-architect` would then analyze the existing code and design a new architecture for it.
    *   The rest of the workflow proceeds as normal, resulting in a newly refactored, fully specified component.
4.  **Use the "Lite" Workflow for Minor Changes:** For small changes to the legacy codebase (e.g., bug fixes), the "lite" workflow is often the most practical approach.

### Preventing Specification and Code Drift

"Drift" occurs when the implementation (the code) no longer matches the specification. This is a common problem in software development, and SDD-Unified is specifically designed to prevent it.

**How SDD-Unified Prevents Drift:**

1.  **Code is a Downstream Product of the Spec:** The core principle of the framework is that code is *generated from* the specification. You should never manually change the code generated by the `sdd-coder` to add new functionality. If a change is needed, you must go back and modify the specification first. The workflow's structure enforces this discipline.
2.  **The "Single Source of Truth":** The collection of `spec.yaml`, `l1_architecture.md`, `l2_component_design.md`, and task files are the single source of truth for how a feature is intended to work. The code is merely the implementation of that truth.
3.  **Iterative Reviews:** The multi-layer review process ensures that the implementation is constantly being checked against the design and the requirements. If a developer were to manually change the code, it would be caught during the next review cycle because it would no longer align with the approved design documents.
4.  **Automated Regeneration:** For a truly disciplined approach, you can adopt a policy where the code for a feature is completely regenerated from the specification whenever the spec changes. This makes it impossible for manual, "off-the-books" code changes to persist.

By adhering to the workflow, you treat your specifications and design documents as living, executable artifacts, not as static documents that are created once and then forgotten. This is the key to eliminating spec-code drift and maintaining a codebase that is predictable, consistent, and easy to understand.

## 6. Advanced Topics

### The "Lite" Workflow

For smaller, less complex features, the full, five-agent workflow can be overkill. In these scenarios, you can use the "lite" workflow. The lite workflow is a streamlined version of the standard workflow that uses fewer agents and has fewer review cycles.

To use the lite workflow, you would typically use a different workflow template that might only involve the `sdd-architect` and `sdd-coder` agents. This is useful for tasks like:

*   Simple bug fixes.
*   Adding a single API endpoint.
*   Making minor modifications to existing functionality.

You can customize the workflow by editing the `workflow.json.template` file or by creating new templates for different scenarios.

### Troubleshooting

*   **Agent Not Found:** If you get an error that an agent cannot be found, make sure that all the agents are properly registered in your AI coding assistant and that their names match the names in the workflow configuration.
*   **Incorrect Output:** If an agent is producing unexpected or incorrect output, you can often guide it by providing more specific instructions in your prompts. You can also modify the agent's persona and instructions in the `.sdd-unified/agents/roles/` directory to fine-tune its behavior.
*   **Workflow Stuck in a Loop:** If a review cycle gets stuck in a loop of rejection and rework, you may need to intervene manually. This usually indicates that the instructions are not clear enough or that there is a fundamental disagreement between the goals of the different agents.

### Customization

SDD-Unified is designed to be customizable. You can adapt the framework to your team's specific needs by:

*   **Modifying Agent Personas:** You can change the behavior of the agents by editing their persona files in `.sdd-unified/agents/roles/`.
*   **Customizing Commands:** The prompts and instructions for each command can be modified in the `.sdd-unified/commands/` directory.
*   **Creating New Workflow Templates:** You can create new workflow templates for different types of tasks (e.g., a "bug-fix" template, a "refactoring" template).

## 6. Reference

### Agent Commands

This section provides a reference for the standard commands used by each agent.

*   **`/feature <description>`:** Initializes a new feature.
*   **`sdd-ba`:**
    *   `Define requirements for...`: Starts the requirements definition process.
*   **`sdd-architect`:**
    *   `Create L1 architecture for...`: Begins the high-level architecture design.
*   **`sdd-pe`:**
    *   `Create L2 component design...`: Starts the detailed component design.
*   **`sdd-le`:**
    *   `Create L3 implementation tasks...`: Begins the implementation planning.
*   **`sdd-coder`:**
    *   `Implement task...`: Starts the code generation for a specific task.

### `spec.yaml` Schema

The `spec.yaml` file is the machine-readable specification that drives the workflow. The basic schema is as follows:

```yaml
feature:
  name: <feature_name>
  description: <feature_description>

requirements:
  - id: REQ-001
    description: <requirement_description>
    type: functional | non-functional

components:
  - name: <component_name>
    description: <component_description>
    endpoints:
      - path: <api_path>
        method: GET | POST | PUT | DELETE
        description: <endpoint_description>
        request:
          ...
        response:
          ...
```

This schema can be extended and customized to fit the needs of your project.

