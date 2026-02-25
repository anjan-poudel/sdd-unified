# ai-sdd PRD

## 1. Problem
Current SDD implementations are effective but rigid. Teams need a configurable framework where agents, workflows, and governance logic are externalized and tunable.

## 2. Vision
`ai-sdd` is a flexible, overlay-first framework for agentic software engineering. The core orchestrates; overlays provide behavior.

## 3. Users
| Persona | Need |
|---|---|
| Solo engineer | Fast default workflow with low setup |
| Product/dev team | Tunable review loops and handovers |
| Enterprise | Evidence-based gates, risk-tier routing, HIL |

## 4. Functional Requirements

### 4.1 Agent System
| ID | Requirement |
|---|---|
| AGT-001 | Agent roles are defined in YAML, not hardcoded. |
| AGT-002 | Default agents include BA, Architect, PE, DEV, LE, Reviewer. |
| AGT-003 | Custom agents can replace or extend defaults. |
| AGT-004 | Agent inheritance/overlay supports targeted overrides. |
| AGT-005 | Each agent can set provider/model independently. |
| AGT-006 | Each agent supports hyperparameter tuning. |

### 4.2 Workflow System
| ID | Requirement |
|---|---|
| WF-001 | Workflows are YAML DAGs. |
| WF-002 | Tasks define dependencies, inputs/outputs, handovers, loops. |
| WF-003 | Engine executes in topological order. |
| WF-004 | Independent tasks are eligible for parallel execution. |
| WF-005 | Default SDD workflow template is shipped. |
| WF-006 | Loops require max-iteration and explicit exit conditions. |

### 4.3 Constitution System
| ID | Requirement |
|---|---|
| CON-001 | Constitutions define purpose/background/rules/standards. |
| CON-002 | Constitutions are hierarchical (root + submodule overrides). |
| CON-003 | Resolved constitution is injected into task context. |
| CON-004 | Resolution is deterministic and recursive. |

### 4.4 Core Engine
| ID | Requirement |
|---|---|
| ENG-001 | Thin orchestrator loads workflow, resolves deps, dispatches tasks. |
| ENG-002 | Task state is persisted and resumable. |
| ENG-003 | Hooks: pre-task, post-task, on-failure, on-loop-exit. |
| ENG-004 | Runtime adapters support Codex/Claude/Gemini-style backends. |
| ENG-005 | Planning/task-breakdown policy is constitution-driven, not hardcoded. |

### 4.5 Evaluation & Confidence
| ID | Requirement |
|---|---|
| EVL-001 | Eval metrics can produce confidence (`confidence=f(metrics[])`). |
| EVL-002 | Raw metric mode is supported as simpler alternative. |
| EVL-003 | Confidence overlay is OFF by default. |
| EVL-004 | Confidence cannot be a standalone promotion gate. |

## 5. Overlay Requirements
All overlays are optional except HIL default-on.

### 5.1 Confidence Overlay
| ID | Requirement |
|---|---|
| CL-001 | Confidence provides advisory routing signal only. |
| CL-002 | Threshold is configurable per workflow/task. |
| CL-003 | Loop exits require explicit conditions beyond threshold. |

### 5.2 Paired Workflow Overlay
| ID | Requirement |
|---|---|
| PW-001 | Supports driver/challenger pairing. |
| PW-002 | Role-switch policy is configurable. |
| PW-003 | Exit can use reviewer approval and evidence gate; confidence optional. |
| PW-004 | Max-iteration required. |

### 5.3 Agentic Review Overlay
| ID | Requirement |
|---|---|
| AR-001 | Coder/reviewer roles do not switch. |
| AR-002 | Reviewer evaluates against configurable quality guidelines. |
| AR-003 | Loop uses GO/NO_GO with required rework feedback. |
| AR-004 | Max-iteration and escalation path required. |

### 5.4 Human-in-the-Loop Overlay
| ID | Requirement |
|---|---|
| HIL-001 | HIL is ON by default. |
| HIL-002 | Tasks can require explicit human approval. |
| HIL-003 | Deadlock/loop exhaustion escalates to HIL. |
| HIL-004 | Default queue backend is file-based. |

### 5.5 Evidence Policy Gate
| ID | Requirement |
|---|---|
| PG-001 | Confidence percentage must not be standalone gate criterion. |
| PG-002 | Gate uses acceptance evidence, verification results, operational readiness. |
| PG-003 | Requirement coverage is optional and tunable. |
| PG-004 | Risk tiers: T0 lightweight, T1 standard, T2 strict + human sign-off. |

## 6. Non-Functional Requirements
| ID | Requirement |
|---|---|
| NFR-001 | Provider-agnostic core. |
| NFR-002 | Human-readable YAML configs. |
| NFR-003 | Fail-fast validation for invalid config. |
| NFR-004 | Structured inspectable state files. |
| NFR-005 | Resume after interruption. |

## 7. Success Metrics
- First working pipeline in <30 minutes.
- Agent swap with no framework code changes.
- Overlay toggle by config only.
- Workflow customization via YAML only.
