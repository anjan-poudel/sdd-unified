# SDD Unified Framework (sdd-unified)

## Project Overview

**sdd-unified** is a configuration-driven orchestration system designed for Specification-Driven Development (SDD) using agentic AI tools like Claude Code or Roo Code. It acts as a steering configuration layer that enforces a rigorous development methodology on capable but undisciplined AI agents, ensuring deterministic, verifiable, and specification-driven development instead of ad-hoc code generation.

### Key Concepts & Architecture
- **Structured Workflow (DAG-Based):** A Directed Acyclic Graph defines task dependencies, controls automatic agent switching, enables parallel execution, and provides a complete audit trail.
- **Five Specialized Agents:** The framework utilizes a multi-agent system with focused responsibilities:
  - **sdd-ba:** Business requirements and specifications.
  - **sdd-architect:** High-level system architecture (Layer 1).
  - **sdd-pe:** Detailed component design (Layer 2).
  - **sdd-le:** Implementation task planning (Layer 3).
  - **sdd-coder:** Code execution and generation.
- **Task-Driven BDD Implementation:** Development is broken down into discrete tasks with Gherkin acceptance criteria (Given/When/Then) for verifiable and testable outcomes.
- **Iterative Review Cycles:** Formal reviews occur at every design layer, featuring automatic rework, circuit breakers to prevent infinite loops, and human-in-the-loop intervention.
- **Context Management:** Explicit context passing between agents via a `context.json` manifest, tracking decisions, rationale, iteration counts, and review history.

## Development and Usage

### Prerequisites
- Python (for orchestrator and testing scripts).
- AI Agent Tools (e.g., Claude Code or Roo Code) installed.
- Basic understanding of YAML and JSON for configuration.

### Setup & Installation
To use the framework in a project, you copy its configuration into your target repository:
```bash
# Copy framework files into your application repo
mkdir -p .sdd_unified
cp -r /path/to/sdd-unified/agents .sdd_unified/
cp -r /path/to/sdd-unified/commands .sdd_unified/
cp -r /path/to/sdd-unified/templates .sdd_unified/
cp -r /path/to/sdd-unified/orchestrator .sdd_unified/
cp -r /path/to/sdd-unified/spec .sdd_unified/

# Register agents in your agentic tool (e.g., Claude Code)
```

### Typical Workflow Execution
1. **Initialize a feature:**
   ```
   /feature "Create user authentication API"
   ```
2. **Automated multi-agent execution follows:**
   - **sdd-ba:** Generates requirements and `spec.yaml`.
   - **sdd-architect:** Generates `l1_architecture.md`.
   - **Reviews:** Validates L1.
   - **sdd-pe:** Generates `l2_component_design.md`.
   - **Reviews:** Validates L2.
   - **sdd-le:** Generates implementation tasks (`tasks/task-001.md`, etc.).
   - **sdd-coder:** Implements tasks (potentially in parallel).
   - **Reviews:** Validates implementation against BDD criteria.

### Project Structure Highlights
- `agents/`: Agent persona definitions and registration configs.
- `commands/`: Prompts and instructions categorized by agent role.
- `docs/`: Comprehensive documentation (Start at `docs/INDEX.md`).
- `orchestrator/`: Python code managing workflow, task scheduling, routing, and policy gates.
- `spec/`: Feature specification schemas (`spec.yaml`, `spec.schema.json`).
- `templates/`: Templates for workflows, context manifests, and review logs.
- `validation-tests/`: Scripts and plans for validating the framework.

## Development Conventions
- **Declarative Configuration:** Uses YAML/JSON to define workflows and agent behaviors.
- **Forward-Only Transformation:** Changes should be made in specifications or templates, letting agents regenerate the output; avoid manual tweaks to generated code.
- **Contract-First & BDD:** Emphasis on detailed, machine-readable specifications and acceptance criteria before implementation.
- **Continuous Validation:** The framework itself is under active testing (Phase 1: Validation) to confirm integration assumptions with tools like Claude Code. Ensure changes are supported by tests or validation scripts in `validation-tests/` or `orchestrator/`.