# Phase 3 Validation: End-to-End Feature Development

**Goal:** Test complete workflow with all agents, review cycles, and parallel execution.

**Prerequisites:** Phase 1 and Phase 2 completed successfully

**Estimated Time:** 4-8 hours (includes execution + observation)

## Test Overview

Use the FSM Parallel Workflow Engine use case as a real-world test:
- Complete feature specification
- All 5 agents involved
- Multiple review cycles
- Parallel reviewer execution
- Full L1 → L2 → L3 → Implementation flow

## Test Setup

### Step 1: Install All Agents and Commands

```bash
# Install all 5 agent configurations
cp /path/to/sdd-unified/agents/configs/*.yaml ~/.claude-code/agents/

# Install all commands (if not already done)
cp /path/to/sdd-unified/commands/slash/*.yaml ~/.claude-code/commands/

# Restart Claude Code
```

**Verify:** Check that all agents are loaded:
- sdd-ba
- sdd-architect
- sdd-pe
- sdd-le
- sdd-coder

### Step 2: Initialize Feature Workspace

```bash
cd sdd-unified/validation-tests
mkdir -p phase3-fsm-engine/{spec,design,design/l3_tasks,implementation,review}
cd phase3-fsm-engine

# Copy the complete workflow template
cp ../../templates/workflow.json.template ./workflow.json

# Copy the FSM use case as input
cp ../../use_cases/FSM_PARALLEL_WORKFLOW_ENGINE.md ./requirements_input.md
```

### Step 3: Initialize Context File

Create `context.json`:

```json
{
  "feature_name": "FSM Parallel Workflow Engine",
  "feature_id": "phase3-validation",
  "current_phase": "requirements",
  "iteration_count": {
    "requirements": 0,
    "design_l1": 0,
    "design_l2": 0,
    "design_l3": 0,
    "implementation": 0
  },
  "decisions": [],
  "handover_notes": ""
}
```

## Phase 3A: Requirements Definition (BA Agent)

**In Claude Code:**

```
You are the sdd-ba agent. Read requirements_input.md and create:
1. spec/requirements.md - Human-readable requirements
2. spec/spec.yaml - Machine-readable specification

Update workflow.json to mark "define-requirements" as COMPLETED.
```

**Success Criteria:**
- ✅ spec/requirements.md created with clear requirements
- ✅ spec/spec.yaml created with structured data
- ✅ workflow.json updated: define-requirements = COMPLETED
- ✅ BA agent followed requirements-focused persona

**Time:** ~30 minutes

## Phase 3B: L1 Architecture (Architect Agent)

**In Claude Code:**

```
You are the sdd-architect agent. Based on spec/spec.yaml, create:
- design/l1_architecture.md

Include: System architecture, component boundaries, technology choices.
Update workflow.json to mark "design-l1" as COMPLETED.
```

**Success Criteria:**
- ✅ design/l1_architecture.md created
- ✅ High-level architecture defined
- ✅ workflow.json updated: design-l1 = COMPLETED

**Time:** ~30-45 minutes

## Phase 3C: L1 Reviews (Parallel Execution Test)

**Critical Test:** Can three agents review in parallel?

**In Claude Code:**

```
Execute the following review tasks in PARALLEL:
1. sdd-ba reviews L1 architecture (review-l1-ba)
2. sdd-pe reviews L1 architecture (review-l1-pe)
3. sdd-le reviews L1 architecture (review-l1-le)

Each creates review/{agent}_l1_review.json with outcome.
```

**Success Criteria:**
- ✅ Three review files created concurrently
- ✅ Each follows their agent's perspective (BA=business, PE=technical, LE=implementation)
- ✅ Reviews complete without waiting for each other
- ✅ All three marked COMPLETED in workflow.json

**Failure Mode to Test:**
If reviews show REJECTED status → Test rework loop:
- Should trigger "design-l1-rework" task
- Architect should receive feedback
- Circuit breaker should limit rework iterations

**Time:** ~20-30 minutes

## Phase 3D: L2 Component Design (PE Agent)

**In Claude Code:**

```
You are the sdd-pe agent. Create detailed component design:
- design/l2_component_design.md

Include: Class diagrams, API contracts, data models.
Update workflow.json: design-l2 = COMPLETED.
```

**Success Criteria:**
- ✅ L2 design created with technical details
- ✅ workflow.json updated

**Time:** ~45-60 minutes

## Phase 3E: L2 Reviews (Parallel)

**In Claude Code:**

```
Execute in parallel:
1. sdd-architect reviews L2 (review-l2-architect)
2. sdd-le reviews L2 (review-l2-le)

Create review files and update workflow.json.
```

**Success Criteria:**
- ✅ Two reviews complete concurrently
- ✅ Appropriate perspectives maintained

**Time:** ~15-20 minutes

## Phase 3F: L3 Task Breakdown (LE Agent)

**In Claude Code:**

```
You are the sdd-le agent. Break down implementation into discrete tasks:
- design/l3_tasks/task-001.md
- design/l3_tasks/task-002.md
- ... (create 5-10 tasks)

Each task must include:
- Clear scope
- Gherkin BDD acceptance criteria (Given/When/Then)
- Dependencies on other tasks

Update workflow.json: design-l3 = COMPLETED.
```

**Success Criteria:**
- ✅ 5-10 task files created
- ✅ Each has BDD criteria
- ✅ Tasks are discrete and testable
- ✅ Dependencies clear

**Time:** ~60-90 minutes

## Phase 3G: L3 Reviews (Parallel)

**In Claude Code:**

```
Execute in parallel:
1. sdd-pe reviews L3 task breakdown (review-l3-pe)
2. sdd-coder reviews L3 task breakdown (review-l3-coder)
```

**Success Criteria:**
- ✅ Reviews from different perspectives
- ✅ PE checks architectural alignment
- ✅ Coder checks implementability

**Time:** ~15-20 minutes

## Phase 3H: Implementation (Coder Agent - Critical Test)

**Question:** Can dynamic task execution work?

**In Claude Code:**

```
You are the sdd-coder agent. For each task in design/l3_tasks/:
1. Read the task specification
2. Implement the code
3. Create tests matching BDD criteria
4. Mark task as complete in workflow.json

Start with task-001.
```

**Success Criteria:**
- ✅ Code implements task requirements
- ✅ Tests verify BDD scenarios
- ✅ Each task marked COMPLETED individually
- ✅ Implementation follows architecture

**Time:** ~2-4 hours (depending on task count)

## Phase 3I: Code Reviews (Per Task)

**For each implemented task:**

```
You are the sdd-le agent. Review the implementation of task-XXX:
- Code quality
- Test coverage
- BDD criteria met
- Create review/task-XXX-review.json
```

**Success Criteria:**
- ✅ Each task reviewed individually
- ✅ Feedback specific to implementation
- ✅ Clear APPROVE/REJECT decisions

**Time:** ~30-60 minutes

## Phase 3J: Final Validation

**Check complete workflow:**

```bash
# View workflow status
cat workflow.json | python3 -m json.tool

# Count completed tasks
grep -o '"status": "COMPLETED"' workflow.json | wc -l

# Check all artifacts created
find . -type f -name "*.md" -o -name "*.yaml" -o -name "*.json"
```

**Success Criteria:**
- ✅ All tasks marked COMPLETED
- ✅ No tasks stuck in RUNNING
- ✅ All expected artifacts present
- ✅ Review cycles completed

## Critical Observations to Record

### 1. Workflow Execution Model

**Did Claude Code execute workflow.json as a DAG?**
- [ ] YES - Autonomous DAG execution
- [ ] PARTIAL - Manual task triggering needed
- [ ] NO - Required external orchestrator

**Notes:**

### 2. Parallel Execution

**Did parallel reviews actually execute concurrently?**
- [ ] YES - True parallel execution observed
- [ ] NO - Sequential execution despite parallel flag
- [ ] UNKNOWN - Could not determine

**Notes:**

### 3. Agent Context Preservation

**Did context carry over between agents?**
- [ ] YES - Each agent had previous work available
- [ ] PARTIAL - Some context lost
- [ ] NO - Each agent started fresh

**Notes:**

### 4. Status Management

**Who managed workflow.json updates?**
- [ ] Claude Code automatically
- [ ] Manual prompting required
- [ ] External script needed

**Notes:**

### 5. Review/Rework Loops

**Did rejection → rework cycles work?**
- [ ] YES - Automatic rework triggered
- [ ] PARTIAL - Manual intervention needed
- [ ] NO - Rework didn't happen
- [ ] NOT TESTED - No rejections occurred

**Notes:**

### 6. BDD Validation

**Were Gherkin criteria actually tested?**
- [ ] YES - Automated test verification
- [ ] NO - Manual verification only

**Notes:**

## Results Summary

### Overall Success Level

**Score each area 0-5:**

| Area | Score | Notes |
|------|-------|-------|
| Requirements Definition | /5 | |
| Architecture Design | /5 | |
| Task Breakdown | /5 | |
| Parallel Reviews | /5 | |
| Implementation | /5 | |
| Review Cycles | /5 | |
| Workflow Management | /5 | |

**Total: ___/35**

**Grade:**
- 30-35: A - Framework works as designed
- 25-29: B - Minor adjustments needed
- 20-24: C - Significant rework required
- Below 20: Framework needs major revision

### Critical Findings

**What worked well:**
1.
2.
3.

**What didn't work:**
1.
2.
3.

**Blockers encountered:**
1.
2.
3.

**Workarounds applied:**
1.
2.
3.

## Recommendations

Based on test results:

**If Grade A:**
→ Framework is validated and production-ready
→ Remove orchestrator.py (not needed)
→ Simplify installation
→ Document actual behavior
→ Ship v1.0

**If Grade B:**
→ Make documented adjustments
→ Re-test specific areas
→ Keep orchestrator.py as optional helper
→ Ship v1.0-beta

**If Grade C:**
→ Significant architecture revision needed
→ Keep orchestrator.py as required component
→ Timeline extends 4-6 weeks
→ Consider hybrid model

**If Below C:**
→ Fundamental assumptions invalid
→ Major redesign required
→ Timeline extends 2-3 months
→ Consider alternative approaches

## Next Steps

1. Document all findings in `validation-results.md`
2. Update ARCHITECTURE_CORRECTION.md with actual behavior
3. Revise CLAUDE.md based on learnings
4. Create decision: Keep or remove orchestrator.py
5. Update installation instructions
6. Plan v1.0 release or revision cycle

## Test Artifacts

Complete directory after Phase 3:

```
phase3-fsm-engine/
├── workflow.json                  # Complete workflow status
├── context.json                   # Agent handover state
├── requirements_input.md          # Original use case
├── spec/
│   ├── requirements.md           # BA output
│   └── spec.yaml                 # BA output
├── design/
│   ├── l1_architecture.md        # Architect output
│   ├── l2_component_design.md    # PE output
│   └── l3_tasks/                 # LE output
│       ├── task-001.md
│       ├── task-002.md
│       └── ...
├── implementation/
│   └── src/                      # Coder output
│       └── ...
└── review/                       # All reviews
    ├── ba_l1_review.json
    ├── pe_l1_review.json
    ├── le_l1_review.json
    ├── architect_l2_review.json
    ├── le_l2_review.json
    ├── pe_l3_review.json
    ├── coder_l3_review.json
    └── task-*-review.json
```

This becomes the reference implementation for framework usage.
