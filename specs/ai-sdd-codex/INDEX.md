# ai-sdd Spec Index (Codex)

## Documents
| Doc | Purpose |
|---|---|
| [PRD.md](PRD.md) | Product requirements |
| [PLAN.md](PLAN.md) | Architecture and implementation plan |
| [ROADMAP.md](ROADMAP.md) | Milestones and task groups |
| [ROADMAP.yaml](ROADMAP.yaml) | Machine-readable roadmap |

## Tasks
| Task | Title | Dependencies |
|---|---|---|
| [T001](tasks/T001-agent-system.md) | Agent System | none |
| [T002](tasks/T002-workflow-system.md) | Workflow System | T001 |
| [T003](tasks/T003-constitution-system.md) | Constitution System | none |
| [T004](tasks/T004-core-engine.md) | Core Engine | T001, T002, T003 |
| [T005](tasks/T005-hil-overlay.md) | HIL Overlay | T004 |
| [T006](tasks/T006-confidence-overlay.md) | Confidence Overlay | T004 |
| [T007](tasks/T007-paired-workflow-overlay.md) | Paired Workflow Overlay | T004, T006 |
| [T008](tasks/T008-agentic-review-overlay.md) | Agentic Review Overlay | T004, T005, T006 |
| [T009](tasks/T009-cli-and-config.md) | CLI and Config | T004 |
