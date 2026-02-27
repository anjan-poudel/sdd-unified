# T010: CLI, Project Config, and Runtime Adapter

**Phase:** 1 (Core Engine)
**Status:** PENDING
**Dependencies:** T004 (core engine)
**Changes from synthesized-claude:** Added `ai-sdd init`, `ai-sdd run --step`, `ai-sdd status --metrics`, `ai-sdd constitution`, `ai-sdd serve --mcp`; updated config schema with `engine` section, `openai` adapter type; updated adapter type list.

---

## Context

The CLI is the primary user entry point for `ai-sdd`. It loads project configuration, initializes the engine, and provides operational commands.

The `ai-sdd init --tool <name>` command installs integration files (slash commands, AGENTS.md, .roomodes) into a project — replacing per-tool `install.sh` scripts.

The `RuntimeAdapter` interface decouples the engine from specific AI tools, making it testable and runtime-portable.

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

  Scenario: Step mode pauses after each task
    When `ai-sdd run --step` is executed
    Then the engine runs the first task
    And pauses after it completes, showing task output
    And the operator can choose: [c]ontinue, [s]kip next, [a]bort

  Scenario: Show workflow status
    When `ai-sdd status` is executed
    Then all tasks are listed with their current status
    And the current iteration count for looping tasks is shown

  Scenario: Show workflow status with metrics
    When `ai-sdd status --metrics` is executed
    Then the status table includes: tokens_used, estimated_cost_usd, duration_ms per task
    And a totals row shows cumulative cost for the run

  Scenario: Validate config without running
    When `ai-sdd validate-config` is executed
    Then the engine validates ai-sdd.yaml, workflow YAML, and all agent YAMLs
    And reports all validation errors without executing any tasks

  Scenario: Dry run
    When `ai-sdd run --dry-run` is executed
    Then the engine prints the execution plan (task order, overlay config per task)
    And no LLM calls are made

  Scenario: Init installs tool integration files
    When `ai-sdd init --tool claude_code --project /path/to/project` is executed
    Then .claude/agents/sdd-*.md subagent files are copied (one per SDD role)
    And .claude/skills/sdd-run/SKILL.md orchestrating skill is copied
    And .claude/skills/sdd-status/SKILL.md status skill is copied
    And CLAUDE.md template is added (or appended) to the project root
    And .ai-sdd/ config directory is created if absent

  Scenario: Init for Roo Code
    When `ai-sdd init --tool roo_code --project /path/to/project` is executed
    Then .roomodes is copied to the project root
    And .roo/mcp.json is created with the ai-sdd MCP server config

  Scenario: Init for Codex CLI
    When `ai-sdd init --tool codex --project /path/to/project` is executed
    Then AGENTS.md template is added to the project root
    And .ai-sdd/ config is created if absent
    Note: --tool controls CLI UX path (AGENTS.md vs slash commands).
          adapter.type: openai in ai-sdd.yaml controls the API runtime path.
          These are independent settings.

  Scenario: MCP server starts on serve command
    When `ai-sdd serve --mcp` is executed
    Then the MCP server starts on the default port (3000)
    And exposes get_workflow_status, complete_task, get_hil_queue tools

  Scenario: Constitution command returns merged constitution
    When `ai-sdd constitution` is executed
    Then the merged constitution (including artifact manifest) is printed to stdout
    When `ai-sdd constitution --task design-l1` is executed
    Then the constitution merged for the design-l1 task context is printed

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
    When a task is dispatched with an idempotency_key
    Then the mock adapter records the call and key
    And returns a configurable response
    And no real LLM calls are made
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
  directory: ".ai-sdd/agents/"
  use_defaults: true

constitution:
  file: "constitution.md"

engine:
  max_concurrent_tasks: 3
  rate_limit_requests_per_minute: 20
  cost_budget_per_run_usd: 10.00    # pause → HIL when exceeded

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
  type: claude_code   # claude_code | openai | roo_code | mock
  max_retries: 3
  retry_backoff_seconds: 5

state:
  path: ".ai-sdd/state/workflow-state.json"

observability:
  log_level: INFO
  log_file: ".ai-sdd/logs/ai-sdd.log"
  secret_patterns: []               # additional regex patterns to redact
```

---

## CLI Commands

```bash
# Workflow execution
ai-sdd run                           # run from beginning
ai-sdd run --resume                  # resume from last state
ai-sdd run --task <task-id>          # run specific task + unmet deps
ai-sdd run --dry-run                 # print plan; no LLM calls
ai-sdd run --step                    # pause after each task for operator review

# Status and monitoring
ai-sdd status                        # show all task statuses
ai-sdd status --metrics              # include tokens, cost, duration per task
ai-sdd status --json                 # machine-readable JSON (full workflow state)
ai-sdd status --next --json          # JSON of next READY task(s) only; used by MCP get_next_task()

# Configuration
ai-sdd validate-config               # validate all YAML configs, no execution
ai-sdd constitution                  # print merged constitution
ai-sdd constitution --task <id>      # print constitution for specific task context

# Human-in-the-Loop
ai-sdd hil list                      # list PENDING HIL items
ai-sdd hil show <item-id>            # show item context
ai-sdd hil resolve <item-id>         # resolve (unblock task)
ai-sdd hil reject <item-id>          # reject (fail task)

# Task completion (used by MCP server — atomic write + validate + advance)
ai-sdd complete-task --task <task-id> --output-path <path> --content-file <tmp>
                                     # 1. validates path against allowlist
                                     # 2. runs security sanitization
                                     # 3. validates artifact contract
                                     # 4. atomically writes file + advances state + updates manifest

# Project setup
ai-sdd init --tool <name> --project <path>   # install tool integration files
                                             # <name>: claude_code | codex | roo_code

# MCP server (for Roo Code / Claude Code MCP client)
ai-sdd serve --mcp                   # start MCP server (default port 3000)
ai-sdd serve --mcp --port 3001
```

---

## Implementation Notes

- CLI built with `typer`.
- Config discovered from `.ai-sdd/ai-sdd.yaml` relative to CWD.
- `ai-sdd init` copies files from `integration/<tool>/` to the target project.
- `ai-sdd serve --mcp` starts `integration/mcp_server/server.py`.
- `ai-sdd constitution` calls `ConstitutionResolver` directly and prints to stdout (used by MCP server's `get_constitution` tool).
- All CLI commands emit structured observability events.
- Adapters in Phase 1: `MockRuntimeAdapter`, `ClaudeCodeAdapter`.
- Phase 3: `OpenAIAdapter`; MCP server (T020).

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

- CLI integration tests: run, resume, step, status, status --metrics, validate-config, dry-run.
- CLI integration tests: init --tool claude_code/openai/roo_code copies correct files.
- Unit tests: config merge precedence (CLI > project > defaults).
- Unit tests: config validation (missing workflow file, invalid agent reference).
- Unit tests: MockRuntimeAdapter records idempotency_key correctly.

## Rollback/Fallback

- If adapter fails after max retries: mark task FAILED, persist state, exit.
- If config validation fails: print all errors, exit before any task runs.
- If project config is missing: use framework defaults with a warning.
- If `ai-sdd init` target files already exist: prompt before overwriting.
