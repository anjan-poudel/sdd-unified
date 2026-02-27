# AI-SDD Prompt Pack (Codex)

Use this as the structured prompt set for designing `ai-sdd` from `sdd-unified`.

## Output Location (Mandatory)
- Generate all files under `specs/ai-sdd-codex/`.
- Do not generate or update files under `specs/ai-sdd/`.

## Master PRD Prompt

```md
You are a principal architect. Design `ai-sdd`, a configurable SDD framework extracted from `sdd-unified`.

## Goal
Create a thin, extensible orchestration core where almost all behavior is implemented as overlays.

## Scope
### In Scope (v1)
1. Core orchestration engine with pluggable runtime adapters.
2. Externalized agent registry in YAML (no hardcoded BA/PE/LE logic).
3. YAML workflow DSL with dependencies, handovers, loops, and break conditions.
4. Overlay system (pairing, review loops, confidence routing, HIL).
5. Configurable loop guards (max iterations + explicit exit conditions).
6. Basic evidence + scoring module with confidence optional/off by default.
7. File-based human queue and resolve lifecycle.
8. Migration path from `sdd-unified` templates.

### Out of Scope (v1)
1. Full workflow SDK (code-first workflow authoring) — phase 2 only.
2. Non-file queue backends (DB/Redis/Kafka).
3. Multi-tenant authz platform.

## Principles
1. Thin core, overlays for behavior.
2. Declarative-by-default (YAML first).
3. Backward-compatible migration path.
4. Deterministic state transitions.
5. Evidence-first gates; confidence is optional routing signal, not sole approval criterion.

## Required Deliverables
1. Architecture doc with module boundaries.
2. YAML schemas:
   - `agents.schema.yaml`
   - `workflow.schema.yaml`
   - `overlay.schema.yaml`
   - `context.schema.yaml`
3. Runtime adapter interface.
4. State machine for task lifecycle + review/rework loop.
5. Default overlay configs (all optional features OFF by default except HIL ON).
6. Example end-to-end config set.
7. Test strategy (unit/integration/e2e) and acceptance checklist.
8. Migration plan from `sdd-unified`.

## Required Output Format
Return exactly these sections:
1. Executive Summary
2. Module Architecture
3. Data Contracts (YAML schemas)
4. State Machine and Loop Logic
5. Overlay Model and Precedence Rules
6. Runtime Adapter Design
7. Defaults and Tunables
8. Migration Strategy
9. Risks and Mitigations
10. Acceptance Criteria (must be testable)

## Constraints
- Keep core < 20% of total behavior; overlays implement the rest.
- Every loop must define:
  - `max_iterations`
  - explicit `exit_conditions`
  - escalation target.
- Confidence scoring must support OFF mode.
- Human queue must support `PENDING -> ACKED -> RESOLVED/REJECTED`.
```

## Agent-Specific Prompt Templates

### 1. Framework Architect Agent

```md
Design `ai-sdd` architecture from the master PRD.
Focus on bounded contexts, extension points, and overlay precedence.
Output:
- C4-style module map
- Core vs overlay responsibilities
- State ownership per module
- Failure modes and recovery paths
```

### 2. Core Engine Agent

```md
Define thin orchestration core only.
Implement:
- task scheduler (dependency DAG)
- state transitions
- adapter invocation contract
- deterministic persistence points
Do NOT implement pair/review/confidence logic in core.
Output:
- core API signatures
- state transition table
- pseudo-code for run loop
```

### 3. Workflow DSL Agent

```md
Design YAML workflow DSL.
Must support:
- tasks, dependencies
- handovers
- loops with max_iterations + exit_conditions
- escalation hooks
Output:
- schema + examples
- validation rules
- common authoring errors and lint checks
```

### 4. Agent Registry Agent

```md
Design agent/persona config model in YAML.
Must support:
- role metadata
- llm provider/model params
- prompt/constitution references
- extension/override inheritance
Output:
- schema + default agents
- override resolution rules
- conflict handling
```

### 5. Overlay System Agent

```md
Design overlays as composable policies.
Target overlays:
- pair workflow
- agentic review
- confidence routing
- HIL
Output:
- overlay schema
- precedence/merge semantics
- enable/disable/default policy matrix
```

### 6. Evaluation and Confidence Agent

```md
Design evidence and scoring.
Requirements:
- confidence optional (OFF default)
- evidence-first decision support
- simple function: confidence = f(metrics[])
Output:
- metric schema
- scoring formulas (simple and advanced)
- calibration + drift checks
```

### 7. Runtime Adapter Agent

```md
Design adapter interface for invoking runtimes (Claude/Codex/Gemini/etc).
Output:
- adapter contract
- normalized TaskResult schema
- retry/timeout policy
- strict vs compatibility mode behavior
```

### 8. QA and Validation Agent

```md
Create test strategy and MVP acceptance gates.
Include:
- unit tests by module
- integration tests (loops/queue)
- e2e fixture scenarios (T0/T1/T2)
- CI gating checklist
Output:
- test matrix
- minimal passing criteria
- artifact assertions
```


## Suggested Execution Order

1. Framework Architect Agent
2. Core Engine Agent
3. Workflow DSL Agent
4. Agent Registry Agent
5. Overlay System Agent
6. Runtime Adapter Agent
7. Evaluation and Confidence Agent
8. QA and Validation Agent
