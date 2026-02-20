# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**sdd-unified** is a configuration-driven orchestration framework for Specification-Driven Development (SDD) using agentic AI tools. It's a "steering configuration layer" that makes tools like Claude Code follow rigorous specification-driven development methodology through a DAG-based workflow engine.

**Status:** Design complete (v1.0.0-alpha), validation in progress.

**Core Concept:** Instead of ad-hoc code generation, this framework enforces deterministic, verifiable, specification-driven development through structured workflows, specialized agents, and formal review cycles.

## Architecture: DAG-Based Workflow Engine

The framework is built on a **Directed Acyclic Graph (DAG)** workflow model:

- **Single Source of Truth:** `workflow.json` in each feature directory defines all tasks, dependencies, and status
- **Task Status:** `PENDING` → `READY` → `RUNNING` → `COMPLETED` / `FAILED`
- **Dependency Resolution:** Tasks only execute when all dependencies are `COMPLETED`
- **Parallel Execution:** Independent tasks (e.g., multiple reviews) can run simultaneously
- **Agent Switching:** Each task runs a specific agent with its own persona and commands

### Five Specialized Agents

1. **sdd-ba** (Business Analyst): Requirements and specifications
2. **sdd-architect**: High-level system architecture (L1)
3. **sdd-pe** (Principal Engineer): Detailed component design (L2)
4. **sdd-le** (Lead Engineer): Implementation task planning (L3)
5. **sdd-coder**: Code execution with BDD acceptance criteria

### Three Design Layers

- **L1 Architecture** (`design/l1_architecture.md`): High-level technical blueprint, API design, data models
- **L2 Component Design** (`design/l2_component_design.md`): Detailed component specifications
- **L3 Implementation Tasks** (`implementation/tasks/task-NNN.md`): Discrete tasks with Gherkin acceptance criteria

## Key Directories

### `/agents/`
- **`roles/*.yaml`**: Agent persona definitions (expertise, responsibilities)
- **`configs/*.yaml`**: Agent registration for Claude Code integration

### `/commands/`
- **`ba/`, `architect/`, `pe/`, `le/`, `coder/`**: Agent-specific command prompts
- **`feature/`, `slash/`**: Feature initialization and status commands
- Each command YAML defines task dependencies, inputs/outputs, and execution prompts

### `/templates/`
- **`workflow.json.template`**: Master DAG workflow definition for features
- **`review.log.template`**: Review feedback structure

### `/orchestrator/`
- **`main.py`**: Workflow orchestrator (may be needed if Claude Code can't execute DAG natively)
- **`status.py`**: Status management utilities

### `/validation-tests/`
- **Phase 1**: Agent loading tests
- **Phase 2**: Workflow execution tests
- **Phase 3**: End-to-end feature tests
- See `VALIDATION_MASTER_PLAN.md` for validation strategy

### `/docs/`
Comprehensive documentation (60+ pages) organized by:
- Getting started guides
- Architecture deep-dives
- Integration guides
- Practical usage guides
- Technical reference
- Framework analysis

## Development Commands

### Running Validations

```bash
# Phase 1: Test agent loading (30-60 min)
cd validation-tests/phase1-agent-loading
# Follow README.md for step-by-step instructions

# Phase 2: Test workflow execution (2-3 hours)
cd validation-tests/phase2-workflow-execution
# Follow README.md

# Phase 3: End-to-end feature test (4-8 hours)
cd validation-tests/phase3-end-to-end
# Follow README.md
```

### Setup Scripts

```bash
# Install framework for Claude Code
./scripts/install_claude.sh

# Install framework for Roo Code
./scripts/install_roo.sh
```

### Validation Setup

```bash
# Automated validation environment setup
./validation-tests/setup-validation.sh
```

## Critical Workflow Concepts

### Task Dependencies in workflow.json

Example from `templates/workflow.json.template`:

```json
{
  "design-l1": {
    "command": "sdd-architect-design-l1 --task_id=design-l1",
    "status": "PENDING",
    "dependencies": ["define-requirements"]
  },
  "review-l1-ba": {
    "status": "PENDING",
    "dependencies": ["design-l1"]
  },
  "review-l1-pe": {
    "status": "PENDING",
    "dependencies": ["design-l1"]
  },
  "design-l2": {
    "status": "PENDING",
    "dependencies": ["review-l1-ba", "review-l1-pe", "review-l1-le"]
  }
}
```

**Key Pattern:** Multiple review tasks depend on the same parent (e.g., `design-l1`), enabling parallel execution. Next phase waits for ALL reviews to complete.

### Command Structure

Each command YAML follows this pattern:

1. **Dependency Check:** Verify prerequisite tasks are `COMPLETED` in `workflow.json`
2. **Status Update:** Set task status to `RUNNING`
3. **Execute Task:** Read input artifacts, perform analysis/design/implementation
4. **Create Outputs:** Write required artifacts to specified paths
5. **Update Status:** Set task status to `COMPLETED`

### First Principles Thinking

Agent commands emphasize **first principles thinking**:
- "5 Whys" methodology for requirement decomposition
- Explicit justification for architectural decisions
- Single responsibility principle for components
- Root cause analysis before solutions

### BDD Task-Driven Implementation

Implementation tasks use **Gherkin acceptance criteria**:

```markdown
## Acceptance Criteria (Gherkin)
Given [precondition]
When [action]
Then [expected outcome]
And [additional verification]
```

Each task is discrete, verifiable, and testable.

### Iterative Review Cycles

- Formal review at every design layer (L1, L2, L3, Code)
- Automatic rework when reviews reject (with circuit breakers)
- Review results stored in `review/*.log` files
- Maximum iterations defined to prevent infinite loops

## Working with This Framework

### When Modifying Agent Personas

Agent roles are defined in `agents/roles/*.yaml`. When editing:
- Keep `expertise` lists focused and specific
- Ensure `description` clearly defines scope and boundaries
- Don't add generic capabilities; specialization is intentional

### When Modifying Commands

Command prompts in `commands/**/*.yaml` define agent behavior. Key principles:
- **Always specify `file_path`** for output artifacts (used by orchestrator)
- **Document dependencies** explicitly in the prompt
- **Include workflow.json integration steps** (dependency check, status updates)
- **Provide step-by-step instructions** for task execution
- **Define success criteria** clearly

### When Modifying workflow.json

The DAG structure in `templates/workflow.json.template`:
- Add tasks with unique `task_id`
- Specify `dependencies` array (can be empty for root tasks)
- Define `command` to execute
- Initialize `status` as `PENDING`
- Consider parallelism opportunities (tasks with same dependency)

### Context Management

The `context.json` file (referenced in architecture) carries state between agents:
- Decision tracking with rationale
- Iteration counting
- Review history
- Agent handover notes

## Key Files to Reference

- **`README.md`**: Project overview, quick start, status
- **`ARCHITECTURE.md`**: Five-layer architecture, agent communication, repeatability mechanisms
- **`PLAYBOOK.md`**: DAG workflow details, command reference, agent roles
- **`paired-sessions-and-formal-reviews_prompt.md`**: Alternative proposal using pair programming approach
- **`docs/INDEX.md`**: Complete documentation navigation
- **`validation-tests/VALIDATION_MASTER_PLAN.md`**: Validation strategy and testing approach

## Current Validation Status

The framework is **unvalidated** with Claude Code. Critical questions being tested:

1. Can Claude Code execute `workflow.json` as a DAG natively?
2. Does agent switching work with context preservation?
3. Can conditional branching work based on review outcomes?
4. Does parallel task execution work?
5. How does state persistence work across sessions?

**Grade:** B+ (8.5/10) - Excellent design, needs validation to prove assumptions.

## When Working on Validation

If working on validation tests (`validation-tests/`):
- Follow the three-phase strategy: Agent Loading → Workflow Execution → End-to-End
- Document actual behavior vs. expected behavior in phase READMEs
- Update `VALIDATION_MASTER_PLAN.md` with findings
- If assumptions fail, document workarounds or architecture changes needed

## Technology Stack

- **Primary Language:** Python (for orchestrator utilities)
- **Configuration:** YAML (agents, commands), JSON (workflow state)
- **Dependencies:** Listed in `requirements.txt` (minimal: pyyaml)
- **Target Runtime:** Claude Code or Roo Code
- **Documentation:** Markdown

## Integration Points

The framework integrates into target projects by copying to `.sdd_unified/`:

```bash
mkdir -p /target/project/.sdd_unified
cp -r agents commands templates orchestrator spec /target/project/.sdd_unified/
```

Then register agents with Claude Code and use `/feature "description"` command to start workflows.
