# Validation Execution Guide

**Version:** 1.0.0  
**Last Updated:** 2025-10-16

## Prerequisites

Before executing validation tasks, ensure you have:

### 1. Claude Code Installation

```bash
# Verify Claude Code is installed
claude --version

# Expected output: Claude Code v.X.X.X
```

If not installed, visit: [Claude Code Installation Guide]

### 2. SDD Unified Configuration

```bash
# Verify sdd-unified is set up
ls ~/sdd-unified/
# Should show: agents/, commands/, templates/

# OR in project directory
ls sdd-unified/
```

### 3. Agent Registration

```bash
# List registered agents
claude agents list

# You should see:
# - sdd-ba
# - sdd-architect
# - sdd-pe
# - sdd-le
# - sdd-coder
```

If agents aren't registered, follow: [Integration Guide](../../docs/3_integration/claude_code.md)

## Validation Execution Order

Execute in this order (Phase 1 is critical):

**Phase 1: Core Validation (REQUIRED)**
1. ✅ V001: DAG Execution (30-60 min)
2. ✅ V002: Agent Switching (15-30 min)
3. ✅ V003: Context Management (30-45 min)

**Decision Point:** If any Phase 1 test fails, STOP and assess before continuing.

**Phase 2: Advanced Features (OPTIONAL)**
4. V004: Review Outcomes (20-30 min)
5. V006: State Persistence (15-20 min)
6. V007: Conditional Branching (20-30 min)

**Phase 3: Enhancements (FUTURE)**
7. V005: Parallel Execution (30-45 min)
8. V008: BDD Validation (45-60 min)

## Quick Start: Run Phase 1

### Step 1: Setup Test Environment

```bash
# Create test directory
mkdir -p ~/sdd-validation-test
cd ~/sdd-validation-test

# Copy sdd-unified configuration
mkdir -p .sdd_unified
cp -r /path/to/sdd-unified/agents .sdd_unified/
cp -r /path/to/sdd-unified/commands .sdd_unified/
cp -r /path/to/sdd-unified/templates .sdd_unified/
cp -r /path/to/sdd-unified/orchestrator .sdd_unified/
cp -r /path/to/sdd-unified/spec .sdd_unified/

# Create test feature directory
mkdir -p features/validation-001/{spec,design,implementation,review}
cd features/validation-001
```

### Step 2: Execute V001 (DAG Execution)

**Create Test Workflow:**

```bash
cat > workflow.json << 'EOF'
{
  "workflow_id": "validation-001-dag",
  "version": "1.0",
  "nodes": [
    {
      "id": "task-1",
      "description": "Create test file",
      "command": "echo 'Task 1 output' > test1.txt",
      "dependencies": []
    },
    {
      "id": "task-2",
      "description": "Read test file and create another",
      "command": "cat test1.txt && echo 'Task 2 output' > test2.txt",
      "dependencies": ["task-1"]
    }
  ]
}
EOF
```

**Execute Workflow:**

```bash
# Method 1: If Claude Code has workflow command
claude workflow execute workflow.json

# Method 2: Manual execution (fallback)
claude run "Execute task-1 from workflow.json"
# Wait for completion
claude run "Execute task-2 from workflow.json"
```

**Verify Results:**

```bash
# Check files exist
ls -la test*.txt

# Check execution order
echo "test1.txt should exist before test2.txt was created"

# Expected:
# ✅ test1.txt exists
# ✅ test2.txt exists
# ✅ task-2 ran after task-1
```

**Record Results:**

```bash
# Create results file
cat > ../../results/V001-results.md << EOF
# V001 Validation Results

**Date:** $(date)
**Tester:** $(whoami)
**Status:** PASS/FAIL

## Observations:
- DAG execution: [AUTO/MANUAL/FAILED]
- Dependency respected: [YES/NO]
- Notes: [add observations]
EOF
```

### Step 3: Execute V002 (Agent Switching)

**Create Agent Workflow:**

```bash
cat > workflow-agents.json << 'EOF'
{
  "workflow_id": "validation-002-agents",
  "nodes": [
    {
      "id": "requirements",
      "agent": "sdd-ba",
      "command": "Create a simple requirements.md file describing a hello world API",
      "dependencies": [],
      "outputs": ["spec/requirements.md"]
    },
    {
      "id": "design",
      "agent": "sdd-architect",
      "command": "Read spec/requirements.md and create a simple L1 architecture design",
      "dependencies": ["requirements"],
      "inputs": ["spec/requirements.md"],
      "outputs": ["design/l1_architecture.md"]
    }
  ]
}
EOF
```

**Execute:**

```bash
# If automatic agent switching works:
claude workflow execute workflow-agents.json

# If manual switching required:
claude switch-agent sdd-ba
claude run "Create simple requirements.md for hello world API" --output spec/requirements.md

claude switch-agent sdd-architect  
claude run "Create L1 architecture based on spec/requirements.md" --output design/l1_architecture.md
```

**Verify:**

```bash
# Check both files exist
ls spec/requirements.md design/l1_architecture.md

# Check if architect referenced requirements
grep -i "requirement" design/l1_architecture.md

# Expected:
# ✅ Both files exist
# ✅ L1 design mentions requirements
# ✅ Agent switch succeeded
```

### Step 4: Execute V003 (Context Management)

**Create Context File:**

```bash
cat > context.json << 'EOF'
{
  "feature_id": "validation-003",
  "created_at": "2025-10-16T08:00:00Z",
  "handover_notes": {
    "history": []
  },
  "iteration_tracking": {
    "design-l1": {
      "attempts": 0,
      "max_attempts": 3
    }
  }
}
EOF
```

**Test Context Reading:**

```bash
# Run command that should read context
claude switch-agent sdd-architect
claude run "Read context.json and create design referencing any handover notes"

# Check if context was accessed
# Look for evidence in output
```

**Test Context Writing:**

```bash
# Add handover note manually first
cat > context.json << 'EOF'
{
  "feature_id": "validation-003",
  "handover_notes": {
    "history": [
      {
        "from_agent": "sdd-ba",
        "to_agent": "sdd-architect",
        "message": "Critical requirement: System must handle 1000 req/sec"
      }
    ]
  }
}
EOF

# Run architect command
claude switch-agent sdd-architect
claude run "Design architecture considering handover notes in context.json"

# Check if architect's output mentions "1000 req/sec"
grep -i "1000" design/l1_architecture.md
```

## Interpreting Results

### Phase 1 Decision Matrix

| V001 | V002 | V003 | Decision |
|------|------|------|----------|
| PASS | PASS | PASS | ✅ PROCEED to production |
| PASS | PASS | FAIL | ⚠️ Manual context OK, proceed |
| PASS | FAIL | * | ⚠️ Manual agents OK, proceed |
| FAIL | * | * | ❌ REDESIGN required |

### Success Criteria

**Minimum for Production:**
- V001 MUST pass (DAG execution)
- V002 OR manual agent switching works
- V003 OR manual context works

**Ideal:**
- All Phase 1 tests pass automatically
- No manual intervention needed
- Context fully automated

## Recording Results

### Create Results Directory

```bash
mkdir -p ~/sdd-validation-test/results
```

### For Each Test

```bash
# Copy template
cp sdd-unified/specs/validation/tasks/task-VXXX.md results/VXXX-results.md

# Fill in results section
# Document:
# - What happened
# - Screenshots
# - Error messages
# - Recommendations
```

### Summary Report

After all tests:

```bash
cat > results/SUMMARY.md << 'EOF'
# Validation Summary

**Date:** $(date)
**Claude Code Version:** [version]
**Overall Status:** PASS/PARTIAL/FAIL

## Phase 1 Results
- V001 DAG Execution: PASS/FAIL
- V002 Agent Switching: PASS/FAIL  
- V003 Context Management: PASS/FAIL

## Key Findings
[Summarize main discoveries]

## Recommendations
- [ ] Proceed as designed
- [ ] Modify for manual mode
- [ ] Redesign needed

## Next Steps
[Action items]
EOF
```

## Troubleshooting

### Claude Code Not Found

```bash
# Check if installed
which claude

# If not found, install Claude Code first
```

### Agents Not Registered

```bash
# Re-register agents
claude agents register sdd-unified/agents/configs/sdd-ba.yaml
claude agents register sdd-unified/agents/configs/sdd-architect.yaml
# ... repeat for all agents
```

### Workflow Syntax Errors

```bash
# Validate JSON
cat workflow.json | jq .

# If error, fix JSON syntax
```

### Permission Errors

```bash
# Make test directory writable
chmod -R u+w ~/sdd-validation-test
```

## Getting Help

If validation fails or behavior is unclear:

1. **Document exact behavior** - Screenshots, logs, error messages
2. **Check Claude Code docs** - Review official documentation
3. **Contact support** - Provide validation results
4. **Review alternatives** - See failure handling in task documents

## Next Steps After Validation

### If All Tests Pass

1. Update framework assessment (Grade: A-)
2. Create production deployment guide
3. Build example workflows
4. User testing with real features

### If Some Tests Fail

1. Document which assumptions failed
2. Implement documented fallback strategies
3. Update framework architecture
4. Re-validate after changes

### If All Tests Fail

1. Assess if Claude Code supports needed features
2. Consider alternative agentic tools
3. Evaluate building thin orchestration layer
4. Redesign for manual-mode workflow

---

**Document Version:** 1.0.0  
**Last Updated:** 2025-10-16  
**Maintained By:** sdd-unified Validation Team

## Quick Reference Commands

```bash
# Setup
mkdir -p ~/sdd-validation-test/features/validation-001
cd ~/sdd-validation-test/features/validation-001

# V001: Test DAG
claude workflow execute workflow.json

# V002: Test Agents
claude switch-agent sdd-ba
claude run "Create requirements"

# V003: Test Context  
cat context.json  # Verify exists
claude run "Use context.json"

# Record Results
echo "Test results" > ../../results/summary.md
