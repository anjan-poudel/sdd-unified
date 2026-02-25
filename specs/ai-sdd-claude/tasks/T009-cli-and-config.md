# T009: CLI, Project Config, and Runtime Adapter

**Phase:** 1 (Core Engine)
**Status:** PENDING
**Dependencies:** T004 (core engine)

---

## Context

The CLI is the primary user entry point for `ai-sdd`. It loads project configuration, initializes the engine, and provides operational commands (run, status, HIL management).

The project config file (`ai-sdd.yaml`) is the single control plane for all project-level settings: active workflow, overlay enablement, LLM defaults, and per-task overrides.

The RuntimeAdapter interface decouples the engine from specific AI coding tools (Claude Code, Codex, Gemini, etc.), making the core engine testable and runtime-portable.

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

  Scenario: Run a specific task
    When `ai-sdd run --task design-l1` is executed
    Then only that task (and its unmet dependencies) are executed

Feature: Project config

  Scenario: Config overrides framework defaults
    Given ai-sdd.yaml sets default LLM to claude-opus-4-6
    And agent ba.yaml sets LLM to claude-sonnet-4-6
    When the BA agent is loaded
    Then the BA agent uses claude-sonnet-4-6 (agent-level config wins over default)

  Scenario: Invalid config fails fast
    Given ai-sdd.yaml references a workflow file that does not exist
    When `ai-sdd run` is executed
    Then an error is raised immediately: "workflow file not found: ..."

Feature: RuntimeAdapter

  Scenario: Mock adapter for tests
    Given the engine is initialized with a MockRuntimeAdapter
    When a task is dispatched
    Then the mock adapter records the call and returns a configurable response
    And no real LLM calls are made

  Scenario: Claude Code adapter
    Given the engine is initialized with a ClaudeCodeAdapter
    When a task is dispatched
    Then the adapter formats the task as a Claude Code command and executes it
```

---

## ai-sdd.yaml Config Schema (Draft)

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
  directory: ".ai-sdd/agents/"        # project-specific agent overrides
  use_defaults: true                  # load default agents from framework

constitution:
  file: "constitution.md"             # filename to look for at each level

overlays:
  hil:
    enabled: true
    queue_path: ".ai-sdd/state/hil/"
  confidence_loop:
    enabled: false
  paired_workflow:
    enabled: false
  agentic_review:
    enabled: false

state:
  path: ".ai-sdd/state/workflow-state.json"
```

---

## Implementation Notes

- CLI built with `click` or `typer`.
- Config loaded from `.ai-sdd/ai-sdd.yaml` relative to current working directory.
- Config merge order: framework defaults → project `ai-sdd.yaml` → CLI flags.
- RuntimeAdapter interface:
  ```python
  class RuntimeAdapter(ABC):
      @abstractmethod
      def dispatch(self, task: Task, context: AgentContext) -> TaskResult:
          ...
  ```
- Adapters to implement in Phase 1: `MockRuntimeAdapter` (for tests), `ClaudeCodeAdapter`.
- Adapters to plan for Phase 2: `CodexAdapter`, `GeminiAdapter`.

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
