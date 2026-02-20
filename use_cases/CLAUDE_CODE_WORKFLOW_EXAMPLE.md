# SDD Unified Framework: Claude Code Workflow Example

## Complete End-to-End Feature Development

This use case demonstrates how to use the SDD Unified Framework with Claude Code to develop a complete feature autonomously.

**Feature:** User Authentication API with JWT Tokens

## Prerequisites

```bash
# Ensure the framework is installed
cd sdd-unified
bash scripts/install_claude.sh --scope=global

# Reload Claude Code to register agents and commands
# (Restart IDE or reload window)
```

## Autonomous Workflow Example

### Step 1: Initiate Feature Development

In Claude Code, simply use the `/feature` slash command:

```
/feature "Create a REST API for user authentication. Requirements: POST /login endpoint accepts username/password, returns JWT token on success, 401 on failure. Must use bcrypt for password hashing. Token expires in 2 hours."
```

### What Happens Behind the Scenes

The orchestrator springs to life and executes the entire workflow:

```
🚀 SDD Unified Framework - Autonomous Mode
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📁 Initializing feature workspace...
✓ Created: features/user-auth-api/
✓ Created: workflow.json from template
✓ Created: context.json

👔 Task: define-requirements
   Agent: sdd-ba
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   Loading context...
   Analyzing requirements prompt...
   Generating spec.yaml...
   ✓ Created: spec/spec.yaml (8 requirements)
   ✓ Updated: context.json (handover note to sdd-architect)
   ✓ Updated: workflow.json (define-requirements: COMPLETED)

🏗️ Task: design-l1
   Agent: sdd-architect
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   Loading context from previous agents...
   - Read: spec/spec.yaml
   - Read: context.json handover notes
   Designing L1 architecture...
   ✓ Created: design/l1_architecture.md
   Key decisions:
     • 3-tier architecture
     • bcrypt for password hashing (cost factor 12)
     • JWT with 2-hour expiration
   ✓ Updated: context.json
   ✓ Updated: workflow.json (design-l1: COMPLETED)

🔍 Task: review-l1-ba (parallel)
   Agent: sdd-ba
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   Validating L1 against requirements...
   ✓ All requirements addressed
   ✓ Created: review/review_l1_ba.json (APPROVED)
   ✓ Updated: review/review.log

🔍 Task: review-l1-pe (parallel)
   Agent: sdd-pe
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   Checking technical soundness...
   ⚠ Issue found: Missing password complexity requirements
   ✓ Created: review/review_l1_pe.json (REJECTED_WITH_FEEDBACK)
   ✓ Updated: review/review.log

🔍 Task: review-l1-le (parallel)
   Agent: sdd-le
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   Checking implementation clarity...
   ✓ Design is clear for L2
   ✓ Created: review/review_l1_le.json (APPROVED)

⚠ Review Status: 1 REJECTED - Triggering rework

🔧 Task: design-l1-rework
   Agent: sdd-architect
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   Loading all review feedback...
   - review_l1_pe.json: Missing password complexity
   Incorporating feedback...
   ✓ Updated: design/l1_architecture.md
   Added: Password policy (min 8 chars, 1 uppercase, 1 number, 1 special)
   ✓ Updated: workflow.json (design-l1-rework: COMPLETED)

🔄 Re-running L1 reviews...

🔍 review-l1-pe (retry)
   ✓ All issues addressed
   ✓ review_l1_pe.json (APPROVED)

✅ L1 Design: APPROVED by all reviewers

[Process continues through L2, L3, task generation, and implementation...]

🎯 Task: design-l3
   Agent: sdd-le
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   Decomposing L2 into tasks...
   ✓ Created: implementation/tasks/task-001.md (Create User model)
   ✓ Created: implementation/tasks/task-002.md (Implement password hashing)
   ✓ Created: implementation/tasks/task-003.md (Create JWT service)
   ✓ Created: implementation/tasks/task-004.md (Implement /login endpoint)
   Total: 4 tasks with BDD acceptance criteria

⌨️ Task: execute-task-001
   Agent: sdd-coder
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   Reading task definition...
   Acceptance Criteria:
     Given a User class is needed
     When the class is instantiated with username and hashed_password
     Then it should store these properties correctly
   ✓ Created: src/models/user.js
   ✓ Updated: workflow.json (execute-task-001: COMPLETED)

🔍 Task: review-task-001
   Agent: sdd-le
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   Verifying acceptance criteria...
   ✓ Code satisfies all criteria
   ✓ Created: review/review_task_001.json (APPROVED)

[Continues for tasks 002, 003, 004...]

✅ Feature Complete!
   All tasks implemented and approved.
   Summary:
   - 4 source files created
   - 4 tasks passed review
   - 0 reworks needed
   - Total time: ~15 minutes
```

## Manual Workflow Example

For more control, you can execute each step manually using individual slash commands:

### Initialization

```
/sdd-init "user-auth-api"
```

Creates the feature workspace and workflow.json.

### Requirements Phase

```
/sdd-define-requirements "POST /login endpoint with JWT authentication"
```

The `sdd-ba` agent creates `spec/spec.yaml`.

**Context Handover:**
- Outputs: spec/spec.yaml
- Updates: workflow.json, context.json
- Next: sdd-architect needs to read spec.yaml

### L1 Architecture Phase

```
/sdd-design-l1
```

The `sdd-architect` agent:
1. Loads context.json
2. Reads handover notes from sdd-ba
3. Reads spec/spec.yaml
4. Creates design/l1_architecture.md
5. Writes handover note for reviewers

### L1 Review Phase

```
/sdd-review-l1-ba
/sdd-review-l1-pe
/sdd-review-l1-le
```

Three agents review in parallel. Each:
1. Loads context
2. Reads l1_architecture.md
3. Validates against their criteria
4. Writes review/review_l1_{role}.json

**If any review is REJECTED:**

```
/sdd-rework-l1
```

The architect reads all feedback and creates an improved design.

### L2, L3, and Implementation

```
/sdd-design-l2
/sdd-review-l2-architect
/sdd-review-l2-le

/sdd-design-l3
/sdd-review-l3-pe
/sdd-review-l3-coder

/sdd-execute-task 001
/sdd-review-task 001

# ... continue for each task
```

## Context Management in Action

### Example context.json After L1 Completion

```json
{
  "feature_id": "user-auth-api",
  "current_phase": "review-l1",
  "context_sources": {
    "requirements": {
      "file": "spec/spec.yaml",
      "summary": "Authentication API with JWT, bcrypt hashing, 2-hour token expiry"
    },
    "l1_architecture": {
      "file": "design/l1_architecture.md",
      "status": "pending_review",
      "summary": "3-tier architecture: AuthController, AuthService, UserRepository. PostgreSQL for users, Redis for sessions."
    }
  },
  "handover_notes": {
    "history": [
      {
        "from_agent": "sdd-ba",
        "to_agent": "sdd-architect",
        "message": "Requirements complete. 8 FRs, 4 NFRs. Critical: NFR-003 requires 1000 req/sec throughput.",
        "critical_points": [
          "Must use bcrypt with minimum cost factor 10",
          "JWT tokens must include user_id and role claims"
        ]
      },
      {
        "from_agent": "sdd-architect",
        "to_agent": ["sdd-ba", "sdd-pe", "sdd-le"],
        "message": "L1 design complete. Key decision: Using microservices pattern for scalability. Auth Service separated from User Profile Service for independent scaling.",
        "critical_points": [
          "Chose PostgreSQL for ACID compliance in user data",
          "Redis cache for session tokens to hit performance target"
        ]
      }
    ]
  }
}
```

### Why This Matters

When `sdd-pe` starts the L2 design, they:

1. Read `context.json` to see what's been done
2. See the handover note explaining the microservices decision
3. Read `spec/spec.yaml` to understand requirements
4. Read `design/l1_architecture.md` to understand the architecture
5. Have full context to create a coherent L2 design

**No information is lost. Every agent has perfect situational awareness.**

## Autonomous vs Manual: When to Use Each

### Use Autonomous Mode (`/feature`) When:
- Starting a new feature from scratch
- You trust the framework to handle the standard workflow
- You want rapid prototyping
- The requirements are clear and stable

### Use Manual Mode (`/sdd-*` commands) When:
- You want to review each step before proceeding
- Requirements are complex or uncertain
- You're learning the framework
- You need to debug or investigate specific phases
- You want to manually intervene in the design process

### Mixed Mode

You can start autonomous and then interrupt:

```
/feature "Payment processing API"

# ... framework runs autonomously ...
# ... you notice an issue during L2 review ...

# Stop the autonomous execution (Ctrl+C or interrupt)
# Fix the issue manually
/sdd-rework-l2

# Resume autonomous execution
/feature-continue
```

## Key Insights


## Circuit Breaker: Handling Review Loops

### Scenario: When Agents Can't Converge

Sometimes agents get stuck in review/rework cycles. Here's how the circuit breaker protects against infinite loops:

```
🚀 Autonomous execution running...

🏗️ Task: design-l1 (Attempt 1)
   ✓ Created design/l1_architecture.md

🔍 Review: review-l1-pe
   ⚠ REJECTED: "Missing horizontal scaling strategy"

🔧 Task: design-l1-rework (Attempt 2)
   ✓ Added Kubernetes scaling approach

🔍 Review: review-l1-pe (retry)
   ⚠ REJECTED: "Database sharding strategy not defined"

🔧 Task: design-l1-rework (Attempt 3)
   ✓ Added database sharding details

🔍 Review: review-l1-pe (retry)
   ⚠ REJECTED: "Disaster recovery plan missing"

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
⚠ CIRCUIT BREAKER TRIGGERED
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

Task: design-l1
Attempts: 3/3 (maximum limit reached)

The review/rework cycle has not converged after 3 iterations.
This indicates a fundamental issue requiring human judgment.

Review History:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Attempt 1: REJECTED by sdd-pe
  Issue: Missing horizontal scaling strategy

Attempt 2: REJECTED by sdd-pe  
  Issue: Database sharding strategy not defined

Attempt 3: REJECTED by sdd-pe
  Issue: Disaster recovery plan missing

Pattern Detected: Requirements scope is expanding beyond L1
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Human Intervention Required

Options:
1. Override review - Force APPROVED and continue
2. Provide specific instructions to the reviewing agent
3. Manually edit the design document
4. Abort workflow and reassess requirements

Your choice [1-4]: 
```

### Human Response: Option 2 (Provide Guidance)

```
Your choice [1-4]: 2

Provide instructions for the sdd-pe agent:
> "The DR concerns are valid but beyond L1 architectural scope. 
  Create ADR-003 documenting that disaster recovery strategy 
  will be detailed in L2 component design where specific 
  components can have tailored DR approaches. With this ADR, 
  approve the L1 design."

✓ Instructions recorded in context.json
✓ Creating ADR-003: Disaster Recovery Strategy (Deferred to L2)
✓ Re-triggering review-l1-pe with enhanced context...

🔍 Review: review-l1-pe (with human guidance)
   Loading human instructions from context...
   Reading ADR-003...
   Validating scope alignment...
   ✓ APPROVED - L1 scope is appropriate with ADR documentation

✅ Circuit breaker cleared
✅ Workflow resuming autonomous execution

🎯 Task: design-l2
   Agent: sdd-pe (now with clear scope understanding)
   ... continues ...
```

### Why Circuit Breakers Matter

1. **Prevents Wasted Compute**: Stops endless loops burning resources
2. **Identifies Blockers**: Flags genuine problems vs. minor issues
3. **Human Expertise**: Leverages human judgment for complex situations
4. **Maintains Momentum**: Quick resolution keeps workflow moving
5. **Learning Opportunity**: Patterns in triggers improve future requirements

### Configurable Limits

Adjust thresholds based on project complexity:

```bash
# Via slash command
/sdd-config set-loop-limit design 5    # More iterations for complex designs
/sdd-config set-loop-limit task 2      # Code should converge faster

# Current limits shown:
/sdd-config show-limits
```

Output:
```
Current Circuit Breaker Limits:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Design Phases:
  design-l1: 3 iterations
  design-l2: 3 iterations
  design-l3: 4 iterations (more complex)

Implementation:
  execute-task: 2 iterations
  review-task: 2 iterations

Global Default: 3 iterations
```

1. **Context is King**: The `context.json` manifest is the single source of truth about the feature's current state
2. **Stateless Agents**: Agents load fresh context every time - no hidden state
3. **Workflow is the Guide**: `workflow.json` defines what can run and when
4. **Reviews are Gates**: No progress until all reviewers approve
5. **Handover Notes**: Explicit communication between agents prevents information loss

This architecture enables true autonomous development while preserving the ability to manually intervene at any point.