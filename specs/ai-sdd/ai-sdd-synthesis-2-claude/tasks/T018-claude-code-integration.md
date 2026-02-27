# T018: Claude Code Native Integration

**Phase:** 3 (Native Integration)
**Status:** PENDING
**Dependencies:** T010 (CLI + config), Phase 1 complete
**Size:** S (4 days) *(reduced from 8 — interactive adapter removed)*

---

## Context

When running **inside** Claude Code, `ai-sdd` does not need an adapter layer — Claude Code
is both the orchestration surface and the agent runtime. The slash commands tell Claude Code
what to do; Claude Code uses its own native tools (Bash, Read, Grep) to interact with the
`ai-sdd` CLI and read artifacts directly.

The adapter (headless path) is kept only for **CI/programmatic** use where Claude Code runs
as a subprocess.

**Integration model:**
```
Interactive (within Claude Code):
  User → /sdd-run slash command
       → Claude Code reads constitution.md (Read tool)
       → Claude Code runs `ai-sdd run --task <id>` (Bash tool)
       → Claude Code writes artifact (Write tool)
       → Claude Code runs `ai-sdd status` (Bash tool) to show progress

Headless / CI:
  ai-sdd engine → ClaudeCodeAdapter → subprocess `claude --print --prompt-file task.md`
```

---

## Acceptance Criteria

```gherkin
Feature: Claude Code native integration

  Scenario: User runs /sdd-run inside Claude Code
    Given a project with .ai-sdd/ configured
    When the user runs /sdd-run
    Then Claude Code reads the workflow state via Bash: `ai-sdd status`
    And displays the next READY task
    And asks the user to confirm before executing

  Scenario: Claude Code executes a task using native tools
    Given Claude Code is in "sdd-architect" mode (via CLAUDE.md agent role)
    When executing task "design-l1"
    Then Claude Code reads requirements.md using its Read tool
    And produces design/l1.md using its Write tool
    And advances the workflow by running `ai-sdd run --task design-l1 --complete`

  Scenario: /sdd-status shows workflow progress
    When the user runs /sdd-status
    Then Claude Code runs `ai-sdd status --json` via Bash
    And renders a human-readable progress table in the session

  Scenario: /sdd-hil surfaces pending approvals
    Given a PENDING HIL item
    When the user runs /sdd-hil
    Then Claude Code runs `ai-sdd hil list` via Bash
    And presents the item context to the user for a decision
    And runs `ai-sdd hil resolve <id>` or `ai-sdd hil reject <id>` based on user choice

  Scenario: CLAUDE.md steers agent behavior
    Given CLAUDE.md is present in the project root
    When Claude Code opens the project
    Then it loads the SDD methodology instructions automatically
    And follows the correct agent role for the active task

  Scenario: Headless adapter dispatches task as subprocess
    Given ai-sdd running in CI with adapter: claude_code
    When a task is dispatched
    Then ClaudeCodeAdapter writes a task prompt file to a temp path
    And calls `claude --print --prompt-file <path>` as a subprocess
    And captures stdout as the task output
```

---

## Deliverables

### 1. Slash Commands (`.claude/commands/`)

Plain markdown files — no custom code. Claude Code executes these as prompts.

**`sdd-run.md`**
```markdown
Run the active ai-sdd workflow task.

1. Run `ai-sdd status --json` to find the next READY task.
2. Read the task's required inputs from the paths listed in the artifact manifest
   (check constitution.md → "## Workflow Artifacts" section).
3. Execute the task in your role as the assigned agent (see CLAUDE.md for your role).
4. Write the output artifact to the path specified.
5. Run `ai-sdd run --task <task-id>` to record completion and advance the workflow.
6. Show the updated status.
```

**`sdd-status.md`**
```markdown
Show the current ai-sdd workflow status.
Run: `ai-sdd status` and display the output.
Highlight any FAILED or HIL_PENDING tasks.
```

**`sdd-hil.md`**
```markdown
Show and resolve pending Human-in-the-Loop items.
1. Run `ai-sdd hil list` to show all PENDING items.
2. For each item, display the context and ask the user for a decision.
3. Run `ai-sdd hil resolve <id>` or `ai-sdd hil reject <id> --reason "..."`.
```

**`sdd-validate.md`**
```markdown
Validate the ai-sdd configuration without running.
Run: `ai-sdd validate-config` and report any errors.
```

**`sdd-step.md`**
```markdown
Run the workflow one task at a time in step mode.
Run: `ai-sdd run --step` and pause after each task to show output.
```

### 2. CLAUDE.md Template

Lightweight project orientation. Relies on the constitution for artifact context — no duplication.

```markdown
# CLAUDE.md

## Project Methodology
This project uses ai-sdd for Specification-Driven Development.
Workflow state: `.ai-sdd/state/workflow-state.json`
Artifact manifest: see `## Workflow Artifacts` in `constitution.md`

## How to Work
- Run `/sdd-status` to see what task is next.
- Run `/sdd-run` to execute the next task.
- Run `/sdd-hil` if a human decision is needed.
- Read `constitution.md` to understand project context and available artifacts.
- Use the Read tool to read artifacts; use Bash to run `ai-sdd` commands.

## Your Role
Your active agent role is determined by the current workflow task.
See `constitution.md → ## Agent Roles` for role descriptions.
Do not perform work outside your assigned agent's scope.

## SDD Rules
- Write acceptance criteria in Gherkin format.
- Justify architectural decisions against requirements.
- Verify outputs match the artifact contract before marking a task complete.
```

### 3. ClaudeCodeAdapter (headless/CI only)

```python
class ClaudeCodeAdapter(RuntimeAdapter):
    """
    For headless/CI use only. Interactive Claude Code sessions use slash
    commands directly — no adapter needed for that path.
    """
    def dispatch(self, task: Task, context: AgentContext,
                 idempotency_key: str) -> TaskResult:
        prompt_path = self._write_prompt_file(task, context)
        result = subprocess.run(
            ["claude", "--print", "--prompt-file", str(prompt_path)],
            capture_output=True, text=True, timeout=self.timeout_seconds
        )
        return self._parse_result(result, task)
```

### 4. Install via CLI (no install.sh)

```bash
# Add Claude Code integration to a project
ai-sdd init --tool claude_code --project /path/to/project

# Copies:
#   .claude/commands/sdd-*.md   (slash commands)
#   CLAUDE.md                   (appends if exists, creates if not)
#   .ai-sdd/                    (framework config, if not present)
```

This is handled by the existing `ai-sdd init` CLI command (T010). No separate `install.sh`.

---

## Files to Create

- `integration/claude_code/slash_commands/sdd-run.md`
- `integration/claude_code/slash_commands/sdd-status.md`
- `integration/claude_code/slash_commands/sdd-hil.md`
- `integration/claude_code/slash_commands/sdd-validate.md`
- `integration/claude_code/slash_commands/sdd-step.md`
- `integration/claude_code/CLAUDE.md.template`
- `integration/claude_code/README.md`
- `adapters/claude_code_adapter.py` (headless path only)
- `tests/integration/test_claude_code_adapter.py` (headless path only)

---

## Test Strategy

- Unit tests: ClaudeCodeAdapter writes prompt file in correct format.
- Unit tests: `ai-sdd init --tool claude_code` copies files correctly.
- Integration test: headless `claude --print` path produces parseable TaskResult.
- Manual validation: run `/sdd-run` inside Claude Code; task executes and state advances.

## Rollback/Fallback

- If `claude` binary not in PATH: adapter raises clear error; falls back to MockAdapter in tests.
- If slash command files already exist: `ai-sdd init` prompts before overwriting.
