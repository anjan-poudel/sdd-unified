# Quick Start Guide

Get up and running with sdd-unified in 5 minutes.

## Recommended Operating Mode

For first adoption, use:

- Manual or supervised execution mode
- Pair execution inside each critical task (driver + challenger)
- Independent formal review gates before advancing

See:
- [Day 1 Checklist](day1_checklist.md)
- [Pair + Formal Review Overlay](../2_architecture/pair_review_overlay.md)

## Prerequisites

- Claude Code or Roo Code installed
- Basic understanding of YAML and JSON
- A code project directory

## Installation

### Step 1: Copy Configuration Files

```bash
# Navigate to your project
cd /path/to/your/project

# Create sdd-unified directory structure
mkdir -p .sdd_unified/{agents,commands,templates,orchestrator,spec}

# Copy sdd-unified configuration files
cp -r /path/to/sdd-unified/agents .sdd_unified/
cp -r /path/to/sdd-unified/commands .sdd_unified/
cp -r /path/to/sdd-unified/templates .sdd_unified/
cp -r /path/to/sdd-unified/orchestrator .sdd_unified/
cp -r /path/to/sdd-unified/spec .sdd_unified/
```

### Step 2: Configure Your Agentic Tool

**For Claude Code:**

1. Open Claude Code settings
2. Navigate to Agent Configuration
3. Import agents from `.sdd_unified/agents/configs/`
4. Verify all 5 agents are registered (sdd-ba, sdd-architect, sdd-pe, sdd-le, sdd-coder)

**For Roo Code:**

1. Open Roo Code preferences
2. Add custom agents directory: `.sdd_unified/agents/configs/`
3. Reload agent configurations
4. Verify agents appear in agent selector

### Step 3: Initialize a Feature

```bash
# Using slash command (if integrated)
/feature "Create user authentication"

# Or manually create feature directory
mkdir -p features/feature-001-auth/{spec,design,implementation/tasks,review}
```

## Your First Feature

Let's create a simple REST API endpoint to understand the workflow.

### 1. Define Requirements (sdd-ba)

Switch to the sdd-ba agent and run:
```
Define requirements for a GET /health endpoint that returns service status
```

**Expected Output:** `spec/requirements.md` and `spec/spec.yaml`

### 2. Design Architecture (sdd-architect)

Switch to sdd-architect agent:
```
Create L1 architecture for the health check endpoint
```

**Expected Output:** `design/l1_architecture.md`

### 3. Review Design (sdd-ba, sdd-pe, sdd-le)

Each reviewer validates the design:
```
Review the L1 architecture design
```

**Expected Output:** `review/review_l1_ba.json` with status APPROVED or REJECTED_WITH_FEEDBACK

### 4. Component Design (sdd-pe)

If L1 approved, proceed to L2:
```
Create L2 component design based on approved L1
```

**Expected Output:** `design/l2_component_design.md`

### 5. Implementation Planning (sdd-le)

Generate discrete implementation tasks:
```
Create L3 implementation tasks with BDD acceptance criteria
```

**Expected Output:** `implementation/tasks/task-001.md`, `task-002.md`, etc.

### 6. Implement Code (sdd-coder)

Execute each task:
```
Implement task-001: Create health endpoint route
```

**Expected Output:** Source code files

### 7. Review Implementation (sdd-le)

Validate task completion:
```
Review task-001 implementation against BDD criteria
```

**Expected Output:** `review/review_task_001.json`

## Lite Workflow (For Simple Features)

For simple tasks like bug fixes or small endpoints, use the lite workflow:

```yaml
# Use simplified workflow template
workflow: lite
agents: [sdd-architect, sdd-coder]
design_levels: [L1]
reviews: optional
```

This skips BA requirements and PE/LE roles for faster iteration.

## Verification

Check that your setup is working:

1. ✅ Agents are registered in your agentic tool
2. ✅ Can create feature directory structure
3. ✅ Can switch between agents
4. ✅ Each agent produces expected outputs
5. ✅ Review files trigger correctly

## Troubleshooting

### Agents Not Appearing

**Problem:** Agents don't show up in Claude Code/Roo Code  
**Solution:** Verify agent YAML files are in the correct directory and properly formatted

### Workflow Not Executing

**Problem:** Commands don't trigger the expected workflow  
**Solution:** Check that `workflow.json` is in the feature directory and follows the DAG structure

### Context Not Passing Between Agents

**Problem:** Each agent starts from scratch  
**Solution:** Ensure `context.json` is being created and updated in the feature directory

### Review Outcomes Not Triggering Rework

**Problem:** Rejected reviews don't automatically trigger rework commands  
**Solution:** This requires Claude Code/Roo Code native support for conditional workflow execution

## Next Steps

- Read the [Feature Development Workflow](../4_guides/feature_development.md) guide
- Understand [Agent Roles](../4_guides/agent_roles.md)
- Learn about [BDD Task Verification](../2_architecture/task_driven_implementation.md)
- Review the [Architecture Overview](../2_architecture/overview.md)

## Getting Help

- **Documentation:** Browse the `/docs` directory
- **Examples:** See `/use_cases/examples/` for complete workflows
- **Issues:** Common problems and solutions in troubleshooting guide

## Summary

You now have:
- ✅ sdd-unified configuration installed
- ✅ Agents registered in your tool
- ✅ Understanding of the basic workflow
- ✅ Ability to create your first feature

**Time to completion:** ~5 minutes  
**Next:** Try creating a real feature using the full workflow
