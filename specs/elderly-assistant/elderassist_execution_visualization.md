# ElderAssist Execution Visualization

This document shows what happens after you request:

`/feature "Build a mobile app for elderly assistance (ElderAssist)"`

## 1) End-to-End Request Flow

```mermaid
sequenceDiagram
    autonumber
    participant U as User
    participant R as Runtime (Claude Code / CLI)
    participant O as Orchestrator (orchestrator/main.py)
    participant W as workflow.json
    participant A as Agents (BA/Architect/PE/LE/Coder)
    participant F as Feature Workspace

    U->>R: /feature "Build ElderAssist mobile app"
    R->>O: Start orchestration (mode=autonomous|supervised|manual)
    O->>F: Ensure feature folder exists
    O->>W: Load DAG + statuses
    loop Until done or blocked
        O->>W: Find READY tasks (dependencies completed)
        O->>A: Invoke agent command for each READY task
        A->>F: Write artifact(s) (spec/design/review/plan/code)
        O->>W: Update task status (RUNNING -> COMPLETED/FAILED)
        O->>F: Append context.json execution + handover logs
        O->>F: Evaluate review routing (auto-review/auto-approve/human queue)
    end
    O-->>R: Print completion/pause/failure summary
    R-->>U: Visible output + updated files
```

## 2) Core DAG Shape (Design + Review Loops)

```mermaid
flowchart TD
    I[init] --> RQ[define-requirements]
    RQ --> L1[design-l1]
    L1 --> RR1[route-review-l1]
    RR1 --> RL1A[review-l1-ba]
    RR1 --> RL1P[review-l1-pe]
    RR1 --> RL1L[review-l1-le]
    RL1A --> L1RW[design-l1-rework]
    RL1P --> L1RW
    RL1L --> L1RW
    RL1A --> L2[design-l2]
    RL1P --> L2
    RL1L --> L2
    L2 --> RR2[route-review-l2]
    RR2 --> RL2A[review-l2-architect]
    RR2 --> RL2L[review-l2-le]
    RL2A --> L2RW[design-l2-rework]
    RL2L --> L2RW
    RL2A --> L3[design-l3]
    RL2L --> L3
    L3 --> RR3[route-review-l3]
    RR3 --> RL3P[review-l3-pe]
    RR3 --> RL3C[review-l3-coder]
    RL3P --> L3RW[design-l3-rework]
    RL3C --> L3RW
```

## 3) What You See As Output

During execution, the orchestrator prints task-by-task logs like:

- `Task: define-requirements`
- `Agent: sdd-ba`
- `Command: sdd-ba-define-requirements --task_id=define-requirements`
- `Task ... completed successfully` (or failed/paused)

Then one of these terminal outcomes appears:

- `Workflow completed successfully`
- `Autonomous execution paused: Human review required ...`
- `No ready tasks ... Workflow may be stuck`

## 4) ElderAssist Artifacts You Can Inspect

After (or during) the run, check the feature folder for:

- `workflow.json`: source of truth for task states
- `context.json`: handovers, execution log, circuit breaker, routing info
- `spec/requirements.md`, `spec/spec.yaml`
- `design/l1_architecture.md`, `design/l2_component_design.md`
- `implementation/l3_plan.md`
- `review/*.json` (approvals/rejections/routing/human queue items)

## 5) Practical Mental Model

1. Your prompt creates feature intent.
2. `workflow.json` decides what can run next.
3. Agent commands produce artifacts and reviews.
4. Reviews can route to approve, auto-approve, human queue, or rework.
5. You see progress in logs and final state in `workflow.json` + artifacts.
