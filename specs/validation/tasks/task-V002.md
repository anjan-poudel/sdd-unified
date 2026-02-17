# Validation Task V002: Agent Switching with Context

## Task Metadata

**Task ID:** V002  
**Priority:** CRITICAL  
**Estimated Effort:** Small  
**Dependencies:** V001 (DAG Execution must pass)  
**Assumption Being Tested:** Claude Code can switch between agents while preserving context

## Objective

Validate that Claude Code can:
1. Switch from one agent to another during workflow execution
2. Preserve context across agent switches
3. Make previous agent's outputs available to next agent
4. Maintain workflow state through agent transitions

## Why This Matters

**If this fails:** The multi-agent model collapses. Without agent switching, we need either:
- Single agent with role-based prompts (1-2 weeks adaptation)
- Manual agent changes by user (acceptable but cumbersome)
- Separate single-agent workflows per phase

**Impact Level:** CRITICAL - Core to multi-agent architecture

## Acceptance Criteria (Gherkin BDD)

```gherkin
Feature: Agent Switching

Scenario: Two-agent sequential workflow
  Given a workflow with task-1 assigned to sdd-ba
  And task-2 assigned to sdd-architect
  And task-2 depends on task-1
  When the workflow executes
  Then sdd-ba agent executes task-1
  And sdd-architect agent executes task-2
  And sdd-architect can read task-1's output

Scenario: Agent accesses previous agent's context
  Given sdd-ba has created spec/requirements.md
  And workflow switches to sdd-architect
  When sdd-architect executes design-l1 task
  Then sdd-architect's prompt includes reference to spec/requirements.md
  And sdd-architect can read the requirements file
  And sdd-architect's output references requirements

Scenario: Multiple agent switches
  Given a workflow: BA → Architect → PE → LE
  When all tasks execute in sequence
  Then each agent switch succeeds
  And each agent can access all previous outputs
  And no context is lost between switches

Scenario: Agent-specific persona maintained
  Given sdd-ba agent with business analyst persona
  And sdd-architect agent with technical architect persona
  When both agents execute their tasks
  Then sdd-ba's output is business-focused
  And sdd-architect's output is technical-focused
  And each maintains their distinct perspective
```

## Test Procedure

### Setup

1. Create minimal workflow with two agents:

```json
{
  "workflow_id": "validation-002-agents",
  "nodes": [
    {
      "id": "requirements",
      "agent": "sdd-ba",
      "command": "ba/define-requirements",
      "dependencies": [],
      "outputs": ["spec/requirements.md"]
    },
    {
      "id": "design-l1",
      "agent": "sdd-architect",
      "command": "architect/design-l1",
      "dependencies": ["requirements"],
      "inputs": ["spec/requirements.md"],
      "outputs": ["design/l1_architecture.md"]
    }
  ]
}
```

2. Ensure both agents registered in Claude Code:
```bash
# Verify agents exist
claude-code agents list | grep sdd-
```

3. Create test feature directory:
```bash
mkdir -p test-validation/validation-002/{spec,design}
```

### Execution

**Test 1: Basic Agent Switch**

```bash
# Execute workflow
cd test-validation/validation-002
claude-code workflow execute

# OR if no workflow command:
# Manually switch agents and run commands
```

**Observe:**
- Does agent switch from BA to Architect?
- Is switch automatic or manual?
- Does Architect agent have access to requirements.md?

**Test 2: Context Preservation**

After workflow execution:

1. Check if requirements.md exists and has content
2. Check if l1_architecture.md references requirements
3. Verify Architect agent "knew about" requirements

**Test 3: Persona Verification**

Compare outputs:
- Does requirements.md have business language?
- Does l1_architecture.md have technical details?
- Are the perspectives distinct?

### Data Collection

Record for each test:
- Agent switch mechanism (auto/manual/command)
- Context available to each agent
- Output quality (does it reference inputs?)
- Agent persona adherence
- Screenshots of agent switching

## Expected Outcomes

### Best Case: Automatic Switching with Full Context

```
✅ Agents switch automatically based on workflow
✅ Each agent has full context from previous agents
✅ Outputs reference inputs correctly
✅ Agent personas maintained
✅ No manual intervention required
```

**Conclusion:** Multi-agent model works as designed. Framework viable.

### Good Case: Automatic Switching, Manual Context

```
✅ Agents switch automatically
⚠️ Agents must be explicitly told to read previous outputs
✅ Outputs correct when prompted properly
✅ Agent personas maintained
```

**Conclusion:** Need to update command prompts to explicitly load context.  
**Effort:** 1 day to update command YAML files.

### Acceptable: Manual Switching, Context Works

```
⚠️ User must manually switch agents
✅ Each agent can access previous outputs
✅ Outputs reference inputs when prompted
✅ Agent personas maintained
```

**Conclusion:** Workflow requires manual mode.  
**Effort:** Update documentation, acceptable workflow.

### Problematic: No Agent Switching

```
❌ Cannot switch between agents
⚠️ Must use single agent for entire workflow
❌ Agent personas lost
```

**Conclusion:** Single-agent architecture required.  
**Effort:** 1-2 weeks to redesign as role-based prompts.

## Failure Handling

### If Test Fails

**Immediate Actions:**
1. Verify agent configurations are loaded
2. Check Claude Code agent switching documentation
3. Test manual agent switching as fallback
4. Document exact switching behavior

**Alternative Approaches:**

**Option A: Manual Agent Switching**
- User manually switches agents at each phase
- Document switching points in workflow
- **Effort:** No development, documentation only
- **User Experience:** More manual but acceptable

**Option B: Single Agent with Roles**
- One "sdd-multi" agent with role-based prompts
- Each command specifies role (ba, architect, etc.)
- **Effort:** 1-2 weeks to merge agents
- **Loss:** Less specialized personas

**Option C: Command-Based Switching**
- Each command explicitly specifies agent switch
- More verbose but guaranteed to work
- **Effort:** Update command definitions (1 week)
- **Overhead:** More configuration

## Test Results Template

```markdown
# V002 Test Results

**Date:** YYYY-MM-DD
**Tester:** Name
**Claude Code Version:** X.X.X

## Test 1: Basic Agent Switch
- Status: PASS / FAIL
- Agent switch mechanism: AUTO / MANUAL / COMMAND
- Observations:
  - How was switch triggered? [describe]
  - Was it seamless? YES / NO
- Screenshots: [attach]

## Test 2: Context Preservation
- Status: PASS / PARTIAL / FAIL
- Observations:
  - Did Architect see requirements? YES / NO
  - References in output: [list]
  - Context loading: AUTOMATIC / EXPLICIT
- Example Output: [paste]

## Test 3: Persona Verification
- Status: PASS / FAIL
- BA Output Character: BUSINESS / TECHNICAL / MIXED
- Architect Output Character: TECHNICAL / BUSINESS / MIXED
- Personas Distinct: YES / NO

## Overall Assessment

**Agent Switching:** AUTOMATIC / MANUAL / COMMAND / UNSUPPORTED
**Context Access:** AUTOMATIC / EXPLICIT / MANUAL / NONE

**Recommendation:**
- [ ] Proceed as designed (automatic switching)
- [ ] Update prompts for explicit context loading
- [ ] Document manual switching process
- [ ] Redesign as single agent

**Rationale:** [explain]
```

## Success Metrics

| Metric | Target | Acceptable | Unacceptable |
|--------|--------|------------|--------------|
| Agent Switching | Automatic | Manual trigger | Unsupported |
| Context Access | Auto-loaded | Explicit read | Not available |
| Persona Adherence | 100% distinct | 80% distinct | <50% |
| Switch Latency | <2s | <10s | >30s |

## Integration with V001

**Dependency:** This test requires V001 to pass first.

**If V001 fails:**
- Test manually triggered agent switching
- Each agent command run independently
- Still validates context preservation

**Combined Testing:**
- Can run V001 and V002 in same test
- Single workflow, multiple agents
- Efficient validation

## Related Validation Tasks

- V001: DAG Execution (prerequisite)
- V003: Context Management (related)
- V004: Review Outcomes (uses agent switching)

## Notes

- Second most critical test (after V001)
- Multi-agent model depends on this
- Fallback options available if fails
- Test both automatic and manual modes

---

**Task Version:** 1.0.0  
**Created:** 2025-10-16  
**Status:** Pending Execution  
**Criticality:** CRITICAL (after V001)