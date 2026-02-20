# Quick Start Guide: Getting Started with SDD Unified

> Legacy note: This guide is kept for backward compatibility.
> Use these canonical docs for current setup and workflow:
> - `../1_getting_started/quick_start.md`
> - `../1_getting_started/day1_checklist.md`
> - `../2_architecture/pair_review_overlay.md`

Welcome to SDD Unified! This guide will walk you through the initial setup and a basic workflow to get you started.

## What is SDD Unified?

SDD Unified is a framework that brings structure and predictability to AI-powered software development. It uses a series of specialized AI agents, each with a specific role, to take a feature from an idea to fully implemented code, following a rigorous, specification-driven process.

## Prerequisites

Before you begin, ensure you have the following:

*   An AI-powered coding assistant that supports custom agents (e.g., Claude Code, Roo Code).
*   Basic knowledge of YAML and JSON.
*   A project where you want to apply SDD Unified.

## 1. Installation and Setup

First, you need to integrate SDD Unified into your project.

### Copy Configuration

Copy the core configuration of SDD Unified into your project's root directory:

```bash
cp -r /path/to/sdd-unified/agents /path/to/your/project/.sdd_unified/
cp -r /path/to/sdd-unified/commands /path/to/your/project/.sdd_unified/
cp -r /path/to/sdd-unified/templates /path/to/your/project/.sdd_unified/
cp -r /path/to/sdd-unified/orchestrator /path/to/your/project/.sdd_unified/
cp -r /path/to/sdd-unified/spec /path/to/your/project/.sdd_unified/
```

This command copies the agent personas, command prompts, workflow templates, and orchestrator files into a `.sdd_unified` directory in your project.

### Configure Your AI Assistant

Next, register the SDD Unified agents with your AI assistant. The general steps are:

1.  Open your AI assistant's settings or preferences.
2.  Find the section for managing custom agents.
3.  Import the agent configurations from the `.sdd_unified/agents/configs/` directory.
4.  Confirm that the following five agents are now available:
    *   `sdd-ba` (Business Analyst)
    *   `sdd-architect`
    *   `sdd-pe` (Principal Engineer)
    *   `sdd-le` (Lead Engineer)
    *   `sdd-coder`

## 2. Your First Feature: A "Health Check" API

Let's walk through creating a simple API endpoint. This will introduce you to the core workflow and the roles of the different agents.

### Step 1: Initialize the Feature

You can start a new feature in two ways:

*   **Using a slash command (if your tool supports it):**
    ```
    /feature "Create a health check endpoint"
    ```
*   **Manually:**
    ```bash
    mkdir -p features/health-check-endpoint/{spec,design,implementation,review}
    ```

This creates a dedicated directory for your new feature, with subdirectories for each stage of the development process.

### Step 2: Define the Requirements (with `sdd-ba`)

Select the `sdd-ba` agent in your AI assistant. This agent is responsible for turning your request into a clear specification.

**Your prompt:**
> "Define the requirements for a GET endpoint at `/health` that returns a JSON object with a 'status' field set to 'ok'."

The `sdd-ba` will generate two files in the `features/health-check-endpoint/spec/` directory:

*   `requirements.md`: A human-readable description of the feature.
*   `spec.yaml`: A machine-readable specification.

### Step 3: Design the Architecture (with `sdd-architect`)

Now, switch to the `sdd-architect` agent. This agent designs the high-level technical solution.

**Your prompt:**
> "Based on the requirements, create a high-level architecture for the health check endpoint."

The `sdd-architect` will create a `design/l1_architecture.md` file, outlining the overall structure and components.

### Step 4: Plan the Implementation (with `sdd-le`)

Next, the `sdd-le` (Lead Engineer) agent breaks down the design into small, actionable tasks.

**Your prompt:**
> "From the architecture document, create a detailed implementation plan."

This will result in one or more task files in `implementation/tasks/`, such as `task-001.md`. Each task file will include a clear description and BDD-style acceptance criteria (Given/When/Then).

### Step 5: Write the Code (with `sdd-coder`)

Finally, it's time to write the code. Select the `sdd-coder` agent for this.

**Your prompt:**
> "Implement the tasks in the implementation plan."

The `sdd-coder` will read the task files and generate the necessary source code to fulfill the requirements.

## 3. The Review Process

In a real project, each step would be followed by a review from other agents (e.g., the `sdd-pe` and `sdd-le` review the architect's work). This ensures quality and alignment at every stage. For this quick start, we've skipped the explicit review steps, but you can learn more about them in our comprehensive [User Manual](../user_manual/user_manual.md).

## What's Next?

Congratulations! You've successfully run your first feature through the SDD Unified workflow.

From here, you can:

*   Dive deeper into the full capabilities of the framework in our **[User Manual](../user_manual/user_manual.md)**.
*   Explore the different agents and their roles in more detail.
*   Learn about the iterative review cycles and how they improve code quality.
*   Try a more complex feature and observe the full, multi-agent workflow in action.
