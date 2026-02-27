# ai-sdd Implementation Plan

## 1. Architecture

### 1.1 Core Modules
- `core/engine.py`: orchestration loop
- `core/workflow_loader.py`: DAG validation and load
- `core/agent_loader.py`: agent registry + inheritance
- `core/state_manager.py`: persist/resume
- `core/context_manager.py`: constitution + handover context
- `core/hooks.py`: lifecycle hooks
- `constitution/resolver.py`: recursive constitution merge
- `eval/scorer.py`: metrics and confidence utility
- `overlays/*`: confidence, paired, review, hil, policy_gate
- `runtime/adapters/*`: backend adapters
- `cli/main.py`: run/resume/validate/hil

### 1.2 Execution Model
1. Load config + schemas.
2. Resolve workflow DAG.
3. Resolve constitutions by task path.
4. Dispatch through overlay chain.
5. Persist state transitions.
6. Resume from persisted state when requested.

### 1.3 Overlay Order
1. HIL
2. Evidence policy gate
3. Agentic review (if enabled)
4. Paired workflow (if enabled)
5. Confidence (if enabled)
6. Agent execution

## 2. Phased Delivery

### Phase 1: Core Runtime
- T001 Agent system
- T002 Workflow system
- T003 Constitution system
- T004 Core engine
- T005 HIL overlay
- T009 CLI/config/adapters

### Phase 2: Overlay Suite
- T006 Confidence overlay
- T007 Paired workflow overlay
- T008 Agentic review overlay
- Policy gate integration across T006-T008

### Phase 3: Workflow SDK
- Programmatic workflow authoring and YAML export

## 3. Acceptance Rules
- All loops define `max_iterations` and explicit exits.
- Confidence is optional/off by default.
- Confidence never promotes by itself.
- Evidence gate checks:
  - acceptance evidence
  - verification (tests/lint/security)
  - operational readiness
  - optional/tunable requirement coverage
- T2 routes require human sign-off.

## 4. Migration Notes
- Preserve default SDD role set.
- Support config-only migration from existing templates.
- Keep adapter contract stable for multi-provider support.
