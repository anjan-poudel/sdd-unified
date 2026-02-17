# Phase 1 Validation: Agent Loading Test

**Goal:** Confirm Claude Code can load external agent configurations and execute commands.

**Estimated Time:** 30-60 minutes

## Prerequisites

- Claude Code installed and running
- Terminal access

## Test Steps

### Step 1: Prepare Test Agent

Copy a single agent configuration to test Claude Code's ability to load external agents:

```bash
# Create Claude Code agents directory if it doesn't exist
mkdir -p ~/.claude-code/agents

# Copy the BA agent as our test subject
cp ../../agents/configs/sdd-ba.yaml ~/.claude-code/agents/

# Verify the file copied correctly
cat ~/.claude-code/agents/sdd-ba.yaml
```

**Expected:** YAML file displays without errors

### Step 2: Restart Claude Code

**Action:** Completely quit and restart Claude Code to force it to reload agent configurations.

### Step 3: Verify Agent Loading

In Claude Code, try to check if the agent is available:

**Method 1 - Direct invocation:**
```
Switch to sdd-ba agent and introduce yourself
```

**Method 2 - Check agent list (if Claude Code provides a command):**
```
/agents list
```

**Success Criteria:**
- ✅ Agent loads without errors
- ✅ Agent responds with BA persona (requirements focused, asks clarifying questions)
- ✅ No YAML parsing errors

**Failure Indicators:**
- ❌ "Agent not found" error
- ❌ YAML syntax errors
- ❌ Agent loads but doesn't follow persona

### Step 4: Test Command Execution

Copy a simple command for the BA agent:

```bash
# Create commands directory
mkdir -p ~/.claude-code/commands

# Copy the define-requirements command
cp ../../commands/ba/define-requirements.yaml ~/.claude-code/commands/

# Restart Claude Code again
```

In Claude Code, try to execute the command:
```
/define-requirements
```

**Success Criteria:**
- ✅ Command is recognized
- ✅ Prompt executes as defined in YAML
- ✅ Agent follows the command template

### Step 5: Test File Creation

Create a minimal test workspace:

```bash
mkdir -p phase1-test-feature/spec
cd phase1-test-feature
```

In Claude Code, while in the test directory:
```
Create a spec.yaml file based on this requirement: "User can log in with email and password"
```

**Success Criteria:**
- ✅ File `spec/spec.yaml` is created
- ✅ Contains structured requirement data
- ✅ Follows YAML format

## Results Recording

### Test 1: Agent Loading
- [ ] PASS - Agent loaded successfully
- [ ] FAIL - Agent failed to load
- **Notes:**

### Test 2: Agent Persona
- [ ] PASS - Agent follows BA persona
- [ ] FAIL - Agent doesn't follow persona
- **Notes:**

### Test 3: Command Execution
- [ ] PASS - Command executed from YAML
- [ ] FAIL - Command not recognized
- **Notes:**

### Test 4: File Creation
- [ ] PASS - Created spec.yaml correctly
- [ ] FAIL - File creation failed
- **Notes:**

## Critical Findings

**If ALL tests pass:**
✅ Claude Code supports external agent configs - Proceed to Phase 2

**If ANY test fails:**
⚠️ Document the failure mode and investigate:
- Check Claude Code documentation for agent configuration
- Verify YAML syntax
- Check Claude Code version/capabilities
- May need orchestrator.py fallback approach

## Next Steps

- If Phase 1 passes → Proceed to Phase 2: Workflow Execution Testing
- If Phase 1 fails → Document blockers and design alternative approach

## Cleanup

```bash
# If test successful and moving to Phase 2, leave files in place
# If starting over:
rm -rf phase1-test-feature
```
