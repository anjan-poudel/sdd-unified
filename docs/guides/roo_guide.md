# Getting Started with the SDD Unified Framework using Roo Code

This guide provides a comprehensive walkthrough of installing and using the `sdd_unified` framework with the `roo-code` development environment.

## 1. Introduction

The `sdd_unified` framework provides a robust, state-driven, and iterative process for developing software with AI agents. When paired with `roo-code`, it allows you to orchestrate a team of specialized AI agents, manage complex workflows, and ensure the quality of the final product through a structured review and rework cycle.

This guide will show you how to get started.

## 2. Installation

Follow these steps to set up your environment.

1.  **Clone the Repository:**
    ```bash
    git clone <repository_url>
    cd sdd_unified
    ```

2.  **Run the Installation Script:**
    This script will set up a Python virtual environment, install dependencies, and create a set of convenient aliases for using `roo-code` with the framework.
    ```bash
    bash scripts/install_roo.sh
    ```

3.  **Activate the Aliases:**
    The installer will create a file at `~/.sdd_aliases_roo`. To activate the commands, you need to source this file.
    ```bash
    source ~/.sdd_aliases_roo
    ```
    For permanent access, add this line to your shell's startup file (e.g., `~/.zshrc`, `~/.bashrc`, or `~/.profile`).

## 3. Core Concepts

Before diving in, it's important to understand the core concepts:

-   **The DAG-Based Workflow (`workflow.json`):** Everything is driven by a Directed Acyclic Graph (DAG) defined in `workflow.json`. This file orchestrates the entire development process, defining tasks and their dependencies.
-   **The Machine-Readable Specification (`spec.yaml`):** The single source of truth for what the software should do. All design and implementation work is derived from and validated against this file.
-   **Iterative Review Process:** No code or design is "done" on the first try. Every artifact goes through a formal review cycle. Feedback is logged, and a rework is triggered until the review is formally approved.
-   **Task-Driven Implementation:** The implementation phase is broken down into small, verifiable tasks, each with its own BDD-style acceptance criteria.

## 4. Step-by-Step Feature Implementation Example

Let's walk through a complete end-to-end workflow for creating a simple user authentication feature.

**Feature:** A secure API endpoint that authenticates a user based on a username and password.

### Step 1: Initialize the Feature

First, we'll use the `init` command to create a new, self-contained directory for our feature.

```bash
# The alias calls roo-code with the correct prompt file
sdd-feature-init --feature-name "user-auth-api"

# Navigate into the new feature directory
cd features/user-auth-api
```

This creates a standard directory structure (`spec/`, `design/`, `implementation/`, `review/`) and a `workflow.json` file to track our progress.

### Step 2: Define Requirements (Business Analyst)

Next, the Business Analyst agent will translate a high-level requirement into a formal `spec.yaml`.

```bash
# Provide the high-level prompt for the BA
sdd-ba-define-requirements --prompt "Create a secure API endpoint at POST /login that accepts a username and password. It should return a JWT token on success and a 401 error on failure."
```

The framework, via the alias, will invoke `roo-code` with the correct prompt and save the output to `spec/spec.yaml`. The result will look something like this:

```yaml
# spec/spec.yaml
version: 1.0
requirements:
  - id: FR-001
    type: functional
    description: "The system must provide an API endpoint at POST /login for user authentication."
  - id: FR-002
    type: functional
    description: "The POST /login endpoint must accept a JSON body with 'username' and 'password' fields."
  - id: NFR-001
    type: non-functional
    description: "Successful authentication shall return a JWT token with a 2-hour expiration."
```

### Step 3: Design L1 Architecture (Architect)

The Architect agent now takes the `spec.yaml` and creates a high-level technical design.

```bash
sdd-architect-design-l1
```

This will generate `design/l1_architecture.md`, outlining the main components (e.g., "Authentication Controller," "JWT Service," "User Repository").

### Step 4: Review L1 Design & Iterate

Now, the review cycle begins. Let's say the Principal Engineer finds an issue.

```bash
# The PE runs their review command
sdd-pe-review-design-l1
```

The alias invokes `roo-code`, which analyzes the design. Let's imagine it finds a flaw. It will generate `review/review_l1_pe.json` with the following content:

```json
{"status":"REJECTED_WITH_FEEDBACK","findings":[{"nfr":"security","issue":"The L1 design does not mention password hashing. Storing or comparing plain-text passwords is a critical security vulnerability.","recommendation":"The architecture must specify a strong hashing algorithm (e.g., bcrypt) for password management."}]}
```

### Step 5: Rework the L1 Design

The workflow is now blocked until the design is fixed. The Architect agent is invoked to perform the rework.

```bash
sdd-architect-design-l1-rework
```

This command feeds the original design and all the review feedback back into `roo-code`. The agent produces a new, improved `l1_architecture.md` that now includes details about `bcrypt` hashing. The review commands are then run again until all reviewers output an `APPROVED` status.

### Step 6: L2 & L3 Design Cycles

This same pattern of **Design -> Review -> Rework -> Approve** continues for the L2 (component design) and L3 (task generation) phases.

### Step 7: Task-Driven Implementation (Coder)

Once the L3 design is approved, the `implementation/tasks/` directory will be populated with markdown files.

```
implementation/tasks/
├── task-001-create-user-model.md
├── task-002-add-bcrypt-hashing.md
└── task-003-create-login-endpoint.md
```

The Coder agent can now implement these tasks, potentially in parallel if they are independent.

```bash
# Implement the first task
sdd-coder-execute-task --task-id 001
```

### Step 8: Review and Rework a Task

Just like the design phases, each implemented task is reviewed.

```bash
# The Lead Engineer reviews the code for task 001
sdd-le-review-task --task-id 001
```

If the review is rejected, the Coder agent is invoked to fix the specific issue.

```bash
# The Coder reworks the faulty implementation
sdd-coder-rework-task --task-id 001
```

This ensures that every single piece of code is reviewed and meets quality standards before being considered "done."

### Step 9: Feature Completion

When all tasks have been successfully implemented and approved, the feature is complete and ready for integration.

## 5. Conclusion

By using the `sdd_unified` framework with `roo-code`, you transform AI-driven development from a simple "prompt-to-code" activity into a mature, structured, and auditable engineering process. This ensures higher quality, greater predictability, and better alignment with requirements.