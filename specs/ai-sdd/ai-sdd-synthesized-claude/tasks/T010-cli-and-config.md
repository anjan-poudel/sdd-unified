# T010: CLI, Project Config, and Runtime Adapter

**Phase:** 1 (Core Engine)
**Status:** PENDING
**Dependencies:** T004 (core engine)

---

## Context

The CLI is the primary user entry point for `ai-sdd`. It loads project configuration, initializes the engine, and provides operational commands (run, resume, status, validate-config, hil).

The project config file (`ai-sdd.yaml`) is the single control plane for all project-level settings: active workflow, overlay enablement, LLM defaults, and per-task overrides.

The `RuntimeAdapter` interface decouples the engine from specific AI coding tools, making the core engine testable and runtime-portable.

---

## Acceptance Criteria

```gherkin
Feature: CLI

  Scenario: Run a workflow
    Given a project with a valid .ai-sdd/ai-sdd.yaml
    When `ai-sdd run` is executed from the project root
    Then the engine loads the config and workflow
    And begins task execution

  Scenario: Resume an interrupted workflow
    Given a workflow that was interrupted with tasks B and C pending
    When `ai-sdd run --resume` is executed
    Then the engine loads state from disk
    And continues from the last PENDING tasks

  Scenario: Show workflow status
    When `ai-sdd status` is executed
    Then all tasks are listed with their current status (PENDING, RUNNING, COMPLETED, FAILED)
    And the current iteration count for looping tasks is shown

  Scenario: Run a specific task
    When `ai-sdd run --task design-l1` is executed
    Then only that task (and its unmet dependencies) are executed

  Scenario: Validate config without running
    When `ai-sdd validate-config` is executed
    Then the engine validates ai-sdd.yaml, the workflow YAML, and all agent YAMLs
    And reports all validation errors without executing any tasks

  Scenario: Dry run
    When `ai-sdd run --dry-run` is executed
    Then the engine prints the execution plan (task order, overlay config per task)
    And no LLM calls are made

Feature: Project config

  Scenario: Agent-level config overrides project default
    Given ai-sdd.yaml sets default LLM to claude-opus-4-6
    And agent ba.yaml sets LLM to claude-sonnet-4-6
    When the BA agent is loaded
    Then the BA agent uses claude-sonnet-4-6 (agent-level wins)

  Scenario: Config cascade: CLI flag wins over file
    Given ai-sdd.yaml sets hil.enabled=true
    And CLI flag --no-hil is passed
    When the engine initializes
    Then HIL is disabled (CLI flag wins)

  Scenario: Invalid config fails fast
    Given ai-sdd.yaml references a workflow file that does not exist
    When `ai-sdd run` is executed
    Then an error is raised immediately: "workflow file not found: ..."
    And no tasks run

Feature: RuntimeAdapter

  Scenario: Mock adapter for tests
    Given the engine is initialized with a MockRuntimeAdapter
    When a task is dispatched
    Then the mock adapter records the call and returns a configurable response
    And no real LLM calls are made

  Scenario: ClaudeCode adapter
    Given the engine is initialized with a ClaudeCodeAdapter
    When a task is dispatched
    Then the adapter formats the task as a Claude Code command and executes it

  Scenario: Adapter failure with retry
    Given a ClaudeCodeAdapter and a transient network error on dispatch
    When the adapter fails
    Then it retries up to `adapter.max_retries` times
    And if retries are exhausted, the task is marked FAILED
```

---

## ai-sdd.yaml Config Schema

```yaml
version: "1"

project:
  name: "my-project"
  root: "."

workflow:
  file: ".ai-sdd/workflows/default-sdd.yaml"

llm:
  default_provider: anthropic
  default_model: claude-sonnet-4-6

agents:
  directory: ".ai-sdd/agents/"      # project-specific overrides
  use_defaults: true                # load default agents from framework

constitution:
  file: "constitution.md"           # filename to look for at each level

overlays:
  hil:
    enabled: true
    queue_path: ".ai-sdd/state/hil/"
    poll_interval_seconds: 2
  policy_gate:
    enabled: false
    default_risk_tier: T1
  confidence_loop:
    enabled: false
  paired_workflow:
    enabled: false
  agentic_review:
    enabled: false

adapter:
  type: claude_code               # claude_code | codex | mock
  max_retries: 3
  retry_backoff_seconds: 5

state:
  path: ".ai-sdd/state/workflow-state.json"

observability:
  log_level: INFO                  # DEBUG | INFO | WARN | ERROR
  log_file: ".ai-sdd/logs/ai-sdd.log"
```

Config merge precedence (highest priority wins):
1. CLI flags
2. Project `.ai-sdd/ai-sdd.yaml`
3. Framework `config/defaults.yaml`

---

## CLI Commands

```bash
ai-sdd run                          # run workflow from the beginning
ai-sdd run --resume                 # resume from last persisted state
ai-sdd run --task <task-id>         # run specific task + unmet dependencies
ai-sdd run --dry-run                # print execution plan, no LLM calls
ai-sdd status                       # show all task statuses
ai-sdd validate-config              # validate all config files, no execution
ai-sdd hil list                     # list pending HIL items
ai-sdd hil show <item-id>           # show HIL item context
ai-sdd hil resolve <item-id>        # resolve HIL item
ai-sdd hil reject <item-id>         # reject HIL item
```

---

## Implementation Notes

- CLI built with `typer` (preferred) or `click`.
- Config discovered from `.ai-sdd/ai-sdd.yaml` relative to CWD.
- `validate-config` runs schema validation on all YAML files without dispatching tasks.
- Adapters in Phase 1: `MockRuntimeAdapter`, `ClaudeCodeAdapter`.
- Adapters planned for Phase 2: `CodexAdapter`, `GeminiAdapter`.
- All CLI commands emit structured observability events.

---

## Files to Create

- `cli/main.py`
- `cli/commands.py`
- `core/runtime_adapter.py` (interface)
- `adapters/mock_adapter.py`
- `adapters/claude_code_adapter.py`
- `config/defaults.yaml`
- `tests/test_cli.py`
- `tests/test_config_loading.py`

---

## Test Strategy

- CLI integration tests: run, resume, status, validate-config, dry-run.
- Unit tests: config merge precedence (CLI > project > defaults).
- Unit tests: config validation (missing workflow file, invalid agent reference).
- Integration tests: mock adapter records dispatches; real adapter stub.

## Rollback/Fallback

- If adapter fails after max retries: mark task FAILED, persist state, exit.
- If config validation fails: print all errors, exit before any task runs.
- If project config is missing: use framework defaults with a warning.
