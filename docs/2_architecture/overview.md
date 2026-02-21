# Architecture Overview

## Purpose

Explain what `sdd-unified` is, what it is not, and how responsibilities are split.

## Core Model

`sdd-unified` is a **configuration/steering layer**. It is not the execution runtime.

- Runtime (Claude Code/Roo Code): executes prompts, files, and workflow steps
- `sdd-unified`: defines workflow shape, role prompts, gates, and schemas

```text
User request
  -> /feature
  -> Runtime executes tasks
  -> Runtime reads .sdd_unified/{templates,commands,agents,orchestrator,spec}
```

## Primary Components

1. Workflow DAG: `templates/workflow.json.template`
2. Agent configs: `agents/configs/*.yaml`
3. Command templates: `commands/**/*.yaml`
4. State artifacts: `workflow.json`, `context.json`, `review/*.json`

## Operating Modes

1. Manual: run each phase directly
2. Supervised: runtime pauses at checkpoints
3. Autonomous: runtime executes end-to-end (after validation)

## Output Contract

Each feature should produce:

- `spec/requirements.md` and/or `spec/spec.yaml`
- `design/l1_architecture.md`
- `design/l2_component_design.md`
- `implementation/tasks/*.md`
- `review/*.json`

## Related

- `workflow_engine.md`
- `context_management.md`
- `iterative_reviews.md`
- `pair_review_overlay.md`
- `confidence_routing_overlay.md`

Full historical version: `../archive/non_core/2_architecture/overview-full.md`
