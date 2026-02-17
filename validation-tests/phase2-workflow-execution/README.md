# Phase 2 Validation: Workflow DAG Execution

**Goal:** Validate Claude Code can parse and execute workflow.json as a Directed Acyclic Graph.

**Prerequisites:** Phase 1 completed successfully

**Estimated Time:** 2-3 hours

## Test Overview

We'll create a minimal 3-task workflow to test:
1. Claude Code can parse workflow.json structure
2. Tasks execute in dependency order
3. Task status updates persist
4. Agent switching works between tasks

## Test Setup

### Step 1: Create Test Feature Structure

```bash
cd sdd_unified/validation-tests
mkdir -p phase2-test-workflow/{spec,design,review}
cd phase2-test-workflow
```

### Step 2: Create Minimal Workflow

Create `workflow.json` with only 3 tasks:

```json
{
  "init": {
    "command": "echo 'Initializing feature workspace'",
    "status": "COMPLETED",
    "dependencies": []
  },
  "define-requirements": {
    "command": "sdd-ba-define-requirements --task_id=define-requirements",
    "status": "PENDING",
    "dependencies": ["init"]
  },
  "design-l1": {
    "command": "sdd-architect-design-l1 --task_id=design-l1",
    "status": "PENDING",
    "dependencies": ["define-requirements"]
  }
}
```

**Save as:** `workflow.json`

### Step 3: Test Manual Workflow Execution

**Goal:** Manually trigger tasks to see if Claude Code recognizes the workflow structure.

In Claude Code:
```
Read the workflow.json file and execute the first READY task
```

**Expected behavior:**
- Claude Code identifies that "define-requirements" is READY (init is COMPLETED)
- Switches to sdd-ba agent
- Executes the define-requirements command
- Creates `spec/requirements.md` or `spec/spec.yaml`

### Step 4: Check Status Update

After task completes, check if status was updated:

```bash
cat workflow.json
```

**Success Criteria:**
- ✅ "define-requirements" status changed from "PENDING" to "COMPLETED"
- ✅ File created in spec/ directory

**If status NOT updated:**
⚠️ Claude Code may not automatically update workflow.json
- This is a critical finding - document it
- May need orchestrator.py to manage status

### Step 5: Test Sequential Execution

In Claude Code:
```
Continue with the next READY task in the workflow
```

**Expected:**
- Claude Code identifies "design-l1" is now READY
- Switches to sdd-architect agent
- Executes design-l1 command
- Creates `design/l1_architecture.md`

### Step 6: Test Full Workflow Understanding

In Claude Code:
```
Read workflow.json and tell me:
1. Which tasks are completed?
2. Which tasks are ready to execute?
3. Which tasks are still pending?
4. What's the dependency chain?
```

**Success Criteria:**
- ✅ Claude Code correctly parses the DAG structure
- ✅ Understands dependency relationships
- ✅ Can identify READY vs PENDING tasks

## Critical Tests

### Test A: Dependency Resolution

**Question:** Does Claude Code execute tasks in the correct order?

**Method:**
1. Set all tasks to PENDING
2. Only "init" should be READY
3. Ask Claude Code to execute next task
4. Should refuse or execute init only

**Result:**
- [ ] PASS - Respects dependencies
- [ ] FAIL - Executes tasks out of order

### Test B: Status Persistence

**Question:** Do status updates persist across commands?

**Method:**
1. Complete define-requirements
2. Ask Claude Code about workflow status in a NEW message
3. Does it remember the task is complete?

**Result:**
- [ ] PASS - Status persists
- [ ] FAIL - Status resets or not read

### Test C: Agent Switching

**Question:** Can Claude Code switch agents mid-workflow?

**Method:**
1. Execute define-requirements (BA agent)
2. Then execute design-l1 (Architect agent)
3. Check persona in each response

**Result:**
- [ ] PASS - Agent switching works
- [ ] FAIL - Stuck in one agent persona

### Test D: Workflow.json as Single Source of Truth

**Question:** Does Claude Code treat workflow.json as authoritative?

**Method:**
1. Manually edit workflow.json to mark a task COMPLETED
2. Ask Claude Code what's the next task
3. Does it recognize the manual change?

**Result:**
- [ ] PASS - Reads current workflow.json state
- [ ] FAIL - Has stale/cached view

## Results Summary

### Overall Assessment

**If ALL tests pass:**
✅ **Claude Code can execute workflow DAG natively!**
- Pure configuration model validated
- No orchestrator.py needed
- Framework can be simplified significantly

**If SOME tests pass:**
⚠️ **Partial support - need workarounds**
- Document which capabilities are missing
- Determine if orchestrator.py can fill gaps
- May need hybrid approach

**If NO tests pass:**
❌ **Native DAG execution not supported**
- orchestrator.py is required
- Framework needs execution layer
- Timeline extends to 2-3 months

### Critical Findings

**Document answers to:**
1. Does Claude Code parse workflow.json automatically? YES / NO
2. Does Claude Code update task status? YES / NO
3. Can Claude Code switch agents per task? YES / NO
4. Does workflow state persist across messages? YES / NO

## Next Steps

**If Phase 2 succeeds:**
→ Proceed to Phase 3: End-to-End Feature Test

**If Phase 2 fails:**
→ Design orchestrator integration strategy
→ Document required workarounds
→ Re-evaluate architecture

## Test Artifacts

All files created during this phase:
```
phase2-test-workflow/
├── workflow.json           # Workflow definition
├── spec/
│   ├── requirements.md     # Created by BA agent
│   └── spec.yaml          # Created by BA agent
└── design/
    └── l1_architecture.md  # Created by Architect agent
```

Keep these for Phase 3 testing.
