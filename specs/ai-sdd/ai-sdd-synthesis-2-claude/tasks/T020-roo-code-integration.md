# T020: Roo Code Native Integration

**Phase:** 3 (Native Integration)
**Status:** PENDING
**Dependencies:** T010 (CLI + config), Phase 1 complete
**Size:** M (5 days)

---

## Context

Roo Code supports **custom modes** — configurable agent personas with their own system
prompts and tool access. This maps directly to ai-sdd agent roles.

The integration has two parts:

1. **Static `.roomodes` file** — defines all SDD agent modes as Roo Code personas. Shipped
   as a static template with the framework; constitution handles project-specific context.
   No `generate_modes.py` code generator — static templates work because the agent roles
   are stable; the constitution provides all project-specific context dynamically.

2. **Shared MCP server** — exposes `ai-sdd` engine operations as MCP tools. Used by
   both Roo Code (native MCP support) and Claude Code (via MCP client). Lives in
   `integration/mcp_server/` — not scoped to Roo Code only.

**No `generate_modes.py`**. Roo mode files are static templates shipped with the framework.
**No `install.sh`**. `ai-sdd init --tool roo_code` handles setup.

---

## Acceptance Criteria

```gherkin
Feature: Roo Code native integration

  Scenario: SDD agent modes available in Roo Code
    Given ai-sdd installed with Roo Code integration
    When the user opens the mode switcher in Roo Code
    Then modes sdd-ba, sdd-architect, sdd-pe, sdd-le, sdd-dev, sdd-reviewer are available
    And each mode has the correct persona and tool restrictions

  Scenario: BA mode reads workflow state via MCP
    Given Roo Code in "sdd-ba" mode with MCP server running
    When the agent starts a task
    Then it calls the get_next_task MCP tool
    And reads the required inputs from the artifact manifest in constitution.md
    And produces the output artifact using Roo Code's native Write tool

  Scenario: Task completed via MCP
    Given a DEV agent completing an implementation task in Roo Code
    When the agent calls the complete_task MCP tool with the output path
    Then ai-sdd marks the task COMPLETED in the state file
    And the constitution manifest is updated to reflect the new artifact

  Scenario: HIL item surfaces in Roo Code
    Given a PENDING HIL queue item
    When Roo Code polls via the get_hil_queue MCP tool
    Then the item is shown to the user with context
    And the user can call resolve_hil_item or reject_hil_item from within Roo Code

  Scenario: Mode restrictions enforced
    Given Roo Code in "sdd-ba" mode
    When the user requests code generation
    Then the BA mode's system prompt instructs Roo Code to decline
    And it suggests switching to "sdd-dev" mode

  Scenario: MCP server also usable from Claude Code
    Given the shared MCP server running
    When Claude Code connects to it via its MCP client
    Then all the same tools (get_workflow_status, complete_task, etc.) are available
    And behavior is identical to Roo Code's use of the same server
```

---

## Deliverables

### 1. Static `.roomodes` File

Roo Code reads agent mode definitions from a `.roomodes` file in the project root.
This is a JSON file with mode definitions — shipped as a static template.

```json
// .roomodes (static template — shipped with framework)
{
  "customModes": [
    {
      "slug": "sdd-ba",
      "name": "SDD: Business Analyst",
      "roleDefinition": "You are the Business Analyst in an ai-sdd Specification-Driven Development workflow. Translate business needs into formal requirements. Produce requirements.md with functional requirements, NFRs, and Gherkin acceptance criteria.",
      "groups": ["read", "edit", "browser", "command", "mcp"],
      "customInstructions": "Read only. Do not write code. Use the get_next_task MCP tool to find your current task. Read constitution.md for project context and artifact locations. Use complete_task MCP tool when done."
    },
    {
      "slug": "sdd-architect",
      "name": "SDD: Architect",
      "roleDefinition": "You are the System Architect in an ai-sdd workflow. Design high-level architecture from requirements. Produce design/l1.md covering architecture overview, component map, and API contracts.",
      "groups": ["read", "edit", "browser", "command", "mcp"],
      "customInstructions": "Do not write implementation code. Read requirements.md before designing. Justify all architectural decisions. Use MCP tools to interact with workflow state."
    },
    {
      "slug": "sdd-pe",
      "name": "SDD: Principal Engineer",
      "roleDefinition": "You are the Principal Engineer. Design detailed component specifications from the L1 architecture. Produce design/l2.md.",
      "groups": ["read", "edit", "command", "mcp"],
      "customInstructions": "Do not write implementation code. Read design/l1.md before designing components."
    },
    {
      "slug": "sdd-le",
      "name": "SDD: Lead Engineer",
      "roleDefinition": "You are the Lead Engineer. Break down L2 component design into discrete implementation tasks with Gherkin acceptance criteria.",
      "groups": ["read", "edit", "command", "mcp"],
      "customInstructions": "Produce implementation/tasks/*.md files. Each task must have Gherkin acceptance criteria."
    },
    {
      "slug": "sdd-dev",
      "name": "SDD: Developer",
      "roleDefinition": "You are the Developer. Implement code to satisfy the implementation task specifications. Follow BDD — write tests first.",
      "groups": ["read", "edit", "command", "mcp"],
      "customInstructions": "Read the task spec before writing code. Write tests before implementation. Verify outputs match the artifact contract."
    },
    {
      "slug": "sdd-reviewer",
      "name": "SDD: Reviewer",
      "roleDefinition": "You are the Reviewer. Evaluate artifacts against quality guidelines from the project constitution. Issue GO or NO_GO with specific rework feedback.",
      "groups": ["read", "command", "mcp"],
      "customInstructions": "Do not modify artifacts. Issue a structured review decision: { decision: GO|NO_GO, feedback: '...' }. Use constitution Standards section as your review criteria."
    }
  ]
}
```

### 2. Shared MCP Server (`integration/mcp_server/`)

Wraps existing `ai-sdd` CLI operations as MCP tools. Used by both Roo Code and Claude Code.

```python
# integration/mcp_server/server.py
# ~100 lines. No reimplementation — all tools delegate to ai-sdd CLI via subprocess.

@mcp.tool()
def get_workflow_status() -> dict:
    """Return current workflow state (all task statuses)."""
    return _run_cli(["ai-sdd", "status", "--json"])

@mcp.tool()
def get_next_task() -> dict:
    """Return the next READY task."""
    return _run_cli(["ai-sdd", "status", "--next", "--json"])

@mcp.tool()
def complete_task(task_id: str, output_path: str, output_content: str) -> dict:
    """Write task output file and mark task COMPLETED."""
    Path(output_path).write_text(output_content)
    return _run_cli(["ai-sdd", "run", "--task", task_id])

@mcp.tool()
def get_hil_queue() -> list[dict]:
    """Return all PENDING HIL queue items."""
    return _run_cli(["ai-sdd", "hil", "list", "--json"])

@mcp.tool()
def resolve_hil_item(item_id: str, notes: str = "") -> dict:
    return _run_cli(["ai-sdd", "hil", "resolve", item_id, "--notes", notes])

@mcp.tool()
def reject_hil_item(item_id: str, reason: str) -> dict:
    return _run_cli(["ai-sdd", "hil", "reject", item_id, "--reason", reason])

@mcp.tool()
def get_constitution(task_id: str = "") -> str:
    """Return the merged constitution (includes artifact manifest)."""
    return _run_cli(["ai-sdd", "constitution", "--task", task_id] if task_id
                    else ["ai-sdd", "constitution"])

def _run_cli(args: list[str]) -> Any:
    result = subprocess.run(args, capture_output=True, text=True, check=True)
    return json.loads(result.stdout)
```

Started via:
```bash
ai-sdd serve --mcp --port 3000
```

### 3. MCP Server Config for Roo Code

```json
// .roo/mcp.json
{
  "mcpServers": {
    "ai-sdd": {
      "command": "ai-sdd",
      "args": ["serve", "--mcp"],
      "env": {}
    }
  }
}
```

### 4. Install via CLI (no install.sh)

```bash
# Add Roo Code integration to a project
ai-sdd init --tool roo_code --project /path/to/project

# Copies:
#   .roomodes          (static agent mode definitions)
#   .roo/mcp.json      (MCP server config)
#   .ai-sdd/           (framework config, if not present)
```

---

## File Structure

```
integration/
├── mcp_server/                       # Shared — used by Roo Code + Claude Code
│   ├── server.py
│   ├── README.md
│   └── tests/
│       └── test_mcp_server.py
└── roo_code/
    ├── README.md
    ├── .roomodes.template             # Static agent mode definitions
    └── mcp_config.json.template       # .roo/mcp.json template
```

---

## Files to Create

- `integration/mcp_server/server.py`
- `integration/mcp_server/README.md`
- `integration/roo_code/README.md`
- `integration/roo_code/.roomodes.template`
- `integration/roo_code/mcp_config.json.template`
- `tests/integration/test_mcp_server.py`
- `tests/integration/test_roo_code_integration.py`

---

## Test Strategy

- Unit tests: each MCP tool delegates correctly to `ai-sdd` CLI; output parsed correctly.
- Unit tests: `_run_cli` raises AdapterError on non-zero exit.
- Integration test: `complete_task` writes file and advances workflow state.
- Integration test: `get_hil_queue` returns correct items; `resolve_hil_item` unblocks.
- Manual validation: Run sdd-ba → sdd-architect workflow inside Roo Code with MCP active.

## Rollback/Fallback

- If MCP server fails to start: `ai-sdd run` still works via CLI; MCP is additive.
- If `.roomodes` already exists: `ai-sdd init` prompts before overwriting.
