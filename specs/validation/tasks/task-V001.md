# Validation Task V001: DAG Workflow Execution

## Task Metadata

**Task ID:** V001  
**Priority:** CRITICAL  
**Estimated Effort:** Medium  
**Dependencies:** None  
**Assumption Being Tested:** Claude Code can parse and execute workflow.json as a Directed Acyclic Graph

## Objective

Validate that Claude Code can:
1. Parse a workflow.json file containing task nodes and dependencies
2. Execute tasks in correct order based on dependencies
3. Respect the DAG structure (no circular dependencies)
4. Handle task completion and trigger dependent tasks

## Why This Matters

**If this fails:** The entire sdd_unified workflow model breaks. Without DAG execution, we need either:
- A thin orchestration layer (2-4 weeks development)
- Simplified sequential workflow (acceptable but less powerful)
- Complete redesign of orchestration approach

**Impact Level:** CRITICAL - Framework viability depends on this

## Acceptance Criteria (Gherkin BDD)

```gherkin
Feature: DAG Workflow Execution

Scenario: Simple two-task workflow
  Given a workflow.json with two tasks where task2 depends on task1
  And task1 is a simple command "create file1.txt"
  And task2 is a simple command "read file1.txt and create file2.txt"
  When Claude Code executes the workflow
  Then task1 completes before task2 starts
  And task2 only executes after task1 succeeds
  And both files exist at completion

Scenario: Three-task parallel workflow
  Given a workflow.json with three tasks
  And task2 depends on task1
  And task3 depends on task1
  And task2 and task3 have NO dependency on each other
  When Claude Code executes the workflow
  Then task1 completes first
  And task2 and task3 can execute in parallel OR sequentially
  And all three tasks complete successfully

Scenario: Failed task blocks dependents
  Given a workflow.json with two tasks where task2 depends on task1
  And task1 is designed to fail
  When Claude Code executes the workflow
  Then task1 fails
  And task2 is blocked/skipped
  And task2 never executes

Scenario: Complex dependency chain
  Given a workflow.json with 5 tasks
  And dependencies: A → B, A → C, B → D, C → D, D → E
  When Claude Code executes the workflow
  Then execution order respects all dependencies
  And D only executes after both B and C complete
  And E executes last
```

## Test Procedure

### Setup

1. Create test workflow file:

```json
{
  "workflow_id": "validation-001-dag",
  "nodes": [
    {
      "id": "task-1",
      "command": "create_test_file",
      "args": {"filename": "test1.txt", "content": "Task 1 output"},
      "dependencies": []
    },
    {
      "id": "task-2",
      "command": "read_and_create",
      "args": {"input": "test1.txt", "output": "test2.txt"},
      "dependencies": ["task-1"]
    }
  ]
}
```

2. Create test directory:
```bash
mkdir -p test-validation/validation-001
cd test-validation/validation-001
```

3. Copy workflow.json to test directory

### Execution

**Test 1: Simple Sequential**
```bash
# In Claude Code
/workflow execute workflow.json
```

**Observe:**
- Are both tasks executed?
- In what order?
- Does task-2 wait for task-1?

**Test 2: Parallel Tasks**

Modify workflow.json:
```json
{
  "nodes": [
    {"id": "task-1", "dependencies": []},
    {"id": "task-2", "dependencies": ["task-1"]},
    {"id": "task-3", "dependencies": ["task-1"]}
  ]
}
```

Execute and observe:
- Does task-1 complete first?
- Do task-2 and task-3 execute?
- Are they parallel or sequential?

**Test 3: Failure Handling**

Modify task-1 to fail intentionally.

Execute and observe:
- Does task-1 fail as expected?
- Is task-2 blocked?
- What error message appears?

### Data Collection

For each test, record:
- ✅ / ❌ Success/Failure
- Execution order observed
- Timing (if parallel tasks, do they overlap?)
- Error messages
- Screenshots of execution
- Claude Code version

## Expected Outcomes

### Best Case: Full Support

```
✅ task-1 executes first
✅ task-2 waits for task-1 completion
✅ Parallel tasks execute simultaneously
✅ Failed tasks block dependents
✅ Complex chains work correctly
```

**Conclusion:** Claude Code fully supports DAG workflows. Framework viable as designed.

### Partial Support: Sequential Only

```
✅ task-1 executes first
✅ task-2 executes after task-1
⚠️ Parallel tasks execute sequentially (not simultaneously)
✅ Failed tasks block dependents
✅ Dependencies respected
```

**Conclusion:** DAG parsing works but no parallelization. Framework viable, just slower.

### Minimal Support: Manual Steps

```
⚠️ Tasks execute but user must trigger each
⚠️ Dependencies not automatically enforced
❌ No automatic flow control
```

**Conclusion:** Need orchestration layer or manual execution.

### No Support: Complete Failure

```
❌ workflow.json not recognized
❌ Tasks don't execute in order
❌ Dependencies ignored
```

**Conclusion:** Major redesign required. Consider alternatives.

## Failure Handling

### If Test Fails

**Immediate Actions:**
1. Document exact behavior observed
2. Check Claude Code documentation for workflow features
3. Contact Claude Code support for clarification
4. Investigate alternative approaches

**Alternative Approaches:**

**Option A: Build Orchestration Layer**
- Create `orchestrator.py` that reads workflow.json
- Manually manage task execution and dependencies
- **Effort:** 2-4 weeks
- **Complexity:** Medium

**Option B: Simplify to Sequential**
- Remove DAG complexity
- Use simple step-by-step workflow
- **Effort:** 1 week
- **Complexity:** Low

**Option C: Manual Mode Only**
- User triggers each command manually
- No automatic workflow
- **Effort:** No change
- **Complexity:** Minimal (but user burden)

## Test Results Template

```markdown
# V001 Test Results

**Date:** YYYY-MM-DD
**Tester:** Name
**Claude Code Version:** X.X.X
**Environment:** macOS/Windows/Linux

## Test 1: Simple Sequential
- Status: PASS / FAIL
- Observations:
  - Task execution order: [observed order]
  - Timing: [time between tasks]
- Screenshots: [attach]

## Test 2: Parallel Tasks
- Status: PASS / PARTIAL / FAIL
- Observations:
  - Were tasks parallel? YES / NO
  - Execution pattern: [describe]
- Screenshots: [attach]

## Test 3: Failure Handling
- Status: PASS / FAIL
- Observations:
  - Did dependent task block? YES / NO
  - Error message: [paste]
- Screenshots: [attach]

## Overall Assessment

**Claude Code DAG Support:** FULL / PARTIAL / MINIMAL / NONE

**Recommendation:**
- [ ] Proceed with current design
- [ ] Modify to sequential only
- [ ] Build orchestration layer
- [ ] Complete redesign needed

**Rationale:** [explain]
```

## Success Metrics

| Metric | Target | Acceptable | Unacceptable |
|--------|--------|------------|--------------|
| Dependency Enforcement | 100% | 100% | <100% |
| Parallel Execution | Yes | No (sequential OK) | N/A |
| Failure Handling | Blocks dependents | Logs error | Crashes |
| Execution Time | <1s overhead | <5s overhead | >10s overhead |

## Related Validation Tasks

- V002: Agent Switching (depends on V001 passing)
- V003: Context Management (depends on V001 passing)
- V005: Parallel Execution (extends this test)
- V006: State Persistence (workflow state tracking)

## Notes

- This is the MOST CRITICAL validation task
- All other tests assume this passes
- If this fails, framework must be redesigned
- Allocate sufficient time for thorough testing
- Test with both simple and complex workflows

---

**Task Version:** 1.0.0  
**Created:** 2025-10-16  
**Status:** Pending Execution  
**Criticality:** MAXIMUM