# Task-Driven Implementation Design

**Version:** 1.0.0  
**Status:** Core Architecture  
**Last Updated:** 2025-10-16

## The Anti-Pattern: Monolithic Implementation Plans

Traditional SDD approaches produce a single, monolithic implementation plan (e.g., `l3_plan.md`) that:
- Describes ALL work in one document
- Is difficult to verify incrementally
- Doesn't support parallel execution
- Lacks clear acceptance criteria
- Can't track granular progress

**This is an anti-pattern.** sdd_unified replaces it with discrete, verifiable tasks.

## The Solution: BDD-Verified Task System

### Key Innovation

Instead of a monolithic `l3_plan.md`, the `design-l3` command generates **discrete task files** in `implementation/tasks/`:

```
implementation/
└── tasks/
    ├── task-001.md
    ├── task-002.md
    ├── task-003.md
    └── ...
```

Each task is:
- **Discrete:** Can be implemented independently
- **Verifiable:** Has Gherkin BDD acceptance criteria
- **Trackable:** Individual status (pending/in-progress/done)
- **Parallelizable:** Tasks without dependencies can run concurrently

## Task File Schema

Every task file follows this structure:

```markdown
# Task: [Brief Description]

## Task Metadata

**Task ID:** task-XXX  
**Priority:** High/Medium/Low  
**Estimated Effort:** Small/Medium/Large  
**Dependencies:** [task-001, task-002] or None

## Description

[Clear description of what needs to be implemented]

## Acceptance Criteria (Gherkin BDD)

```gherkin
Feature: [Feature name]

Scenario: [Specific scenario]
  Given [precondition]
  And [additional precondition]
  When [action is performed]
  And [additional action]
  Then [expected outcome]
  And [additional outcome]
```

## Technical Details

### Files to Create/Modify
- `path/to/file1.ext` - [Purpose]
- `path/to/file2.ext` - [Purpose]

### Key Implementation Points
- [Technical consideration 1]
- [Technical consideration 2]

### Non-Functional Requirements
- Performance: [requirement]
- Security: [requirement]
- Error Handling: [requirement]

## Verification

After implementation, this task will be reviewed against the acceptance criteria by the sdd-le agent using `le/review-task` command.
```

## Example: Real Task File

**File:** `implementation/tasks/task-003.md`

```markdown
# Task: Implement JWT Token Generation

## Task Metadata

**Task ID:** task-003  
**Priority:** High  
**Estimated Effort:** Medium  
**Dependencies:** task-001 (User model), task-002 (Authentication service)

## Description

Implement JWT (JSON Web Token) generation functionality for user authentication. The system must create secure, time-limited tokens containing user identity and role information.

## Acceptance Criteria (Gherkin BDD)

```gherkin
Feature: JWT Token Generation

Scenario: Generate token for authenticated user
  Given a User object with id "12345" and role "admin"
  When the generateToken() method is called
  Then a valid JWT string is returned
  And the token payload contains user_id "12345"
  And the token payload contains role "admin"
  And the token expires in 24 hours
  And the token is signed with the application secret key

Scenario: Token validation
  Given a generated JWT token
  When the validateToken() method is called with the token
  Then the token is verified as valid
  And the user information is extracted correctly

Scenario: Expired token handling
  Given a JWT token that expired 1 hour ago
  When the validateToken() method is called
  Then an ExpiredTokenError is thrown
  And the error message indicates token expiration
```

## Technical Details

### Files to Create/Modify
- `src/auth/jwt_manager.py` - Create new file with JWTManager class
- `src/auth/__init__.py` - Export JWTManager
- `src/config/auth_config.py` - Add JWT secret and expiry configuration

### Key Implementation Points
- Use PyJWT library for token generation/validation
- Token should include: user_id, role, issued_at, expires_at
- Use HS256 algorithm for signing
- Secret key must be loaded from environment variable
- Include proper error handling for invalid/expired tokens

### Non-Functional Requirements
- Performance: Token generation < 10ms
- Security: Secret key must never be logged or exposed
- Error Handling: Clear error messages for different failure scenarios

## Verification

This task will be verified by sdd-le agent using the acceptance criteria. Implementation must satisfy all Gherkin scenarios.
```

## Workflow Integration

### L3 Design Phase (LE Agent)

The `le/design-l3` command:

1. **Analyzes L2 component design**
2. **Breaks down into discrete tasks**
3. **Generates task files** (task-001.md, task-002.md, ...)
4. **Writes Gherkin acceptance criteria** for each
5. **Identifies task dependencies**

**Output Location:** `implementation/tasks/*.md`

### Task Execution Phase (Coder Agent)

The `coder/execute-task` command takes a `task_id` parameter:

```yaml
# commands/coder/execute-task.yaml
name: execute-task
description: Execute a single implementation task
agent: sdd-coder
inputs:
  - task_id: string  # e.g., "task-003"
context:
  - Read: implementation/tasks/{task_id}.md
  - Read: design/l2_component_design.md
  - Read: context.json
outputs:
  - Source code files as specified in task
```

**Process:**
1. Coder reads task file
2. Understands acceptance criteria
3. Implements code to satisfy criteria
4. Creates/modifies files as specified
5. Updates context.json with completion notes

### Task Review Phase (LE Agent)

The `le/review-task` command verifies BDD criteria:

```yaml
# commands/le/review-task.yaml
name: review-task
description: Review task implementation against BDD criteria
agent: sdd-le
inputs:
  - task_id: string
context:
  - Read: implementation/tasks/{task_id}.md
  - Read: Source code files
outputs:
  - review/review_task_{task_id}.json
```

**Review Outcome:**
```json
{
  "task_id": "task-003",
  "status": "APPROVED" | "REJECTED_WITH_FEEDBACK",
  "acceptance_criteria_results": [
    {
      "scenario": "Generate token for authenticated user",
      "passed": true,
      "notes": "All assertions verified"
    },
    {
      "scenario": "Token validation",
      "passed": true,
      "notes": "Validation logic correct"
    }
  ],
  "feedback": "Implementation meets all criteria",
  "approved_by": "sdd-le",
  "timestamp": "2025-10-16T08:00:00Z"
}
```

## Updated Workflow DAG

**Before (Monolithic):**
```
design-l3 → implement-code → review-code
```

**After (Task-Driven):**
```
design-l3 → review-l3 → [execute-task-001, execute-task-002, execute-task-003] → review-tasks → done
                                ↑ parallel execution ↑
```

### Parallel Execution

Tasks without dependencies can run in parallel:

```json
{
  "nodes": [
    {
      "id": "execute-task-001",
      "dependencies": ["design-l3-approved"],
      "agent": "sdd-coder"
    },
    {
      "id": "execute-task-002",
      "dependencies": ["design-l3-approved"],  // Same dependency
      "agent": "sdd-coder"
    },
    {
      "id": "execute-task-003",
      "dependencies": ["execute-task-001", "execute-task-002"],  // Sequential
      "agent": "sdd-coder"
    }
  ]
}
```

## BDD Verification Strategy

### Gherkin Syntax

All acceptance criteria use Gherkin's Given/When/Then format:

- **Given:** Preconditions/context
- **When:** Action being tested
- **Then:** Expected outcome

### Verification Methods

**Option 1: Manual Review (Current)**
- LE agent reads code and criteria
- Manually verifies each scenario
- Documents results in review file

**Option 2: Automated Testing (Future)**
- Generate test code from Gherkin
- Execute tests automatically
- Report pass/fail results

**Option 3: LLM-Assisted (Hybrid)**
- LLM analyzes code vs. criteria
- Flags potential issues
- Human confirms verification

### Acceptance Criteria Quality

Good acceptance criteria are:
- ✅ **Specific:** Exact inputs and outputs
- ✅ **Testable:** Can be verified objectively
- ✅ **Independent:** Each scenario tests one thing
- ✅ **Complete:** Cover all requirements
- ❌ **Not vague:** Avoid "should work well"
- ❌ **Not implementation:** Don't prescribe HOW

## Benefits Over Monolithic Plans

| Aspect | Monolithic Plan | Task-Driven |
|--------|----------------|-------------|
| **Granularity** | One big document | Discrete tasks |
| **Verifiability** | Subjective review | BDD criteria |
| **Progress Tracking** | Binary (done/not done) | Per-task status |
| **Parallel Work** | Sequential only | Parallel where possible |
| **Rework Scope** | Redo entire plan | Rework single task |
| **Clarity** | Mixed details | Focused purpose |

## Task Dependencies

Tasks declare dependencies explicitly:

```markdown
**Dependencies:** task-001, task-002
```

This enables:
- Automatic dependency resolution
- Parallel execution of independent tasks
- Clear sequencing when required

## Best Practices

### Writing Tasks

1. **One Purpose Per Task**
   - ❌ "Implement auth system"
   - ✅ "Implement JWT token generation"

2. **Clear Acceptance Criteria**
   - Use concrete examples
   - Specify exact inputs/outputs
   - Include edge cases

3. **Right-Sized Tasks**
   - Too small: Task overhead dominates
   - Too large: Difficult to verify
   - Goldilocks: 1-2 hours of work

4. **Explicit Dependencies**
   - List all prerequisite tasks
   - Don't assume implicit dependencies

### Task Execution

1. **Read Task Fully** before coding
2. **Understand BDD Criteria** before implementing
3. **Write Tests** (if automated verification)
4. **Document Assumptions** in code comments
5. **Update Context** after completion

### Task Review

1. **Verify Each Scenario** individually
2. **Check Edge Cases** not just happy path
3. **Document Findings** clearly
4. **Provide Actionable Feedback** if rejected

## Circuit Breaker for Tasks

Each task has a rework limit:

```json
{
  "id": "rework-task-003",
  "max_iterations": 2,
  "on_exceed": "escalate-to-human"
}
```

If a task is rejected twice, human intervention is required.

## Migration from Monolithic

**Old Structure:**
```
implementation/
└── l3_plan.md  (5000 lines of mixed detail)
```

**New Structure:**
```
implementation/
└── tasks/
    ├── task-001.md (50 lines, focused)
    ├── task-002.md (75 lines, focused)
    └── task-003.md (100 lines, focused)
```

## Example: Complete Task Breakdown

**Feature:** User Authentication API

**L2 Components:**
- User model
- Authentication service
- JWT manager
- Login/logout endpoints

**L3 Tasks:**
1. task-001: Create User model
2. task-002: Implement password hashing
3. task-003: Implement JWT generation
4. task-004: Implement authentication service
5. task-005: Create login endpoint
6. task-006: Create logout endpoint
7. task-007: Add authentication middleware

Each task has:
- Own file
- BDD criteria
- Clear dependencies
- Verification process

## Summary

The task-driven implementation model:
- ✅ Replaces monolithic plans with discrete tasks
- ✅ Uses Gherkin BDD for verifiability
- ✅ Enables parallel execution
- ✅ Provides granular progress tracking
- ✅ Supports focused rework
- ✅ Integrates with workflow DAG

**Key Files:**
- Task files: `implementation/tasks/task-*.md`
- Execution command: `commands/coder/execute-task.yaml`
- Review command: `commands/le/review-task.yaml`

**Related Documentation:**
- [Workflow Engine](workflow_engine.md)
- [Iterative Reviews](iterative_reviews.md)
- [Context Management](context_management.md)