# ai-sdd: Implementation Plan

**Version:** 0.1.0-draft
**Date:** 2026-02-23
**Status:** Draft

---

## 1. Overview

`ai-sdd` is delivered in three phases:

| Phase | Name | Goal |
|---|---|---|
| **Phase 1** | Core Engine | Functional pipeline: YAML agents + YAML workflow + constitutions + basic HIL |
| **Phase 2** | Overlays | Confidence loop, paired workflow, agentic review, policy gate |
| **Phase 3** | Workflow SDK | Programmatic workflow definitions; workflow-as-code |

---

## 2. Architecture

### 2.1 Component Overview

```
ai-sdd/
├── core/                      # Engine: orchestrator, workflow runner, state manager
│   ├── engine.py              # Main workflow loop
│   ├── workflow_loader.py     # YAML workflow parser + DAG builder
│   ├── agent_loader.py        # YAML agent definition loader
│   ├── state_manager.py       # Task state persistence (JSON)
│   ├── context_manager.py     # Context assembly (constitutions + handover state)
│   └── hooks.py               # Pre/post-task, on-failure, on-loop-exit hooks
│
├── constitution/              # Constitution resolver
│   ├── resolver.py            # Recursive merge of project + subfolder constitutions
│   └── schema.yaml            # Constitution file schema
│
├── agents/                    # Agent system
│   ├── base_agent.yaml        # Base agent schema/defaults
│   ├── defaults/              # Default agents (BA, PE, DEV, Architect, LE, Reviewer)
│   │   ├── ba.yaml
│   │   ├── architect.yaml
│   │   ├── pe.yaml
│   │   ├── le.yaml
│   │   ├── dev.yaml
│   │   └── reviewer.yaml
│   └── loader.py              # Agent YAML loader + overlay merger
│
├── workflows/                 # Workflow templates
│   ├── default-sdd.yaml       # Standard SDD pipeline (mirrors sdd-unified)
│   └── schema.yaml            # Workflow YAML schema
│
├── overlays/                  # Optional overlay modules
│   ├── confidence/            # Confidence scoring loop
│   ├── paired/                # Paired workflow loop
│   ├── review/                # Agentic review loop
│   └── hil/                   # Human-in-the-loop
│
├── eval/                      # Evaluation metrics
│   ├── metrics.py             # EvalMetric types
│   └── scorer.py              # confidence = f([EvalMetric]) → decimal
│
├── config/                    # Project-level configuration
│   └── ai-sdd.yaml            # Master config file (LLMs, overlays, thresholds)
│
└── cli/                       # CLI entrypoint
    └── main.py
```

### 2.2 Configuration Hierarchy

```
project-root/
├── .ai-sdd/
│   ├── ai-sdd.yaml            # Project config (overrides defaults)
│   ├── constitution.md        # Root constitution (project-level steers)
│   ├── agents/                # Project-specific agent overrides/additions
│   └── workflows/             # Project-specific workflows
│
└── src/
    └── some-module/
        └── .ai-sdd/
            └── constitution.md   # Module-level constitution (overrides root)
```

### 2.3 Workflow YAML Schema (Draft)

```yaml
# .ai-sdd/workflows/my-workflow.yaml
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

  review-l1:
    agent: reviewer
    inputs: ["design/l1.md"]
    outputs: ["review/l1.log"]
    dependencies: ["design-l1"]
    loop:
      max_iterations: 3
      exit_conditions:
        - "review.decision == GO"

  design-l2:
    agent: pe
    inputs: ["design/l1.md", "review/l1.log"]
    outputs: ["design/l2.md"]
    dependencies: ["review-l1"]
```

### 2.4 Agent YAML Schema (Draft)

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

### 2.5 Constitution Schema (Draft)

```markdown
# constitution.md (project root)
## Purpose
[Why this project exists and what it's trying to achieve]

## Background
[Domain context, key constraints, technology choices and rationale]

## Rules
- [Hard rule 1]
- [Hard rule 2]

## Standards
- Code style: [...]
- Testing: [...]
- Naming: [...]
```

Resolution order (highest priority last wins):
1. Framework defaults
2. Project root `constitution.md`
3. Sub-module `constitution.md` (closest to the task)

### 2.6 Overlay Architecture

Each overlay is a self-contained module that wraps task execution. Overlays are stacked as decorators around the core task dispatch:

```
Core Engine dispatch(task)
    └── HIL overlay (always loaded if enabled)
        └── Agentic Review overlay (if enabled for task)
            └── Paired Workflow overlay (if enabled for task)
                └── Confidence Loop overlay (if enabled for task)
                    └── Agent execution
```

Each overlay is activated by a flag in the workflow task definition or the project config:

```yaml
tasks:
  design-l1:
    agent: architect
    overlays:
      paired_workflow:
        enabled: true
        challenger_agent: pe
        max_iterations: 3
        exit_conditions:
          - "pair.approved == true"
          - "confidence_score >= 0.85"
      confidence_loop:
        enabled: true
        threshold: 0.80
```

---

## 3. Phase 1: Core Engine

**Goal:** A fully functional pipeline using default agents and YAML workflow.

### Deliverables

| ID | Deliverable | Description |
|---|---|---|
| P1-D1 | Agent YAML schema + loader | Parse agent YAML, support `extends` for inheritance |
| P1-D2 | Default agents | BA, Architect, PE, LE, DEV, Reviewer YAML definitions |
| P1-D3 | Workflow YAML schema + loader | Parse workflow YAML, build DAG, validate |
| P1-D4 | Core engine | Resolve deps, dispatch tasks, collect outputs |
| P1-D5 | State manager | Persist task state (PENDING→RUNNING→COMPLETED/FAILED) |
| P1-D6 | Context manager | Assemble context: constitution + handover state + task inputs |
| P1-D7 | Constitution resolver | Recursive merge of root + subfolder constitutions |
| P1-D8 | HIL overlay (basic) | Mark tasks as requiring human approval; pause and wait |
| P1-D9 | Default SDD workflow template | `default-sdd.yaml` mirroring current sdd-unified pipeline |
| P1-D10 | CLI | `ai-sdd run --workflow <path> --project <path>` |

### Acceptance Criteria

- Given a project with a valid `ai-sdd.yaml` and `default-sdd.yaml`, when `ai-sdd run` is executed, then tasks execute in dependency order.
- Given a custom agent YAML extending a default agent, when the workflow loads, then the custom agent's attributes override the base.
- Given a sub-module with its own `constitution.md`, when a task in that module runs, then the merged constitution is injected into the agent context.
- Given a task marked `requires_human: true`, when the task is ready, then execution pauses until human input is provided.

---

## 4. Phase 2: Overlays

**Goal:** All four overlay types are independently configurable and composable.

### Deliverables

| ID | Deliverable | Description |
|---|---|---|
| P2-D1 | Confidence scoring engine | `EvalMetric` types + `confidence = f([EvalMetric]) → decimal` |
| P2-D2 | Confidence loop overlay | Auto-transition when score ≥ threshold |
| P2-D3 | Paired workflow overlay | Driver/challenger loop with role switch support |
| P2-D4 | Agentic review overlay | Reviewer critiques coder output; loop until quality gate passes |
| P2-D5 | Enhanced HIL overlay | Deadlock detection, loop escape escalation to human |
| P2-D6 | Overlay config schema | Unified schema for enabling/configuring all overlays |
| P2-D7 | Overlay interaction tests | Validate behaviour when multiple overlays are active together |

### Acceptance Criteria

- Given `confidence_loop.enabled=true` and threshold=0.80, when confidence score >= 0.80, then the engine auto-advances to the next task without human input.
- Given `paired_workflow.enabled=true`, when the driver completes a round, then the challenger critique runs before the next driver iteration.
- Given `agentic_review.enabled=true`, when the reviewer outputs NO_GO, then the coder receives the feedback and reruns the task.
- Given a loop that has reached MAX_ITERATION without an exit condition being met, when the HIL overlay is active, then the engine pauses and presents the situation to a human operator.
- Given multiple overlays enabled on one task, when the task runs, then overlay behaviour composes correctly without conflicts.

---

## 5. Phase 3: Workflow SDK

**Goal:** Programmatic workflow definitions as an alternative to YAML.

### Deliverables

| ID | Deliverable | Description |
|---|---|---|
| P3-D1 | Python Workflow SDK | Fluent API for defining workflows in Python |
| P3-D2 | SDK → YAML export | Serialize SDK-defined workflows to YAML for engine execution |
| P3-D3 | SDK documentation | Usage guide and examples |

### Acceptance Criteria (Sketch)

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

## 6. Migration from sdd-unified

The following sdd-unified components map to ai-sdd equivalents:

| sdd-unified | ai-sdd |
|---|---|
| `agents/roles/*.yaml` | `agents/defaults/*.yaml` (same schema, enhanced) |
| `commands/**/*.yaml` (agent commands) | Referenced in agent YAML `commands` section |
| `templates/workflow.json.template` | `workflows/default-sdd.yaml` (YAML, not JSON) |
| `orchestrator/main.py` | `core/engine.py` |
| `docs/2_architecture/pair_review_overlay.md` | `overlays/paired/` module |
| `docs/2_architecture/confidence_routing_overlay.md` | `overlays/confidence/` module |
| `orchestrator/policy_gate.py` | `overlays/review/` module |
| `orchestrator/human_queue.py` | `overlays/hil/` module |
| Hardcoded role names (sdd-ba, etc.) | Configurable via agent YAML `name` field |

---

## 7. Risks and Mitigations

| Risk | Mitigation |
|---|---|
| Overlay composition creates unexpected interactions | Phase 2 includes dedicated overlay interaction tests |
| YAML workflow schema too verbose for complex DAGs | Phase 3 SDK provides programmatic alternative |
| Constitution merge order ambiguity | Explicit documented precedence rules; validation on load |
| HIL integration varies by runtime (Claude Code vs. Codex) | HIL overlay is runtime-agnostic; adapters per runtime |
| LLM hyperparameter drift between agent versions | Schema validation enforces required fields; defaults provided |
