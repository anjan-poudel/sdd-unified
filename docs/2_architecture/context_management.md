# Context Management Design

**Version:** 1.0.0  
**Status:** Core Architecture  
**Last Updated:** 2025-10-16

## The Critical Challenge

**Context preservation is THE hardest problem in multi-agent systems.**

When agents switch during a workflow, information is lost:
- Why decisions were made
- What was tried and failed
- What requirements drive the design
- What iteration we're on
- What the previous agent learned

**Without context management, each agent starts from scratch.**

## The Solution: context.json Manifest

sdd_unified introduces a **formal context manifest** that travels with each feature, providing:

1. **State Tracking:** Current phase, completed tasks
2. **Handover Notes:** Agent-to-agent information transfer
3. **Iteration Tracking:** Circuit breaker counters
4. **Decision History:** Why choices were made
5. **Review History:** What feedback was given

## Context File Location

Every feature has its own context:

```
features/
└── feature-001-auth/
    ├── context.json  ← Central context manifest
    ├── spec/
    ├── design/
    ├── implementation/
    └── review/
```

## Complete Context Schema

```json
{
  "feature_id": "feature-001-auth",
  "feature_name": "User Authentication",
  "workflow_version": "1.0.0",
  "created_at": "2025-10-16T08:00:00Z",
  "updated_at": "2025-10-16T10:30:00Z",
  
  "current_state": {
    "phase": "l2_design",
    "active_agent": "sdd-pe",
    "active_task": "design-l2",
    "status": "in_progress"
  },
  
  "completed_phases": [
    {
      "phase": "requirements",
      "agent": "sdd-ba",
      "completed_at": "2025-10-16T08:15:00Z",
      "outputs": ["spec/requirements.md", "spec/spec.yaml"]
    },
    {
      "phase": "l1_design",
      "agent": "sdd-architect",
      "completed_at": "2025-10-16T09:00:00Z",
      "iterations": 2,
      "outputs": ["design/l1_architecture.md"]
    }
  ],
  
  "iteration_counts": {
    "design_l1": 2,
    "design_l2": 0,
    "design_l3": 0,
    "task_001": 0
  },
  
  "circuit_breaker_status": {
    "design_l1": {
      "current": 2,
      "max": 3,
      "status": "ok"
    },
    "design_l2": {
      "current": 0,
      "max": 3,
      "status": "ok"
    }
  },
  
  "handover_notes": [
    {
      "from": "sdd-ba",
      "to": "sdd-architect",
      "timestamp": "2025-10-16T08:15:00Z",
      "priority": "high",
      "note": "Critical requirement R-3.2 mandates horizontal scalability. Consider distributed architecture from the start. Performance budget: 100ms p95 latency."
    },
    {
      "from": "sdd-architect",
      "to": "sdd-pe",
      "timestamp": "2025-10-16T09:00:00Z",
      "priority": "high",
      "note": "L1 went through 2 iterations. Initial design used monolithic DB which failed scalability review. Final design uses microservices with event-driven communication. PE should focus on inter-service contracts."
    }
  ],
  
  "decisions": [
    {
      "id": "DEC-001",
      "made_by": "sdd-architect",
      "timestamp": "2025-10-16T08:30:00Z",
      "decision": "Use microservices architecture instead of monolith",
      "rationale": "Horizontal scalability requirement R-3.2 cannot be met with monolith",
      "alternatives_considered": ["Modular monolith", "Serverless"],
      "trade_offs": "Increased complexity for operational scalability"
    },
    {
      "id": "DEC-002",
      "made_by": "sdd-architect",
      "timestamp": "2025-10-16T08:45:00Z",
      "decision": "Event-driven communication between services",
      "rationale": "Loose coupling required for independent scaling",
      "alternatives_considered": ["REST APIs", "gRPC"],
      "trade_offs": "Eventual consistency vs strong consistency"
    }
  ],
  
  "review_history": [
    {
      "artifact": "design/l1_architecture.md",
      "iteration": 1,
      "reviewer": "sdd-ba",
      "status": "REJECTED_WITH_FEEDBACK",
      "timestamp": "2025-10-16T08:20:00Z",
      "key_issues": ["Monolithic DB doesn't scale", "Missing caching strategy"]
    },
    {
      "artifact": "design/l1_architecture.md",
      "iteration": 2,
      "reviewer": "sdd-ba",
      "status": "APPROVED",
      "timestamp": "2025-10-16T08:55:00Z",
      "key_issues": []
    }
  ],
  
  "requirements_summary": {
    "functional": [
      "F-1: User registration and login",
      "F-2: JWT token-based authentication",
      "F-3: Role-based access control"
    ],
    "non_functional": [
      "R-3.2: Support 10K concurrent users (horizontal scalability)",
      "R-4.1: 100ms p95 response time",
      "R-5.1: 99.9% availability"
    ],
    "constraints": [
      "C-1: Must use existing AWS infrastructure",
      "C-2: No GPL-licensed dependencies"
    ]
  },
  
  "dependencies": {
    "external": ["AWS RDS", "Redis", "Kafka"],
    "internal": ["user-service", "auth-service"],
    "blockers": []
  },
  
  "risks": [
    {
      "id": "RISK-001",
      "severity": "medium",
      "description": "Event-driven eventual consistency may confuse users",
      "mitigation": "Add UI feedback for async operations",
      "status": "mitigated"
    }
  ],
  
  "metrics": {
    "total_tasks": 0,
    "completed_tasks": 0,
    "review_iterations": 2,
    "total_time_hours": 2.5,
    "estimated_completion": "2025-10-18"
  }
}
```

## Context Updates

### Who Updates Context?

**Every agent updates context after completing their task:**

- **sdd-ba:** After requirements → Adds requirements summary, initial handover note
- **sdd-architect:** After L1 design → Adds decisions, handover to PE
- **sdd-pe:** After L2 design → Adds component decisions, handover to LE
- **sdd-le:** After L3 tasks → Adds task breakdown notes, handover to Coder
- **sdd-coder:** After each task → Updates task completion status

### Update Pattern

Each agent's command includes context update:

```yaml
# Example: commands/architect/design-l1.yaml
outputs:
  - design/l1_architecture.md
  - context.json  # Updated with decisions and handover notes
```

**Update Process:**
1. Read current context.json
2. Add new information (handover notes, decisions, etc.)
3. Update current_state
4. Increment iteration_count if applicable
5. Write updated context.json

## Handover Notes

### Purpose

Handover notes transfer **critical information** between agents that isn't captured elsewhere.

### Effective Handover Notes

✅ **Good Handover Note:**
```json
{
  "from": "sdd-architect",
  "to": "sdd-pe",
  "priority": "critical",
  "note": "L1 design went through 2 iterations due to scalability concerns. Originally proposed MongoDB but reviews flagged inability to shard effectively. Final design uses PostgreSQL with read replicas. PE must ensure L2 component design accommodates read-heavy workload with 80:20 read-write ratio."
}
```

❌ **Poor Handover Note:**
```json
{
  "note": "Design is done, please continue"
}
```

### Handover Note Template

```json
{
  "from": "agent-name",
  "to": "agent-name",
  "timestamp": "ISO-8601",
  "priority": "critical|high|medium|low",
  "note": "Concise summary of critical information",
  "related_artifacts": ["path/to/file"],
  "action_items": ["What the next agent should focus on"]
}
```

## Decision Tracking

### Why Track Decisions?

Decisions made early affect later work. Tracking them:
- Prevents contradictory choices
- Provides rationale for reviewers
- Enables informed iteration
- Creates audit trail

### Decision Format

```json
{
  "id": "DEC-XXX",
  "made_by": "agent-name",
  "timestamp": "ISO-8601",
  "decision": "What was decided",
  "rationale": "Why this was chosen",
  "alternatives_considered": ["Option A", "Option B"],
  "trade_offs": "What was sacrificed",
  "related_requirements": ["R-X", "R-Y"],
  "related_decisions": ["DEC-001"]  // Dependencies
}
```

### Example Decision Chain

```
DEC-001: Microservices architecture
  ↓ (enables)
DEC-002: Event-driven communication
  ↓ (requires)
DEC-003: Kafka message broker
  ↓ (implies)
DEC-004: Eventual consistency model
```

## Iteration Tracking

### Circuit Breaker Integration

Context tracks iterations for circuit breaker enforcement:

```json
{
  "iteration_counts": {
    "design_l1": 2,  // 2 iterations (original + 1 rework)
    "design_l2": 0,  // First attempt
    "task_003": 1    // 1 rework
  },
  "circuit_breaker_status": {
    "design_l1": {
      "current": 2,
      "max": 3,
      "status": "ok"  // Not triggered
    }
  }
}
```

### Increment Logic

Each rework command increments:

```python
# Pseudocode in rework command
current = context["iteration_counts"]["design_l1"]
max_allowed = 3

if current >= max_allowed:
    trigger_human_intervention()
else:
    context["iteration_counts"]["design_l1"] += 1
    proceed_with_rework()
```

## Review History

### Tracking Review Outcomes

```json
{
  "review_history": [
    {
      "artifact": "design/l1_architecture.md",
      "iteration": 1,
      "reviewer": "sdd-ba",
      "status": "REJECTED_WITH_FEEDBACK",
      "timestamp": "2025-10-16T08:20:00Z",
      "key_issues": [
        "Scalability concern: Monolithic DB",
        "Missing: Caching strategy"
      ],
      "review_file": "review/review_l1_ba_iter1.json"
    },
    {
      "artifact": "design/l1_architecture.md",
      "iteration": 2,
      "reviewer": "sdd-ba",
      "status": "APPROVED",
      "timestamp": "2025-10-16T08:55:00Z",
      "key_issues": [],
      "review_file": "review/review_l1_ba_iter2.json"
    }
  ]
}
```

### Benefits

- See progression through iterations
- Understand what changed between versions
- Verify all feedback was addressed
- Audit trail for compliance

## Context Loading Mechanism

### Question: How Do Agents Access Context?

**Option 1: Explicit Instruction** (Manual)
```yaml
# In command prompt template
You are the architect agent.
Before starting, read context.json to understand:
- Current requirements
- Previous decisions
- Handover notes addressed to you
```

**Option 2: Auto-Load** (Ideal)
```yaml
# Claude Code automatically loads context when switching agents
context_file: context.json
auto_load: true
```

**Option 3: Hybrid**
- Auto-load basic state (current phase, iteration counts)
- Explicit read for detailed notes

**Current Assumption:** Commands explicitly instruct agents to read context.json

⚠️ **Needs Validation:** Confirm Claude Code's context loading capabilities

## Context in Rework Cycles

### Why Context Matters for Rework

When design is rejected, the rework command needs:

1. **What was wrong:** From review feedback
2. **What was tried:** From previous iteration
3. **Why it was tried:** From decisions
4. **What constraints exist:** From requirements
5. **How many attempts:** From iteration counts

### Rework Context Loading

```yaml
# design-l1-rework.yaml
context_sources:
  - context.json
  - review/review_l1_*.json  # All L1 reviews
  - design/l1_architecture.md  # Previous attempt
  - spec/requirements.md  # Original requirements
```

## Best Practices

### 1. Update Context Immediately
Don't wait - update context right after completing work.

### 2. Be Specific in Handover Notes
Include actionable information, not generic statements.

### 3. Track All Decisions
Even small decisions can have big impacts later.

### 4. Link Artifacts
Reference specific files, sections, requirements.

### 5. Maintain History
Don't overwrite - append to history arrays.

### 6. Use Priorities
Mark critical handover notes as `priority: "critical"`.

## Example: Complete Handover Flow

### BA → Architect

```json
{
  "from": "sdd-ba",
  "to": "sdd-architect",
  "note": "Requirements emphasize scalability (R-3.2: 10K concurrent users) and low latency (R-4.1: 100ms p95). User research shows peak traffic 9am-5pm weekdays. Consider time-based auto-scaling. Security is critical - require TLS 1.3, JWT tokens, rate limiting."
}
```

### Architect → PE

```json
{
  "from": "sdd-architect",
  "to": "sdd-pe",
  "note": "L1 design uses microservices (auth-service, user-service, api-gateway). Event-driven with Kafka for inter-service communication. PE should detail: 1) Service API contracts, 2) Event schemas, 3) Database schema per service, 4) Caching strategy. Note: Initial design failed reviews due to monolithic DB - avoid this in L2."
}
```

### PE → LE

```json
{
  "from": "sdd-pe",
  "to": "sdd-le",
  "note": "L2 components defined with clear interfaces. Auth service has 4 main components: TokenManager, SessionStore, PasswordHasher, RateLimiter. Each needs discrete implementation tasks. Focus on TokenManager first as other components depend on it. Estimated 8-10 tasks total."
}
```

### LE → Coder

```json
{
  "from": "sdd-le",
  "to": "sdd-coder",
  "note": "Created 9 implementation tasks. Start with task-001 (User model) as it's a dependency for others. Tasks 002-004 can run parallel after 001. Each task has BDD acceptance criteria - implement to satisfy those scenarios. Pay attention to task-003 (JWT generation) - reviewer flagged this as critical for security."
}
```

## Metrics and Monitoring

Context enables workflow metrics:

```json
{
  "metrics": {
    "phases_completed": 3,
    "total_iterations": 5,
    "review_pass_rate": 0.6,
    "average_iteration_count": 1.67,
    "estimated_vs_actual_time": "+15%",
    "bottleneck_phase": "l1_design"
  }
}
```

These metrics help:
- Identify bottlenecks
- Improve future workflows
- Estimate completion times
- Optimize agent prompts

## Integration with Other Systems

### Version Control

context.json should be committed:
```bash
git add context.json
git commit -m "Update context: L1 design approved after 2 iterations"
```

### CI/CD

CI can validate context:
- All required fields present
- Iteration counts within limits
- Review history consistent
- No circuit breaker violations

### Project Management

Context can feed project dashboards:
- Current phase
- Blocked tasks
- Iteration warnings
- Estimated completion

## Summary

Context management solves the agent handover problem through:

- ✅ **Central manifest** (context.json)
- ✅ **Handover notes** (agent-to-agent transfer)
- ✅ **Decision tracking** (rationale preservation)
- ✅ **Iteration tracking** (circuit breaker enforcement)
- ✅ **Review history** (audit trail)
- ✅ **State management** (current phase tracking)

**Key File:** `context.json` in each feature directory

**Related Documentation:**
- [Workflow Engine](workflow_engine.md)
- [Iterative Reviews](iterative_reviews.md)
- [Context Template Specification](../5_reference/context_schema.md)