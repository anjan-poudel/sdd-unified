# SDD Unified Framework Architecture Overview

**Version:** 1.0.0-alpha  
**Status:** Design Complete, Validation Needed  
**Last Updated:** 2025-10-16

## What is sdd-unified?

sdd-unified is a **configuration-driven orchestration system** that makes agentic coding tools (like Claude Code or Roo Code) follow rigorous specification-driven development (SDD) methodology.

### The Core Insight

**sdd-unified is a STEERING SYSTEM, not a runtime.**

It doesn't execute anything—it **directs and structures** how existing agentic tools perform software development.

```
┌─────────────────────────────────────────────────────┐
│  User: "Create auth API"                            │
└─────────────────────┬───────────────────────────────┘
                      ↓
                 /feature command
                      ↓
┌─────────────────────────────────────────────────────┐
│   Claude Code / Roo Code (Execution Engine)         │
│   - Reads workflow.json DAG                         │
│   - Switches between agents                         │
│   - Calls LLMs with prompts                         │
│   - Manages file I/O and state                      │
└─────────────────────┬───────────────────────────────┘
                      ↓ consults
┌─────────────────────────────────────────────────────┐
│   sdd-unified (Configuration/Steering)              │
│   - workflow.json (defines WHAT, WHEN, WHO)         │
│   - agents/configs/*.yaml (agent personas)          │
│   - commands/**/*.yaml (task prompts)               │
│   - context.json (state schema)                     │
└─────────────────────────────────────────────────────┘
```

### Division of Responsibility

| Concern | Owner | Format |
|---------|-------|--------|
| LLM execution | Claude Code/Roo Code | Runtime |
| Workflow parsing | Claude Code/Roo Code | Runtime |
| Agent switching | Claude Code/Roo Code | Runtime |
| File operations | Claude Code/Roo Code | Runtime |
| State persistence | Claude Code/Roo Code | Runtime |
| **Workflow structure** | **sdd-unified** | **workflow.json** |
| **Agent roles** | **sdd-unified** | **agents/*.yaml** |
| **Task prompts** | **sdd-unified** | **commands/*.yaml** |
| **Quality gates** | **sdd-unified** | **Review architecture** |
| **Context schema** | **sdd-unified** | **context.json** |

## Core Architecture Components

### 1. Workflow DAG (Directed Acyclic Graph)

Defined in `templates/workflow.json.template`, the DAG specifies:
- Tasks and their dependencies
- Agent assignments
- Conditional flows (review outcomes)
- Parallel execution opportunities

**Key Innovation:** Declarative workflow as configuration, not imperative scripts.

### 2. Five Specialized Agents

Each agent has a focused responsibility with optimized prompts:

| Agent | Role | Key Outputs |
|-------|------|-------------|
| **sdd-ba** | Business Analyst | requirements.md, spec.yaml |
| **sdd-architect** | System Architect | l1_architecture.md |
| **sdd-pe** | Principal Engineer | l2_component_design.md |
| **sdd-le** | Lead Engineer | implementation/tasks/*.md |
| **sdd-coder** | Implementation | Source code |

### Optional Operating Overlay: Pair + Formal Review

The default role architecture stays unchanged. An optional overlay adds:

- `driver_agent` and `challenger_agent` collaboration on critical tasks
- single `artifact_dri` accountability for each output
- independent formal review gates as GO/NO-GO evidence checks

This gives higher early defect detection without changing the core DAG shape.

See: [Pair + Formal Review Overlay](pair_review_overlay.md)

### 3. Three-Layer Design

**L1 (Architecture):** High-level system design  
**L2 (Components):** Detailed component specifications  
**L3 (Tasks):** Discrete implementation tasks with BDD criteria

### 4. Task-Driven Implementation

L3 produces **discrete task files** (not monolithic plans):
- Each task has a unique ID
- Gherkin BDD acceptance criteria
- Technical details without over-prescription
- Verifiable completion

**Example task file:**
```yaml
task_id: "task-003"
description: "Implement JWT token generation"
acceptance_criteria: |
  Given a valid user credential
  When generateToken() is called
  Then a valid JWT is returned
  And the token contains user ID and role
  And the token expires in 24 hours
```

### 5. Iterative Review Architecture

Every design layer has formal reviews with outcomes:
- Review outcome files (JSON format)
- APPROVED / REJECTED_WITH_FEEDBACK status
- Automatic triggering of `*-rework` commands
- Circuit breakers to prevent infinite loops

**Review Cycle:**
```
Design L1 → BA Review → [APPROVED] → Continue
                      ↘ [REJECTED] → L1 Rework → BA Review
                                                  ↓
                                           (max 3 iterations)
                                                  ↓
                                           Human Intervention
```

### 6. Context Management

The `context.json` manifest solves agent-to-agent information loss:
- Current phase tracking
- Handover notes between agents
- Iteration counters (for circuit breakers)
- Review history

## Design Principles

### 1. Configuration Over Code
All orchestration is declarative YAML/JSON, not imperative Python/Shell scripts.

### 2. Verifiability Through BDD
Every implementation task has Gherkin acceptance criteria that can be tested.

### 3. Separation of Concerns
Each agent has ONE clear responsibility, avoiding "do everything" anti-pattern.

### 4. Fail-Safe Iteration
Circuit breakers prevent infinite review loops, with human intervention protocol.

### 5. Framework Agnostic
While designed for Claude Code, the configuration could work with any agentic tool supporting:
- YAML agent configs
- JSON workflow DAGs
- Prompt templates
- State persistence

## Key Files and Directories

```
sdd-unified/
├── agents/
│   ├── roles/          # Agent persona definitions
│   └── configs/        # Claude Code agent registration
├── commands/
│   ├── ba/             # Business analyst commands
│   ├── architect/      # Architect commands
│   ├── pe/             # Principal engineer commands
│   ├── le/             # Lead engineer commands
│   ├── coder/          # Coder commands
│   └── feature/        # Feature initialization
├── templates/
│   └── workflow.json.template  # DAG workflow definition
├── spec/
│   └── spec.yaml       # Feature specification schema
└── docs/               # Comprehensive documentation
```

## Workflow Example

**User Request:** "Create user authentication API"

**Automated Flow:**
1. **Feature Init** → Creates feature directory structure
2. **sdd-ba** → Writes requirements.md and spec.yaml
3. **sdd-architect** → Creates L1 architecture design
4. **Multiple Reviewers** → BA, PE, LE review L1
5. **If Rejected** → L1 Rework (max 3 iterations)
6. **sdd-pe** → Creates L2 component design
7. **Reviewers** → Architect, LE review L2
8. **sdd-le** → Generates discrete implementation tasks
9. **PE Review** → Validates task breakdown
10. **sdd-coder** → Implements each task sequentially
11. **LE Review** → Validates each implementation
12. **If Rejected** → Task rework (max 2 iterations)
13. **Done** → Audit trail in workflow.json

## Comparison to Alternatives

### vs. Ad-Hoc Prompting
**Ad-Hoc:** "Claude, create auth API" → Code appears (no structure, no verification)  
**sdd-unified:** Structured spec → design → review → implement → verify

**Winner:** sdd-unified (far more rigorous)

### vs. Manual SDD
**Manual:** Developer writes spec → Email reviews → Implement → PR  
**sdd-unified:** Automated spec generation → Structured reviews → Task-driven implementation

**Winner:** sdd-unified (faster and more consistent)

### vs. Other SDD Frameworks
- **spec-kit:** Template library (no orchestration)
- **BMAD:** Process documentation (no automation)
- **a-sdd-starter:** Shell scripts (imperative, not declarative)

**sdd-unified:** Configuration-driven orchestration (declarative and portable)

## Current Status

### ✅ Complete
- Workflow DAG architecture
- Agent role definitions
- Task-driven implementation design
- Iterative review architecture
- Context management system
- Comprehensive documentation

### ⚠️ Needs Validation
- Claude Code can execute workflow.json as DAG
- Agent switching with context passing
- Conditional logic for review outcomes
- State persistence mechanisms

### ❌ Not Started
- End-to-end testing with real projects
- BDD validation mechanism
- Error recovery procedures
- "Lite" workflow templates for simple features

## Next Steps

1. **Prototype with Claude Code** (Week 1)
   - Validate core assumptions
   - Test basic agent switching
   - Verify workflow execution

2. **Remove Unnecessary Complexity** (Week 1)
   - Delete orchestrator.py
   - Simplify installation
   - Pure configuration only

3. **Create Lite Workflow** (Week 2)
   - For simple features (CRUD, bug fixes)
   - 2 agents instead of 5
   - 1 design level instead of 3

4. **End-to-End Testing** (Weeks 2-4)
   - Simple API endpoint
   - Authentication feature
   - Bug fix workflow

## Further Reading

- [Workflow Engine Design](workflow_engine.md) - Deep dive into DAG execution
- [Task-Driven Implementation](task_driven_implementation.md) - BDD task system
- [Iterative Reviews](iterative_reviews.md) - Review/rework cycles
- [Context Management](context_management.md) - Agent handover system
- [Framework Assessment](../6_analysis/framework_assessment.md) - Honest evaluation

## Conclusion

sdd-unified is a **well-designed orchestration configuration** that brings structure and discipline to AI-driven development. Its value lies not in code execution, but in **process definition**—turning free-form AI assistance into rigorous, verifiable engineering.

**The critical question:** Can Claude Code actually execute this design?  
**The answer:** Validation needed (see Assessment document).
