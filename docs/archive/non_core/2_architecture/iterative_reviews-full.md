# Iterative Review Architecture

**Version:** 1.0.0  
**Status:** Core Architecture  
**Last Updated:** 2025-10-16

## The Missing Feedback Loop

Traditional SDD workflows have a critical flaw: **reviews are "fire-and-forget"** with no mechanism to iterate when designs are rejected.

```
Design → Review → [Approved] → Continue
                ↘ [Rejected] → ??? (workflow ends)
```

This is unrealistic. In real development:
- First designs are rarely perfect
- Reviews identify issues that need addressing
- Iteration is expected and necessary
- Convergence through feedback loops

## The Solution: Formal Review/Rework Cycles

sdd-unified introduces **formal iterative review cycles** with automatic rework triggering and circuit breakers.

### Key Components

1. **Review Outcome Files** (JSON format)
2. **Rework Commands** (triggered on rejection)
3. **Circuit Breakers** (prevent infinite loops)
4. **Human Intervention Protocol** (when loops don't converge)

## Review Outcome Files

Every review produces a structured JSON file with explicit status:

**File:** `review/review_l1_ba.json`

```json
{
  "review_id": "review_l1_ba_001",
  "artifact": "design/l1_architecture.md",
  "reviewer": "sdd-ba",
  "status": "APPROVED" | "REJECTED_WITH_FEEDBACK",
  "timestamp": "2025-10-16T08:00:00Z",
  "iteration": 1,
  "findings": [
    {
      "category": "requirements_alignment",
      "severity": "critical",
      "location": "Section 3.2",
      "issue": "Database choice doesn't align with scalability requirements",
      "recommendation": "Consider distributed database for horizontal scaling"
    },
    {
      "category": "completeness",
      "severity": "minor",
      "issue": "Missing error handling strategy",
      "recommendation": "Add section on error handling patterns"
    }
  ],
  "overall_assessment": "Design needs revision to address scalability concerns",
  "next_step": "design-l1-rework"
}
```

### Review Statuses

**APPROVED**
- All requirements met
- No critical issues found
- Ready to proceed to next phase
- Workflow continues forward

**REJECTED_WITH_FEEDBACK**
- Critical issues identified
- Changes required before proceeding
- Specific feedback provided
- Triggers rework command

## Evidence-Based Gate Policy

Formal review decisions should be based on evidence, not confidence-only statements.

Required evidence by default:
- requirement coverage mapping exists
- acceptance criteria are testable
- relevant validation checks are attached (tests, lint, static checks)

Additional evidence for higher-risk changes:
- security/dependency results
- release/rollback notes

In pair overlay mode, reviewers must be independent from the producing pair.

## Review Phases

### L1 Architecture Review

**Reviewers:** BA, PE, LE (3 perspectives)

**Checklist:**
- ✓ Aligns with requirements
- ✓ Addresses all functional needs
- ✓ Considers non-functional requirements
- ✓ Scalable and maintainable
- ✓ Technology choices justified

**Outcome:**
- All 3 approve → Proceed to L2
- Any reject → Trigger `design-l1-rework`

### L2 Component Review

**Reviewers:** Architect, LE (2 perspectives)

**Checklist:**
- ✓ Components align with L1 architecture
- ✓ Interfaces clearly defined
- ✓ Data flow logical
- ✓ Component boundaries appropriate
- ✓ Implementation feasible

**Outcome:**
- Both approve → Proceed to L3
- Either reject → Trigger `design-l2-rework`

### L3 Task Review

**Reviewer:** PE (technical oversight)

**Checklist:**
- ✓ Tasks are discrete and focused
- ✓ BDD acceptance criteria are clear
- ✓ Dependencies correctly identified
- ✓ Task sizing appropriate
- ✓ All L2 components covered

**Outcome:**
- Approve → Proceed to implementation
- Reject → Trigger `design-l3-rework`

### Task Implementation Review

**Reviewer:** LE (per-task)

**Checklist:**
- ✓ Gherkin scenarios satisfied
- ✓ Code quality acceptable
- ✓ Error handling present
- ✓ Documentation included
- ✓ No regressions introduced

**Outcome:**
- Approve → Task complete
- Reject → Trigger `rework-task-XXX`

## Rework Commands

Each design phase has a corresponding rework command:

### `design-l1-rework.yaml`

```yaml
name: design-l1-rework
description: Revise L1 architecture based on review feedback
agent: sdd-architect
inputs:
  - review_files: [review_l1_ba.json, review_l1_pe.json, review_l1_le.json]
context:
  - Read: design/l1_architecture.md (current version)
  - Read: All review outcome files
  - Read: spec/requirements.md
  - Read: context.json
process:
  - Analyze all review feedback
  - Identify common themes in rejections
  - Revise design to address critical issues
  - Maintain consistency with requirements
  - Document changes made
outputs:
  - design/l1_architecture.md (updated)
  - context.json (updated with iteration notes)
iteration_tracking:
  - Increment: context.iteration_counts.design_l1
  - Max: 3
  - On_exceed: escalate_to_human
```

**Key Features:**
- Reads ALL review feedback
- Iterates on existing design
- Tracks iteration count
- Enforces maximum iterations

### `design-l2-rework.yaml`

Similar structure for L2 component design revisions.

### `design-l3-rework.yaml`

Similar structure for L3 task breakdown revisions.

### `rework-task-XXX.yaml`

```yaml
name: rework-task
description: Fix implementation based on review feedback
agent: sdd-coder
inputs:
  - task_id: string
  - review_file: review_task_{task_id}.json
context:
  - Read: implementation/tasks/{task_id}.md
  - Read: review/review_task_{task_id}.json
  - Read: Source code files
outputs:
  - Source code files (updated)
  - context.json (iteration notes)
iteration_tracking:
  - Max: 2
  - On_exceed: escalate_to_human
```

## Workflow DAG with Feedback Loops

```
┌─────────────────────────────────────────┐
│  L1 Architecture Phase                  │
└─────────────────┬───────────────────────┘
                  ↓
        ┌─────────────────┐
        │  design-l1      │
        └────────┬─────────┘
                 ↓
    ┌────────────────────────┐
    │  Review L1             │
    │  (BA, PE, LE)          │
    └─────┬──────────────┬───┘
          ↓              ↓
    [APPROVED]    [REJECTED]
          ↓              ↓
          │      ┌───────────────┐
          │      │design-l1-rework│
          │      └───────┬───────┘
          │              ↓
          │      (iteration < 3?)
          │         ↓         ↓
          │       Yes        No
          │         ↓         ↓
          │    (back to)  (human)
          │    review    intervention
          ↓
┌─────────────────────────────────────────┐
│  L2 Component Phase                     │
└─────────────────┬───────────────────────┘
                  ↓
        (similar cycle)
```

## Circuit Breaker Pattern

### Why Circuit Breakers?

Without limits, review/rework cycles could loop infinitely:
- Designer misunderstands feedback
- Reviewers have conflicting requirements
- Requirements are unclear/contradictory
- Technical constraints prevent ideal solution

### Iteration Limits

| Phase | Max Iterations | Rationale |
|-------|---------------|-----------|
| L1 Design | 3 | High-level, should converge quickly |
| L2 Design | 3 | Component details need refinement |
| L3 Design | 3 | Task breakdown is iterative |
| Task Implementation | 2 | Code should be right after one fix |

### Tracking Iterations

In `context.json`:

```json
{
  "iteration_counts": {
    "design_l1": 2,
    "design_l2": 0,
    "design_l3": 1,
    "task_001": 1,
    "task_002": 0
  }
}
```

Each rework command increments the counter.

### Circuit Breaker Trigger

When max iterations exceeded:

```yaml
on_exceed: escalate_to_human
```

This triggers the human intervention protocol.

## Human Intervention Protocol

### When Triggered

- Design phase exceeds 3 iterations
- Task implementation exceeds 2 iterations
- Review outcomes are contradictory
- System detects infinite loop pattern

### Intervention Process

**1. Pause Workflow**
```
Workflow paused at: design-l1-rework (iteration 4)
Reason: Maximum iterations exceeded
```

**2. Present Context**
```
- Current artifact: design/l1_architecture.md
- Review history: [review_l1_ba.json (rejected), review_l1_pe.json (rejected), ...]
- Iteration count: 4 (max: 3)
- Key issues: [scalability concerns, technology choices, ...]
```

**3. Request Human Input**
```
Options:
1. Override and approve current design
2. Provide clarifying requirements
3. Resolve contradictory feedback
4. Adjust acceptance criteria
5. Abort feature development
```

**4. Resume Workflow**

Based on human decision:
- **Override → Approve:** Continue to next phase
- **Clarify → Rework:** One more iteration with new context
- **Resolve → Review:** Re-review with conflict resolution
- **Adjust → Update:** Modify criteria and re-evaluate
- **Abort → Cancel:** Stop feature development

## Review Outcome Processing

### Conditional Logic in Workflow

```json
{
  "id": "check-l1-reviews",
  "type": "condition",
  "condition": {
    "all_of": [
      "review_l1_ba.status == APPROVED",
      "review_l1_pe.status == APPROVED",
      "review_l1_le.status == APPROVED"
    ]
  },
  "on_true": "design-l2",
  "on_false": "design-l1-rework"
}
```

### Aggregating Multiple Reviews

**Strategy 1: All Must Approve**
```
Approved if: ALL reviewers approve
Rejected if: ANY reviewer rejects
```

**Strategy 2: Majority Vote**
```
Approved if: 2+ of 3 reviewers approve
Rejected if: 2+ of 3 reviewers reject
```

**Strategy 3: Weighted Consensus**
```
BA: 40% weight (requirements authority)
PE: 30% weight (technical authority)
LE: 30% weight (implementation authority)
Approved if: Weighted score > 70%
```

**Current Implementation:** All Must Approve (most rigorous)

## Feedback Quality

### Effective Feedback

✅ **Specific:** "Database choice doesn't support horizontal scaling requirement R-3.2"  
❌ **Vague:** "Database seems wrong"

✅ **Actionable:** "Add caching layer using Redis to meet latency requirement"  
❌ **Unhelpful:** "Performance might be an issue"

✅ **Referenced:** "Section 4.1 contradicts requirement R-5.1"  
❌ **Unreferenced:** "Something's not right"

### Review Templates

Each review command uses structured templates:

```markdown
## Alignment Review
- [ ] Aligns with requirement R-X
- [ ] Addresses use case UC-Y
- [ ] Satisfies constraint C-Z

## Technical Review
- [ ] Technology choice justified
- [ ] Scalability addressed
- [ ] Security considered
- [ ] Error handling defined

## Completeness Review
- [ ] All components identified
- [ ] Interfaces specified
- [ ] Data flow documented
- [ ] Dependencies listed
```

## Context Handover

Each rework command receives:

1. **Original Artifact:** What was designed
2. **All Review Feedback:** What's wrong
3. **Requirements:** What's needed
4. **Previous Iterations:** What was tried
5. **Iteration Count:** How many attempts

This enables informed revision.

## Benefits of Iterative Reviews

| Aspect | Fire-and-Forget | Iterative Cycles |
|--------|-----------------|------------------|
| **Convergence** | Fails on rejection | Iterates to approval |
| **Feedback Loop** | None | Formal |
| **Quality** | First-attempt only | Refined through iteration |
| **Realism** | Unrealistic | Matches real development |
| **Safety** | Can loop forever | Circuit breakers |
| **Human Role** | Always required | Only when stuck |

## Integration with Task-Driven Model

Reviews happen at multiple granularities:

- **Design Reviews:** L1, L2, L3 (strategic)
- **Task Reviews:** Per-task (tactical)

Both use the same review/rework pattern.

## Audit Trail

All reviews create permanent records:

```
feature-001-auth/
└── review/
    ├── review_l1_ba.json
    ├── review_l1_pe.json
    ├── review_l1_le.json
    ├── review_l2_architect.json
    ├── review_l2_le.json
    ├── review_l3_pe.json
    ├── review_task_001.json
    └── review_task_002.json
```

This provides:
- Full review history
- Decision rationale
- Quality evidence
- Compliance documentation

## Summary

The iterative review architecture:
- ✅ Introduces formal feedback loops
- ✅ Automatic rework triggering
- ✅ Circuit breakers prevent infinite loops
- ✅ Human intervention when needed
- ✅ Matches realistic development process
- ✅ Creates audit trail

**Key Files:**
- Review outcome format: JSON with APPROVED/REJECTED_WITH_FEEDBACK
- Rework commands: `*-rework.yaml` for each phase
- Circuit breaker: `context.json` iteration tracking

**Related Documentation:**
- [Workflow Engine](workflow_engine.md)
- [Task-Driven Implementation](task_driven_implementation.md)
- [Context Management](context_management.md)
