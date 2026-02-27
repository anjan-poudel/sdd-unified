# ai-sdd: Synthesized Implementation Plan

**Version:** 0.1.0-synthesized
**Date:** 2026-02-27
**Synthesized from:** ai-sdd-claude, ai-sdd-codex, ai-sdd-gemini

---

## 1. Overview

`ai-sdd` is delivered in four phases:

| Phase | Name | Goal |
|---|---|---|
| **Phase 1** | Core Engine | Functional pipeline: YAML agents + YAML workflow + constitutions + basic HIL |
| **Phase 2** | Overlay Suite | Evidence gate, confidence loop, paired workflow, agentic review; composable overlays |
| **Phase 3** | Workflow SDK | Programmatic workflow definitions (Python + TypeScript); workflow-as-code |
| **Phase 4** | Production Hardening | Reliability, security, observability, governance for enterprise adoption |

---

## 2. Architecture

### 2.1 Component Overview

```
ai-sdd/
├── core/                      # Engine: orchestrator, workflow runner, state manager
│   ├── engine.py              # Main workflow loop (asyncio for parallel tasks)
│   ├── workflow_loader.py     # YAML workflow parser + DAG builder + cycle detection
│   ├── agent_loader.py        # YAML agent definition loader + extends resolution
│   ├── state_manager.py       # Task state persistence (JSON) + resume logic
│   ├── context_manager.py     # Context assembly (constitutions + handover state)
│   ├── hooks.py               # Pre/post-task, on-failure, on-loop-exit hooks
│   └── runtime_adapter.py     # RuntimeAdapter interface (ABC)
│
├── adapters/                  # Runtime adapter implementations
│   ├── mock_adapter.py        # Deterministic mock (for tests)
│   ├── claude_code_adapter.py # Claude Code integration
│   └── codex_adapter.py       # Codex/OpenAI integration (Phase 1 scaffold)
│
├── constitution/              # Constitution resolver
│   ├── resolver.py            # Recursive merge: framework → root → sub-module
│   └── schema.yaml            # Constitution file schema
│
├── agents/                    # Agent system
│   ├── base_agent.yaml        # Base agent schema/defaults
│   ├── schema.yaml            # Agent YAML schema (for validation)
│   ├── defaults/              # Default agents (BA, PE, DEV, Architect, LE, Reviewer)
│   │   ├── ba.yaml
│   │   ├── architect.yaml
│   │   ├── pe.yaml
│   │   ├── le.yaml
│   │   ├── dev.yaml
│   │   └── reviewer.yaml
│   └── loader.py              # Agent YAML loader + extends merger
│
├── workflows/                 # Workflow templates
│   ├── default-sdd.yaml       # Standard SDD pipeline (mirrors sdd-unified)
│   └── schema.yaml            # Workflow YAML schema
│
├── overlays/                  # Optional overlay modules (decorator chain)
│   ├── base_overlay.py        # Abstract overlay interface
│   ├── hil/                   # Human-in-the-loop (default ON)
│   │   ├── hil_overlay.py
│   │   └── queue.py           # File-based HIL queue
│   ├── policy_gate/           # Evidence policy gate
│   │   └── gate_overlay.py
│   ├── confidence/            # Confidence scoring loop
│   │   └── confidence_overlay.py
│   ├── paired/                # Paired workflow loop
│   │   ├── paired_overlay.py
│   │   └── pair_session.py
│   └── review/                # Agentic review loop
│       └── review_overlay.py
│
├── eval/                      # Evaluation metrics
│   ├── metrics.py             # EvalMetric types (coverage, lint, checklist, llm-judge)
│   └── scorer.py              # confidence = f([EvalMetric]) → decimal
│
├── config/                    # Framework-level defaults
│   └── defaults.yaml          # Framework default config values
│
├── cli/                       # CLI entrypoint
│   ├── main.py
│   └── commands.py            # run, resume, status, validate-config, hil
│
└── observability/             # Structured event emission
    └── emitter.py             # Emit workflow events to log/stdout
```

### 2.2 Configuration Hierarchy

```
project-root/
├── .ai-sdd/
│   ├── ai-sdd.yaml            # Project config (overrides framework defaults)
│   ├── constitution.md        # Root constitution (project-level steers)
│   ├── agents/                # Project-specific agent overrides/additions
│   ├── workflows/             # Project-specific workflows
│   └── state/
│       ├── workflow-state.json   # Live task state
│       └── hil/               # HIL queue directory
│
└── src/
    └── some-module/
        └── .ai-sdd/
            └── constitution.md   # Module-level constitution (overrides root)
```

Config merge precedence (highest wins):
1. CLI flags
2. Project `.ai-sdd/ai-sdd.yaml`
3. Framework `config/defaults.yaml`

Constitution resolution (highest wins):
1. Framework defaults
2. Project root `constitution.md`
3. Sub-module `constitution.md` (closest to the task)

### 2.3 Workflow YAML Schema

```yaml
# .ai-sdd/workflows/default-sdd.yaml
version: "1"
name: "standard-sdd"

config:
  max_iterations_default: 5

tasks:
  define-requirements:
    agent: ba
    inputs: ["spec.md"]
    outputs: ["requirements.md"]
    dependencies: []

  design-l1:
    agent: architect
    inputs: ["requirements.md"]
    outputs: ["design/l1.md"]
    dependencies: ["define-requirements"]
    overlays:
      paired_workflow:
        enabled: true
        driver_agent: architect
        challenger_agent: pe
        role_switch: session        # options: session | subtask | checkpoint
        max_iterations: 3
        exit_conditions:
          - "pair.challenger_approved == true"
          - "confidence_score >= 0.85"
      confidence_loop:
        enabled: true
        threshold: 0.80
      policy_gate:
        enabled: true
        risk_tier: T1

  review-l1:
    agent: reviewer
    inputs: ["design/l1.md"]
    outputs: ["review/l1.log"]
    dependencies: ["design-l1"]
    overlays:
      agentic_review:
        enabled: true
        max_iterations: 3
        exit_conditions:
          - "review.decision == GO"
```

### 2.4 Agent YAML Schema

```yaml
# agents/defaults/ba.yaml
name: ba
display_name: "Business Analyst"
version: "1"

extends: null  # base agent; custom agents can set extends: ba

llm:
  provider: anthropic
  model: claude-sonnet-4-6
  hyperparameters:
    temperature: 0.3
    max_tokens: 8000

role:
  description: |
    Translates business needs into formal requirements. Responsible for
    capturing, clarifying, and structuring functional and non-functional requirements.
  expertise:
    - requirements elicitation
    - user story writing
    - acceptance criteria (Gherkin)
    - stakeholder communication
  responsibilities:
    - produce requirements.md from spec input
    - validate requirements coverage
    - clarify ambiguities with upstream input or HIL

commands:
  define-requirements: "commands/ba/define-requirements.md"
```

### 2.5 Overlay Execution Chain

Overlays are stacked as decorators around the core task dispatch:

```
Core Engine dispatch(task)
    └── HIL overlay              (always active if enabled — default ON)
        └── Evidence Policy Gate (if enabled for task)
            └── Agentic Review   (if enabled for task)
                └── Paired Workflow (if enabled for task)
                    └── Confidence Loop (if enabled for task)
                        └── Agent execution
```

Overlays register themselves via hooks — the engine does not know about specific overlay logic.

### 2.6 State File Schema

```json
{
  "version": "1",
  "workflow": "default-sdd",
  "project": "/path/to/project",
  "started_at": "2026-02-27T10:00:00Z",
  "tasks": {
    "define-requirements": {
      "status": "COMPLETED",
      "started_at": "...",
      "completed_at": "...",
      "outputs": ["requirements.md"],
      "iterations": 1
    },
    "design-l1": {
      "status": "PENDING",
      "started_at": null,
      "completed_at": null,
      "outputs": [],
      "iterations": 0
    }
  }
}
```

### 2.7 RuntimeAdapter Interface

```python
class RuntimeAdapter(ABC):
    @abstractmethod
    def dispatch(self, task: Task, context: AgentContext) -> TaskResult:
        ...
```

Implementations in Phase 1: `MockRuntimeAdapter`, `ClaudeCodeAdapter`.
Planned for Phase 2: `CodexAdapter`, `GeminiAdapter`.

---

## 3. Phase 1: Core Engine

**Goal:** Fully functional pipeline using default agents and YAML workflow.

| ID | Deliverable | Description |
|---|---|---|
| P1-D1 | Agent YAML schema + loader | Parse agent YAML, support `extends` for inheritance, schema validate on load |
| P1-D2 | Default agents | BA, Architect, PE, LE, DEV, Reviewer YAML definitions |
| P1-D3 | Workflow YAML schema + loader | Parse workflow YAML, build DAG, cycle detection, validate |
| P1-D4 | Core engine | Resolve deps, dispatch tasks via adapter, collect outputs, asyncio parallel |
| P1-D5 | State manager | Persist task state (PENDING→RUNNING→COMPLETED/FAILED), resume support |
| P1-D6 | Context manager | Assemble context: constitution + handover state + task inputs |
| P1-D7 | Constitution resolver | Recursive merge: root → sub-module; deterministic override |
| P1-D8 | HIL overlay | Default-ON; pause on required-human tasks; file-based queue; deadlock escalation |
| P1-D9 | Default SDD workflow template | `default-sdd.yaml` mirroring current sdd-unified pipeline |
| P1-D10 | CLI | `ai-sdd run|resume|status|validate-config|hil` |
| P1-D11 | RuntimeAdapter + MockAdapter | Interface + mock for tests; ClaudeCodeAdapter |
| P1-D12 | Observability emitter | Structured event log for all workflow transitions |

### Phase 1 Acceptance Criteria

- Given a project with a valid `ai-sdd.yaml` and `default-sdd.yaml`, when `ai-sdd run` is executed, then tasks execute in dependency order.
- Given a custom agent YAML extending a default agent, when the workflow loads, then the custom agent's attributes override the base.
- Given a sub-module with its own `constitution.md`, when a task in that module runs, then the merged constitution is injected into the agent context.
- Given a task marked `requires_human: true`, when the task is ready, then execution pauses until human input is provided.
- Given an interrupted workflow, when `ai-sdd run --resume` is executed, then the engine continues from last persisted state.
- Given a cyclic workflow DAG, when the engine loads it, then a validation error is raised immediately.

---

## 4. Phase 2: Overlay Suite

**Goal:** All five overlay types independently configurable and composable.

| ID | Deliverable | Description |
|---|---|---|
| P2-D1 | Confidence scoring engine | `EvalMetric` types + `confidence = f([EvalMetric]) → decimal`; raw mode |
| P2-D2 | Confidence loop overlay | Advisory routing signal; auto-advance advisory when score ≥ threshold |
| P2-D3 | Evidence policy gate | T0/T1/T2 risk tiers; acceptance + verification + readiness evidence |
| P2-D4 | Paired workflow overlay | Driver/challenger loop with role switch; pair session history |
| P2-D5 | Agentic review overlay | Coder/reviewer loop; GO/NO_GO with rework feedback; auditable log |
| P2-D6 | Enhanced HIL | Deadlock detection, loop escape escalation; ACKED/RESOLVED/REJECTED states |
| P2-D7 | Overlay composition tests | Validate behaviour when multiple overlays are active together |

### Phase 2 Acceptance Criteria

- Given `confidence_loop.enabled=true` and threshold=0.80, when confidence score ≥ 0.80, then the engine emits an advisory signal (does not bypass evidence gate).
- Given `policy_gate.risk_tier=T2`, when the gate is checked, then HIL sign-off is mandatory regardless of confidence.
- Given `paired_workflow.enabled=true`, when the driver completes a round, then the challenger critique runs before the next driver iteration.
- Given `agentic_review.enabled=true`, when the reviewer outputs NO_GO, then the coder receives the rework feedback and reruns the task.
- Given a loop that has reached MAX_ITERATION without an exit condition being met, when HIL is active, then the engine pauses and presents the situation to the operator.
- Given multiple overlays enabled on one task, when the task runs, then overlay behaviour composes correctly without conflicts.

---

## 5. Phase 3: Workflow SDK

**Goal:** Programmatic workflow definitions as an alternative to YAML.

| ID | Deliverable | Description |
|---|---|---|
| P3-D1 | Python Workflow SDK | Fluent API for defining workflows in Python |
| P3-D2 | TypeScript Workflow SDK | Same API surface for TypeScript/Node consumers |
| P3-D3 | SDK → YAML export | Serialize SDK-defined workflows to YAML for engine execution |
| P3-D4 | Reference example projects | Simple linear SDD; High-assurance Paired Workflow SDD |
| P3-D5 | Dry-run mode | Validate workflow structure and config without executing tasks |
| P3-D6 | Cost/latency documentation | Explicit cost and latency tradeoff guide per overlay combination |

```python
from ai_sdd import Workflow, Task, Agent

wf = Workflow("my-pipeline")
ba = Agent.load("ba")
arch = Agent.load("architect")

req_task = wf.task("define-requirements", agent=ba)
l1_task = wf.task("design-l1", agent=arch).depends_on(req_task)
wf.run()
```

---

## 6. Phase 4: Production Hardening

**Goal:** Enterprise-grade reliability, security, observability, and governance.

| Track | Deliverables |
|---|---|
| **Reliability** | Retries with backoff; idempotent task execution; load tests |
| **Security** | Secret sanitization in state/logs; supply-chain scan; no secrets in YAML |
| **Observability** | Structured logs; distributed traces; metrics (task durations, retry counts); SLO alerts |
| **Runtime Integration** | Timeout/quota management; LLM provider fallback behaviour |
| **Governance** | Audit export (all promotion decisions with evidence); policy packs for T0/T1/T2 |

---

## 7. Migration from sdd-unified

| sdd-unified | ai-sdd |
|---|---|
| `agents/roles/*.yaml` | `agents/defaults/*.yaml` (same schema, enhanced) |
| `commands/**/*.yaml` | Referenced in agent YAML `commands` section |
| `templates/workflow.json.template` | `workflows/default-sdd.yaml` (YAML, not JSON) |
| `orchestrator/main.py` | `core/engine.py` |
| `docs/.../pair_review_overlay.md` | `overlays/paired/` module |
| `docs/.../confidence_routing_overlay.md` | `overlays/confidence/` module |
| `orchestrator/policy_gate.py` | `overlays/policy_gate/` module |
| `orchestrator/human_queue.py` | `overlays/hil/` module |
| Hardcoded role names (sdd-ba, etc.) | Configurable via agent YAML `name` field |

---

## 8. Risks and Mitigations

| Risk | Mitigation |
|---|---|
| Overlay composition creates unexpected interactions | Phase 2 includes dedicated overlay interaction tests |
| YAML workflow schema too verbose for complex DAGs | Phase 3 SDK provides programmatic alternative |
| Constitution merge order ambiguity | Explicit documented precedence rules; validation on load |
| HIL integration varies by runtime | HIL overlay is runtime-agnostic; adapters per runtime |
| LLM hyperparameter drift between agent versions | Schema validation enforces required fields; defaults provided |
| Evidence gate bypassed by raising threshold | T2 tier requires HIL by design — no config bypass |
| Secrets leaked to state files | Observability emitter strips secrets before writing |
| Workflow schema breaking change mid-run | State file includes schema version; migration guide required |
