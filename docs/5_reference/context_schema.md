# Context.json Schema Reference

**Version:** 1.0.0  
**Status:** Technical Specification  
**Last Updated:** 2025-10-16

## Overview

The `context.json` file is the central state management artifact for each feature in sdd-unified. It tracks workflow state, agent handover notes, iteration counts, and circuit breaker status.

## Template Structure

```json
{
  "feature_id": "{{feature_name}}",
  "created_at": "{{timestamp}}",
  "last_updated": "{{timestamp}}",
  "current_phase": "init",
  "context_sources": {
    "requirements": {
      "file": "spec/spec.yaml",
      "schema": "sdd-unified/spec/spec.schema.json",
      "last_modified": null,
      "summary": ""
    },
    "l1_architecture": {
      "file": "design/l1_architecture.md",
      "status": "pending",
      "last_modified": null,
      "summary": ""
    },
    "l2_component_design": {
      "file": "design/l2_component_design.md",
      "status": "pending",
      "last_modified": null,
      "summary": ""
    },
    "l3_tasks": {
      "directory": "implementation/tasks/",
      "status": "pending",
      "task_count": 0,
      "last_modified": null
    },
    "reviews": {
      "log_file": "review/review.log",
      "outcome_files": [],
      "latest_feedback": ""
    },
    "workflow_state": {
      "file": "workflow.json",
      "completed_tasks": [],
      "current_tasks": [],
      "blocked_tasks": []
    },
    "source_code": {
      "directory": "src/",
      "file_count": 0,
      "last_modified": null
    }
  },
  "handover_notes": {
    "history": []
  },
  "iteration_tracking": {
    "design-l1": {
      "attempts": 0,
      "max_attempts": 3,
      "status": "active",
      "reviews": []
    },
    "design-l2": {
      "attempts": 0,
      "max_attempts": 3,
      "status": "active",
      "reviews": []
    },
    "design-l3": {
      "attempts": 0,
      "max_attempts": 4,
      "status": "active",
      "reviews": []
    }
  },
  "circuit_breaker": {
    "max_review_iterations": 3,
    "max_task_rework_iterations": 2,
    "intervention_required": false,
    "blocked_task": null,
    "reason": null
  }
}
```

## Field Definitions

### Top Level

| Field | Type | Description |
|-------|------|-------------|
| `feature_id` | string | Unique identifier for the feature |
| `created_at` | ISO-8601 | When context was created |
| `last_updated` | ISO-8601 | Last modification timestamp |
| `current_phase` | string | Current workflow phase (init, requirements, l1_design, etc.) |

### Context Sources

Tracks all artifacts and their status.

**Requirements:**
- `file`: Path to spec.yaml
- `schema`: Path to spec schema
- `last_modified`: Last modification time
- `summary`: Brief summary of requirements

**Design Artifacts (L1, L2, L3):**
- `file` or `directory`: Location of artifact
- `status`: pending | in_progress | completed
- `last_modified`: Last update time
- `summary`: Brief description

### Handover Notes

Array of agent-to-agent communication records.

**Format:**
```json
{
  "timestamp": "ISO-8601",
  "from_agent": "sdd-ba",
  "to_agent": "sdd-architect",
  "task_completed": "define-requirements",
  "message": "Concise handover message",
  "critical_points": [
    "Key point 1",
    "Key point 2"
  ],
  "artifacts_created": [
    "spec/spec.yaml"
  ]
}
```

### Iteration Tracking

Tracks rework iterations for circuit breaker enforcement.

**Per-Phase Format:**
```json
{
  "attempts": 2,
  "max_attempts": 3,
  "status": "active" | "limit_reached" | "approved",
  "reviews": [
    {
      "attempt": 1,
      "outcome": "REJECTED_WITH_FEEDBACK",
      "rejecting_agents": ["sdd-pe"],
      "timestamp": "ISO-8601",
      "issues_count": 3
    }
  ]
}
```

### Circuit Breaker

Controls iteration limits and human intervention.

| Field | Type | Description |
|-------|------|-------------|
| `max_review_iterations` | number | Max rework attempts for design (default: 3) |
| `max_task_rework_iterations` | number | Max rework for tasks (default: 2) |
| `intervention_required` | boolean | True when limits exceeded |
| `blocked_task` | string | Task ID that triggered circuit breaker |
| `reason` | string | Why circuit breaker triggered |

## Usage

### Initialization

Created when feature workflow starts:

```bash
# Template location
.sdd_unified/templates/context.json.template

# Instantiated at
features/feature-XXX-name/context.json
```

### Updates

Every agent updates context after completing their task:

```yaml
# In command definition
outputs:
  - design/l1_architecture.md
  - context.json  # Updated with handover notes
```

### Reading

Agents read context to understand previous work:

```yaml
# In command prompt
context_sources:
  - context.json
  - design/l1_architecture.md
```

## Examples

### Complete Context Example

See: [`context_management.md`](../2_architecture/context_management.md#complete-context-schema)

### Handover Note Example

```json
{
  "timestamp": "2025-10-16T08:00:00Z",
  "from_agent": "sdd-architect",
  "to_agent": "sdd-pe",
  "task_completed": "design-l1",
  "message": "L1 architecture complete after 2 iterations. Microservices pattern chosen for scalability requirement R-3.2. PE should focus on inter-service contracts and event schemas.",
  "critical_points": [
    "Initial design failed due to monolithic DB - avoided in final version",
    "Event-driven communication required for loose coupling",
    "Performance budget: 100ms p95 latency"
  ],
  "artifacts_created": [
    "design/l1_architecture.md"
  ]
}
```

### Iteration Tracking Example

```json
{
  "design-l1": {
    "attempts": 2,
    "max_attempts": 3,
    "status": "approved",
    "reviews": [
      {
        "attempt": 1,
        "outcome": "REJECTED_WITH_FEEDBACK",
        "rejecting_agents": ["sdd-ba"],
        "timestamp": "2025-10-16T08:20:00Z",
        "issues_count": 2
      },
      {
        "attempt": 2,
        "outcome": "APPROVED",
        "rejecting_agents": [],
        "timestamp": "2025-10-16T08:55:00Z",
        "issues_count": 0
      }
    ]
  }
}
```

## Related Documentation

- [Context Management Architecture](../2_architecture/context_management.md)
- [Iterative Reviews](../2_architecture/iterative_reviews.md)
- [Workflow Engine](../2_architecture/workflow_engine.md)

---

**Document Version:** 1.0.0  
**Last Updated:** 2025-10-16  
**Maintained By:** sdd-unified Technical Team