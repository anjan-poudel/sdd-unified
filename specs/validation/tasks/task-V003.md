# Validation Task V003: Context.json Management

## Task Metadata

**Task ID:** V003  
**Priority:** CRITICAL  
**Estimated Effort:** Medium  
**Dependencies:** V001 (DAG), V002 (Agent Switching)  
**Assumption Being Tested:** context.json persists state and is accessible to all agents

## Objective

Validate that:
1. context.json is created and maintained throughout workflow
2. All agents can read and write to context.json
3. Handover notes transfer information between agents
4. Iteration tracking works correctly
5. Circuit breaker logic functions as designed

## Why This Matters

**If this fails:** Agents lose critical information between phases. Each agent starts from scratch without understanding previous decisions, iterations, or rationale.

**Without context:**
- No handover notes → agents don't know what predecessors learned
- No iteration tracking → circuit breakers don't work
- No decision history → lost rationale for choices

**Impact Level:** CRITICAL - Prevents information loss in multi-agent system

## Acceptance Criteria (Gherkin BDD)

```gherkin
Feature: Context Management

Scenario: Context file creation and persistence
  Given a new feature workflow is initialized
  When the feature/init command executes
  Then a context.json file is created
  And context.json contains feature_id
  And context.json contains created_at timestamp
  And context.json contains empty handover_notes array

Scenario: Agent reads context
  Given context.json exists with previous agent's work
  And current agent is sdd-architect
  When sdd-architect begins design-l1 task
  Then sdd-architect's prompt includes context.json reference
  And sdd-architect can access handover notes from sdd-ba
  And sdd-architect can read iteration_tracking data

Scenario: Agent updates context
  Given sdd-ba completes requirements task
  When sdd-ba finishes execution
  Then context.json is updated
  And handover_notes array contains new entry
  And handover note includes "from_agent": "sdd-ba"
  And handover note includes "to_agent": "sdd-architect"
  And handover note includes critical information

Scenario: Iteration tracking increments
  Given design-l1 is being reworked for the 2nd time
  When sdd-architect completes design-l1-rework
  Then context.json iteration_tracking.design-l1.attempts increments
  And current value is 2
  And review history is appended

Scenario: Circuit breaker triggers
  Given design-l1 has been reworked 3 times (max attempts)
  When iteration_tracking.design-l1.attempts reaches 3
  Then context.json circuit_breaker.intervention_required becomes true
  And blocked_task is set to "design-l1"
  And workflow pauses for human intervention

Scenario: Context persistence across commands
  Given context.json updated by sdd-ba
  And workflow continues to sdd-architect
  And then to sdd-pe
  When sdd-pe reads context.json
  Then all handover notes from sdd-ba and sdd-architect are present
  And iteration counts are preserved
  And no information is lost
```

## Test Procedure

### Setup

1. Create test feature directory:
```bash
mkdir -p test-validation/validation-003/{spec,design,review}
cd test-validation/validation-003
```

2. Initialize context template:
```bash
cp ../../.sdd_unified/templates/context.json.template ./context.json
```

3. Modify template with test feature_id:
```json
{
  "feature_id": "validation-003-context",
  "created_at": "2025-10-16T08:00:00Z"
}
```

### Execution

**Test 1: Context Creation**

Execute feature init command:
```bash
# Via workflow or direct command
claude-code run feature/init
```

Verify:
- Does context.json exist?
- Does it have required fields?
- Is it valid JSON?

**Test 2: Agent Reads Context**

Set up context with handover note:
```json
{
  "handover_notes": {
    "history": [
      {
        "from_agent": "sdd-ba",
        "to_agent": "sdd-architect",
        "note": "TEST: Critical requirement R-001 mandates scalability"
      }
    ]
  }
}
```

Execute architect command:
```bash
claude-code switch-agent sdd-architect
claude-code run design-l1
```

Check:
- Does architect's output mention R-001?
- Does output reference "scalability"?
- Evidence agent read context?

**Test 3: Agent Writes Context**

Start with minimal context, run BA command:
```bash
claude-code run ba/define-requirements
```

After completion, check context.json:
- Is there a new handover note?
- Does it have from/to agents?
- Is message meaningful?

**Test 4: Iteration Tracking**

Simulate rework cycle:

1. Set initial iteration count:
```json
{
  "iteration_tracking": {
    "design-l1": {
      "attempts": 1,
      "max_attempts": 3
    }
  }
}
```

2. Run rework command:
```bash
claude-code run architect/design-l1-rework
```

3. Check if attempts incremented to 2

**Test 5: Circuit Breaker**

Set iteration to max:
```json
{
  "iteration_tracking": {
    "design-l1": {
      "attempts": 3,
      "max_attempts": 3
    }
  },
  "circuit_breaker": {
    "max_review_iterations": 3,
    "intervention_required": false
  }
}
```

Attempt another rework:
```bash
claude-code run architect/design-l1-rework
```

Verify:
- Does command block/warn?
- Is intervention_required set to true?
- Is workflow halted?

### Data Collection

For each test:
- Initial context.json state
- Final context.json state
- Diff between states
- Agent outputs (check for context references)
- Error messages (if any)
- Screenshots

## Expected Outcomes

### Best Case: Full Context Management

```
✅ context.json created automatically
✅ All agents can read context
✅ Handover notes populated correctly
✅ Iteration tracking increments
✅ Circuit breaker triggers at limits
✅ Context persists across entire workflow
```

**Conclusion:** Context management works as designed.

### Good Case: Manual Context Updates

```
✅ context.json exists
⚠️ Agents must be explicitly instructed to read context
✅ Context can be manually updated
✅ Iteration tracking works when manually incremented
⚠️ Circuit breaker requires manual checking
```

**Conclusion:** Context works but needs explicit management in prompts.  
**Effort:** Update command YAML files to include context operations.

### Acceptable: Context as Reference Only

```
✅ context.json can be created
⚠️ Agents don't automatically use it
⚠️ Manual tracking required
❌ No automatic circuit breaker
```

**Conclusion:** Context is documentation, not automation.  
**Effort:** Manual workflow management acceptable.

### Problematic: No Context Support

```
❌ context.json not accessible to agents
❌ No state persistence
❌ Information lost between phases
```

**Conclusion:** Need alternative state management.  
**Effort:** External database or explicit file-based state (2-3 weeks).

## Failure Handling

### If Test Fails

**Immediate Actions:**
1. Verify context.json is valid JSON
2. Check file permissions
3. Test manual context reading/writing
4. Document exact failure mode

**Alternative Approaches:**

**Option A: Explicit Context in Prompts**
- Each command manually loads and saves context
- Verbose but guaranteed to work
- **Effort:** 1 week to update all commands
- **Reliability:** High

**Option B: Simplified Context**
- Minimal context (just current phase)
- Skip handover notes and iteration tracking
- **Effort:** Minimal
- **Loss:** Circuit breakers, rich context

**Option C: External State Store**
- Use database or key-value store
- More complex but robust
- **Effort:** 2-3 weeks
- **Scalability:** Better for production

## Test Results Template

```markdown
# V003 Test Results

**Date:** YYYY-MM-DD
**Tester:** Name
**Claude Code Version:** X.X.X

## Test 1: Context Creation
- Status: PASS / FAIL
- context.json exists: YES / NO
- Valid JSON: YES / NO
- Required fields present: YES / NO
- Initial state: [paste JSON]

## Test 2: Agent Reads Context
- Status: PASS / PARTIAL / FAIL
- Agent accessed context: YES / NO / UNCLEAR
- Evidence in output: [quote relevant parts]
- Reading mechanism: AUTOMATIC / EXPLICIT / MANUAL

## Test 3: Agent Writes Context
- Status: PASS / PARTIAL / FAIL
- Context updated: YES / NO
- Handover note added: YES / NO
- Note quality: GOOD / ACCEPTABLE / POOR
- Before/After diff: [show changes]

## Test 4: Iteration Tracking
- Status: PASS / FAIL
- Attempts incremented: YES / NO
- Starting value: X
- Ending value: Y
- Expected value: Z

## Test 5: Circuit Breaker
- Status: PASS / FAIL
- Triggered at limit: YES / NO
- intervention_required set: YES / NO
- Workflow blocked: YES / NO
- Error message: [paste]

## Overall Assessment

**Context Accessibility:** FULL / PARTIAL / MANUAL / NONE
**State Persistence:** AUTOMATIC / MANUAL / NONE

**Recommendation:**
- [ ] Context works as designed
- [ ] Update commands for explicit context handling
- [ ] Simplify context model
- [ ] Use alternative state management

**Rationale:** [explain]
```

## Success Metrics

| Metric | Target | Acceptable | Unacceptable |
|--------|--------|------------|--------------|
| Context Creation | Automatic | Manual init | Not possible |
| Agent Read Access | Automatic | Explicit | Not available |
| Agent Write Updates | Automatic | Explicit | Not possible |
| Iteration Tracking | Automatic | Manual | Not available |
| Circuit Breaker | Automatic | Manual check | Not possible |

## Integration with V001 & V002

**Dependencies:**
- V001 must pass (workflow execution)
- V002 must pass (agent switching)

**Combined Testing:**
- Run all three in one workflow
- Full requirements → design → review cycle
- Validates complete flow

**Efficiency:**
- Single test feature
- Multiple validations
- Realistic scenario

## Related Validation Tasks

- V001: DAG Execution (prerequisite)
- V002: Agent Switching (prerequisite)
- V004: Review Outcomes (uses context)
- V006: State Persistence (related)

## Notes

- Third critical validation (completes Phase 1)
- Context is key differentiator for sdd_unified
- Without context, framework loses major value
- Alternative state management possible if fails
- Focus on practical usability

---

**Task Version:** 1.0.0  
**Created:** 2025-10-16  
**Status:** Pending Execution  
**Criticality:** CRITICAL (completes Phase 1)