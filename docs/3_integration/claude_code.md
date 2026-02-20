# Claude Code Integration Guide

**Version:** 1.0.0  
**Status:** Design Complete, Needs Validation  
**Last Updated:** 2025-10-16

## Overview

This guide explains how to integrate sdd-unified with Claude Code, a powerful agentic coding tool that can execute workflows, switch between agents, and orchestrate multi-step development processes.

## Prerequisites

- Claude Code installed and working
- Access to Claude Code's agent configuration system
- Basic understanding of YAML and JSON
- A code project directory

## Architecture

### Division of Responsibility

**Claude Code (Execution Engine):**
- Parses workflow.json DAG
- Switches between agents
- Calls LLMs with prompts
- Manages file I/O
- Persists state

**sdd-unified (Configuration Layer):**
- Defines workflow structure
- Provides agent personas
- Specifies command templates
- Sets quality gates

```
User → /feature command → Claude Code → Reads sdd-unified configs → Executes workflow
```

## Installation Steps

### Step 1: Copy Configuration Files

```bash
# Navigate to your project
cd /path/to/your/project

# Create sdd-unified directory
mkdir -p .sdd_unified/{agents,commands,templates,orchestrator,spec}

# Copy all configuration files
cp -r /path/to/sdd-unified/agents/configs .sdd_unified/agents/
cp -r /path/to/sdd-unified/commands .sdd_unified/
cp -r /path/to/sdd-unified/templates .sdd_unified/
cp -r /path/to/sdd-unified/orchestrator .sdd_unified/
cp -r /path/to/sdd-unified/spec .sdd_unified/
```

### Step 2: Register Agents in Claude Code

**Option A: UI Registration**

1. Open Claude Code Settings
2. Navigate to: Extensions → Agents → Custom Agents
3. For each agent config file in `.sdd_unified/agents/configs/`:
   - Click "Add Custom Agent"
   - Select the YAML file
   - Verify agent appears in list

**Option B: Configuration File**

Add to Claude Code's `settings.json`:

```json
{
  "agents": {
    "customAgents": [
      ".sdd_unified/agents/configs/sdd-ba.yaml",
      ".sdd_unified/agents/configs/sdd-architect.yaml",
      ".sdd_unified/agents/configs/sdd-pe.yaml",
      ".sdd_unified/agents/configs/sdd-le.yaml",
      ".sdd_unified/agents/configs/sdd-coder.yaml"
    ]
  }
}
```

### Step 3: Verify Agent Registration

Open Claude Code command palette and check for:
- ✓ sdd-ba (Business Analyst)
- ✓ sdd-architect (System Architect)
- ✓ sdd-pe (Principal Engineer)
- ✓ sdd-le (Lead Engineer)
- ✓ sdd-coder (Implementation)

### Step 4: Configure Slash Commands (Optional)

If Claude Code supports custom slash commands:

```json
{
  "commands": {
    "custom": [
      {
        "trigger": "/feature",
        "description": "Start new feature with sdd-unified workflow",
        "command": "load_workflow",
        "args": {
          "template": ".sdd_unified/templates/workflow.json.template"
        }
      },
      {
        "trigger": "/sdd-status",
        "description": "Check current workflow status",
        "command": "show_workflow_status"
      }
    ]
  }
}
```

## Usage

## Recommended Adoption Path

For current repo state, start with:

1. Manual or supervised workflow execution
2. Pair execution inside critical tasks (driver + challenger)
3. Independent formal reviews as GO/NO-GO gates

Then move to deeper automation after integration assumptions are validated.

See:
- [Day 1 Checklist](../1_getting_started/day1_checklist.md)
- [Pair + Formal Review Overlay](../2_architecture/pair_review_overlay.md)

### Starting a New Feature

**Method 1: Slash Command (if available)**

```
/feature "Create user authentication API"
```

**Method 2: Manual Initialization**

1. Create feature directory:
```bash
mkdir -p features/feature-001-auth/{spec,design,implementation,review}
```

2. Copy workflow template:
```bash
cp .sdd_unified/templates/workflow.json.template features/feature-001-auth/workflow.json
```

3. Initialize context:
```bash
# Create empty context.json
echo '{"feature_id": "feature-001-auth", "feature_name": "User Authentication"}' > features/feature-001-auth/context.json
```

4. Switch to sdd-ba agent and run:
```
Define requirements for user authentication API
```

### Switching Between Agents

Claude Code should handle agent switching automatically based on workflow.json, but you can also switch manually:

1. Open agent selector
2. Choose the appropriate sdd-* agent
3. Continue the workflow

### Running the Full Workflow

**Autonomous Mode** (if supported):

```
/feature "User authentication" --mode=autonomous
```

Claude Code executes the entire workflow automatically, switching agents as defined in workflow.json.

**Manual Mode:**

You execute each step manually, switching agents between phases:

1. **sdd-ba:** Define requirements
2. **sdd-architect:** Design L1 architecture
3. **sdd-ba, sdd-pe, sdd-le:** Review L1
4. **sdd-pe:** Design L2 components
5. **sdd-le:** Generate L3 tasks
6. **sdd-coder:** Execute tasks
7. **sdd-le:** Review implementations

## Critical Assumptions (Need Validation)

⚠️ **These features are ASSUMED but not yet validated:**

### 1. Workflow DAG Execution

**Assumption:** Claude Code can parse and execute workflow.json as a DAG.

**Validation Needed:**
```json
{
  "nodes": [
    {"id": "task1", "dependencies": []},
    {"id": "task2", "dependencies": ["task1"]}
  ]
}
```

Can Claude Code:
- Parse this structure?
- Execute task1 before task2?
- Handle circular dependency detection?

### 2. Agent Switching with Context

**Assumption:** When switching agents, Claude Code preserves context.

**Validation Needed:**
- Does context.json automatically load for new agent?
- Or must each command explicitly read context.json?
- Is there a context size limit?

### 3. Conditional Branching

**Assumption:** Claude Code can branch based on file contents.

**Validation Needed:**
```json
{
  "condition": "review_l1_ba.status == APPROVED",
  "on_true": "design-l2",
  "on_false": "design-l1-rework"
}
```

Can Claude Code evaluate this?

### 4. Parallel Execution

**Assumption:** Tasks without dependencies can run in parallel.

**Validation Needed:**
```json
{
  "nodes": [
    {"id": "task1", "dependencies": ["design-l3"]},
    {"id": "task2", "dependencies": ["design-l3"]}
  ]
}
```

Can Claude Code run task1 and task2 concurrently?

### 5. State Persistence

**Assumption:** Workflow state persists across sessions.

**Validation Needed:**
- If workflow paused, can it resume?
- Where is state stored?
- How long is state retained?

## Troubleshooting

### Agents Not Appearing

**Symptom:** Custom agents don't show in Claude Code

**Possible Causes:**
- YAML syntax errors in agent configs
- Incorrect file paths in settings
- Claude Code needs restart

**Solutions:**
1. Validate YAML syntax: `yamllint .sdd_unified/agents/configs/*.yaml`
2. Check file paths are absolute or properly relative
3. Restart Claude Code
4. Check Claude Code logs for errors

### Workflow Not Executing

**Symptom:** workflow.json doesn't trigger automatic execution

**Possible Causes:**
- Claude Code doesn't support DAG execution
- workflow.json has syntax errors
- Missing required fields

**Solutions:**
1. Validate JSON: `jsonlint workflow.json`
2. Check Claude Code documentation for workflow support
3. Fall back to manual mode if automatic execution unsupported

### Context Not Passing

**Symptom:** Each agent starts fresh, ignoring previous work

**Possible Causes:**
- context.json not being loaded
- context.json in wrong location
- Agent prompts don't read context

**Solutions:**
1. Verify context.json exists in feature directory
2. Add explicit context reading to command prompts:
```yaml
prompt: |
  First, read and understand context.json.
  Pay special attention to handover notes addressed to you.
```

### Review Outcomes Not Triggering Rework

**Symptom:** Rejected reviews don't automatically start rework

**Possible Causes:**
- Claude Code doesn't support conditional workflow
- Review outcome format incorrect
- Condition syntax not recognized

**Solutions:**
1. Check review JSON files have correct status field
2. Manually trigger rework commands when reviews reject
3. Build simple orchestration layer if needed

## Validation Checklist

Before using sdd-unified with Claude Code in production:

- [ ] Install and register all 5 agents
- [ ] Verify agents appear in Claude Code
- [ ] Create test feature directory
- [ ] Run simple 2-step workflow (BA → Architect)
- [ ] Verify context.json is created and updated
- [ ] Test agent switching with context preservation
- [ ] Validate review outcome format
- [ ] Attempt conditional branching
- [ ] Test parallel task execution (if supported)
- [ ] Measure performance and resource usage

## Performance Considerations

### Resource Usage

Each agent switch involves:
- Loading new agent configuration
- Reading context files
- Potentially calling LLM API
- Writing output files

**Estimated costs:**
- Per agent switch: 1-2 seconds
- Per LLM call: $0.01-0.10 (depends on model)
- Full workflow (simple feature): $1-5
- Full workflow (complex feature): $10-50

### Optimization

To reduce costs and latency:

1. **Use lite workflow** for simple features
2. **Batch agent operations** where possible
3. **Cache common responses** (if Claude Code supports)
4. **Use smaller models** for simple tasks
5. **Limit review iterations** with circuit breakers

## Examples

### Example 1: Simple API Endpoint

```bash
# Initialize
/feature "GET /health endpoint"

# sdd-ba agent runs automatically
# Outputs: spec/requirements.md

# sdd-architect agent runs
# Outputs: design/l1_architecture.md

# Reviews run automatically
# If approved, continues to L2...
```

### Example 2: Complex Feature

```bash
# Use full workflow
/feature "User authentication system" --workflow=full

# Autonomous execution through all phases:
# BA → L1 → Reviews → L2 → Reviews → L3 → Reviews → Implementation → Reviews
```

### Example 3: Manual Step-by-Step

```bash
# Create feature manually
mkdir -p features/feature-002-auth

# Switch to sdd-ba
# Run: "Define requirements for auth API"

# Switch to sdd-architect  
# Run: "Create L1 design based on requirements"

# Continue manually through workflow...
```

## Next Steps

After installation:

1. **Run Validation Tests** - Verify all assumptions
2. **Start with Simple Feature** - Test basic workflow
3. **Document Actual Behavior** - What actually works vs assumptions
4. **Report Issues** - Feed findings back to framework maintainers
5. **Iterate** - Refine configuration based on real usage

## Known Limitations

1. **Unvalidated Integration** - Core assumptions not yet tested
2. **Manual Fallback** - May need manual agent switching
3. **No Error Recovery** - Failure handling undefined
4. **Performance Unknown** - Resource usage not measured
5. **Version Compatibility** - Tied to specific Claude Code version

## Support

If you encounter issues:

1. Check this guide's troubleshooting section
2. Review Claude Code documentation
3. Check framework repository for updates
4. Create issue with detailed error logs

## Summary

sdd-unified + Claude Code provides:
- ✅ Structured SDD workflow
- ✅ Multi-agent specialization
- ✅ Quality gates and reviews
- ⚠️ Needs validation for production use
- ⚠️ May require manual mode if assumptions fail

**Critical Next Step:** Validate assumptions with real Claude Code installation.
