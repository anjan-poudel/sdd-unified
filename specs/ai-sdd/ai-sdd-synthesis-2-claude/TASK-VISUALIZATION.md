# ai-sdd Task Visualization — Full Picture

**Date:** 2026-02-27

---

## 1. What Users See vs. What the Framework Does

T012–T017 are infrastructure tasks — invisible when working correctly, critical when things
go wrong. Developers interact with their *effects*, not the tasks themselves.

| Task | Category | What the user sees / experiences |
|---|---|---|
| T001 Agent System | **Core** | Agent YAML files they read/edit |
| T002 Workflow System | **Core** | `workflow.yaml` they configure |
| T003 Constitution System | **Core** | `constitution.md` they write; artifact manifest auto-appears |
| T004 Core Engine | **Core** | `ai-sdd run` — it just works |
| T005 HIL Overlay | **Core** | Approval prompts at decision points |
| T006 Evidence Gate | **Core** | PASS/FAIL verdict with evidence summary |
| T007 Confidence Loop | **Optional** | Auto-advance when quality threshold met |
| T008 Paired Workflow | **Optional** | Two-agent critique loop |
| T009 Agentic Review | **Optional** | Coder/reviewer cycle with GO/NO_GO |
| T010 CLI | **Core** | Every `ai-sdd` command they type |
| T011 Observability | **Background** | Log file, `status --metrics` cost output |
| T012 Expression DSL | **Infrastructure** | Load-time error if exit condition has a typo — caught before any LLM call |
| T013 Artifact Contract | **Infrastructure** | "requirements.md missing section: acceptance_criteria" — before Architect wastes 90 min |
| T014 Overlay Composition | **Infrastructure** | Overlays compose predictably; CI prevents regressions |
| T015 Adapter Reliability | **Infrastructure** | API 429 at 11pm → transparent retry; user wakes up to a completed workflow |
| T016 Constitution Manifest | **Background** | `## Workflow Artifacts` table auto-updated in constitution.md after each task |
| T017 Security | **Background** | Confluence export with injection → HIL escalation; secrets never in logs |
| T018 Claude Code | **Integration** | `/sdd-run` slash command; CLAUDE.md steers agent persona |
| T019 OpenAI/Codex | **Integration** | AGENTS.md steers `codex` CLI; OpenAIAdapter for batch/CI |
| T020 Roo Code | **Integration** | Mode switcher shows sdd-* modes; MCP tools for workflow state |

---

## 2. Full Task Dependency Graph

```
╔══════════════════════════════════════════════════════════════════════╗
║  PHASE 1 — Core Engine                                               ║
╚══════════════════════════════════════════════════════════════════════╝

T001 (Agent YAML) ──┐
                    ├──► T002 (Workflow DAG) ──┐
T003 (Constitution) ┘                          │
T012 (Expression DSL) ─────────────────────────┼──► T004 (Core Engine)
T013 (Artifact Contract) ──────────────────────┘         │
                                                          │
                              ┌───────────────────────────┤
                              │                           │
                    T005 (HIL) ◄──────────────────────────┤
                    T010 (CLI + Init) ◄───────────────────┤
                    T011 (Observability) ◄────────────────┤
                    T016 (Constitution Manifest) ◄────────┘

╔══════════════════════════════════════════════════════════════════════╗
║  PHASE 2 — Overlay Suite                                             ║
╚══════════════════════════════════════════════════════════════════════╝

T004 + T005 + T012 ──► T006 (Evidence Gate)
T006 ──────────────► T007 (Confidence Loop)
T007 ──────────────► T008 (Paired Workflow)
T007 + T005 ───────► T009 (Agentic Review)

T006 + T007 + T008 + T009 ──► T014 (Overlay Composition Tests)
                                    └── CI gate: must pass before any overlay merges

T010 (CLI/Adapters) ──► T015 (Adapter Reliability Contract)
T011 (Observability) ──► T017 (Security Baseline)

╔══════════════════════════════════════════════════════════════════════╗
║  PHASE 3 — Native Integration                                        ║
╚══════════════════════════════════════════════════════════════════════╝

T010 (CLI — provides ai-sdd init + serve --mcp)
  ├──► T018 (Claude Code: slash commands + CLAUDE.md)
  ├──► T019 (OpenAI/Codex: AGENTS.md + OpenAIAdapter)
  └──► T020 (Roo Code: .roomodes + shared MCP server)
```

---

## 3. Claude Code — How It Works

### Integration Model

```
Developer types /sdd-run in Claude Code session
    │
    ▼
Slash command (.claude/commands/sdd-run.md) instructs Claude Code to:
  1. Run `ai-sdd status --json` via Bash tool  → find next READY task
  2. Read constitution.md via Read tool        → get context + artifact manifest
  3. Execute the task as the assigned agent    → produce the artifact
  4. Write output using Write tool             → save to declared path
  5. Run `ai-sdd run --task <id>` via Bash     → advance workflow state
  6. Manifest writer fires (post-task hook)    → constitution.md updated
  7. Show status to user                       → next HIL or next task
```

Key point: Claude Code IS the agent runtime for interactive use. No adapter intercepts the session. The slash command IS the integration.

For **CI/headless** use: `ClaudeCodeAdapter` invokes `claude --print --prompt-file task.md` as a subprocess.

### Claude Code — Greenfield (New SaaS Product)

```
PROJECT: Invoice tracking SaaS for freelancers

Day 0 — Setup (5 min)
──────────────────────────────────────────────────────
  $ ai-sdd init --tool claude_code --project ./invoice-saas

Creates:
  .claude/commands/sdd-run.md         ← /sdd-run slash command
  .claude/commands/sdd-status.md      ← /sdd-status
  .claude/commands/sdd-hil.md         ← /sdd-hil
  CLAUDE.md                           ← project orientation + role instructions
  constitution.md                     ← blank template
  .ai-sdd/ai-sdd.yaml                 ← config (defaults)
  .ai-sdd/workflows/default-sdd.yaml  ← BA→Arch→PE→LE→Dev→Review DAG

User fills constitution.md:
  ## Purpose
  Invoice tracking SaaS for freelancers.
  ## Rules
  - API-first; no vendor lock-in for payments
  ## Standards
  - Python 3.12, FastAPI, PostgreSQL, pytest 80% coverage

Day 1 — Requirements (30-60 min)
──────────────────────────────────────────────────────
  User: /sdd-run

  CLAUDE.md tells Claude Code it is the sdd-ba agent.
  Claude Code:
    → Bash: ai-sdd status --json            (finds define-requirements is READY)
    → Read: constitution.md                 (project context)
    → Conversation: asks user 5 clarifying questions about invoice workflows
    → Write: .ai-sdd/outputs/requirements.md
    → Bash: ai-sdd run --task define-requirements

  Framework (invisible):
    T013: validates requirements.md has acceptance_criteria section ✓
    T016: updates constitution.md manifest
          | define-requirements | requirements.md | COMPLETED |
          | design-l1           | design/l1.md    | PENDING   |
    T005: HIL gate — "requirements produced, approve to continue?"
    User sees in session: "Requirements complete. Approve to proceed to architecture? [y/n]"

Day 1 — Architecture (60-90 min)
──────────────────────────────────────────────────────
  User approves HIL. Claude Code switches to sdd-architect role (per CLAUDE.md).
    → Read: constitution.md                 (manifest shows requirements.md = COMPLETED)
    → Read: .ai-sdd/outputs/requirements.md (pulls what it needs via manifest)
    → Produces: .ai-sdd/outputs/design/l1.md
    → Bash: ai-sdd run --task design-l1

  T006 Evidence Gate (T1 tier): verifies l1.md covers architecture_overview + api_contracts ✓
  T016: manifest updated; design-l1 = COMPLETED
  HIL: "Architecture ready. Review design/l1.md and approve?"

Day 2 — PE, LE, Dev, Review (same pattern)
──────────────────────────────────────────────────────
  Each step: Claude Code reads manifest → pulls relevant artifact → executes → Bash advances state

  sdd-dev produces src/ code.
  T006 Evidence Gate (T1): tests pass, lint clean, coverage ≥ 80%.
  sdd-reviewer: reviews against constitution Standards → GO.

Final state:
  .ai-sdd/outputs/requirements.md    ← BA
  .ai-sdd/outputs/design/l1.md       ← Architect
  .ai-sdd/outputs/design/l2.md       ← PE
  .ai-sdd/outputs/implementation/    ← LE tasks
  src/                               ← Dev implementation
  .ai-sdd/logs/ai-sdd.log            ← cost per task (T011)
```

### Claude Code — Brownfield (Adding Feature to Existing Codebase)

```
PROJECT: Add multi-currency support to existing invoice service (50k LOC, FastAPI)

Setup (10 min)
──────────────────────────────────────────────────────
  $ ai-sdd init --tool claude_code --project ./existing-invoice-service

User writes constitution.md with existing context:
  ## Background
  Existing: Python 3.12, FastAPI, PostgreSQL, SQLAlchemy ORM.
  Constraint: existing single-currency APIs must stay unchanged.
  Key modules: src/invoices/, src/billing/

  ## Rules
  - Backward-compatible only; no breaking API changes
  - Currency rate stored at invoice creation time (audit trail)

  ## Standards
  - Tests: pytest 90% for new code
  - DB: Alembic migrations, additive only (no column drops)

Configure workflow to skip phases already done:
  .ai-sdd/workflows/multi-currency.yaml:
    define-requirements:
      status: COMPLETED               ← requirements from Jira ticket already exist
    design-l1:
      status: COMPLETED               ← existing architecture is known

  $ ai-sdd run --task design-l2

Claude Code (sdd-pe agent, via CLAUDE.md):
  → Read: constitution.md             (sees existing architecture context)
  → Bash: grep -r "Invoice" src/ --include="*.py" -l
  → Read: src/invoices/models.py      (understand existing data model)
  → Bash: ai-sdd run --task design-l2 --complete

  Produces design/l2.md:
    - CurrencyRate table (new, additive migration)
    - InvoiceWithCurrency (extends existing Invoice, backward-compatible)
    - Impact analysis: src/invoices/models.py, src/billing/service.py need updates

T006 Evidence Gate (T2 tier — brownfield is higher risk):
  → T2 requires human sign-off
  → HIL: "Impact analysis shows 2 existing modules affected. Tech lead approval needed."
  → Tech lead reviews, types: ai-sdd hil resolve <id>
  → (Or: /sdd-hil in Claude Code session → resolves inline)
```

---

## 4. Roo Code — How It Works

### Integration Model

```
Developer opens Roo Code, switches to "SDD: Business Analyst" mode
    │
    ▼
.roomodes defines the agent persona (role, restrictions, instructions)
MCP server (ai-sdd serve --mcp) provides workflow state as tools:
  get_next_task()      → what should I work on?
  get_constitution()   → project context + artifact manifest
  complete_task(...)   → mark done, advance workflow
  get_hil_queue()      → what needs human decision?
  resolve_hil_item()   → unblock a paused task

Agent executes in the mode context:
  → Reads artifacts via Roo Code's native Read/Edit/Search tools
  → Uses Serena (if available) for code intelligence on brownfield projects
  → Calls complete_task() MCP when done
  → Engine advances, manifest updates, next task becomes READY
```

Key difference from Claude Code: Roo Code's **mode system enforces role boundaries**. In `sdd-ba` mode, Roo Code's system prompt prevents it from generating implementation code. In `sdd-architect` mode, it won't modify existing DB schemas. The mode IS the agent persona.

### Roo Code — Greenfield (New SaaS Product)

```
PROJECT: Invoice tracking SaaS for freelancers (same scenario as above)

Day 0 — Setup (5 min)
──────────────────────────────────────────────────────
  $ ai-sdd init --tool roo_code --project ./invoice-saas
  $ ai-sdd serve --mcp &                     ← start MCP server (stays running)

Creates:
  .roomodes                                  ← 6 SDD agent mode definitions
  .roo/mcp.json                              ← points to ai-sdd MCP server
  constitution.md                            ← blank template
  .ai-sdd/                                   ← config + workflow

.roomodes includes (excerpt):
  sdd-ba:
    "You are the Business Analyst. Translate business needs into
     formal requirements. Do NOT write code."
  sdd-architect:
    "You are the System Architect. Design L1 architecture from requirements.
     Do NOT write implementation code. Do NOT modify existing DB schemas."
  ...

User fills constitution.md as before.

Day 1 — Requirements (30-60 min)
──────────────────────────────────────────────────────
  Developer switches to "SDD: Business Analyst" mode in Roo Code.

  Roo Code (sdd-ba mode):
    → MCP: get_next_task()          → { task_id: "define-requirements", agent: "ba" }
    → MCP: get_constitution()       → full constitution.md content
    → Conversation with user: clarifying questions about invoicing
    → Write: .ai-sdd/outputs/requirements.md
    → MCP: complete_task("define-requirements",
                         "requirements.md",
                         <content>)

  Engine (invisible):
    T013: validates requirements.md structure ✓
    T016: manifest updated in constitution.md
    T005: HIL gate created → MCP server returns HIL item on next poll

  Developer sees HIL prompt in Roo Code:
    get_hil_queue() returns:
      { id: "hil-001", task_id: "define-requirements",
        trigger: "requires_human", context: "requirements.md produced" }
    Developer calls: resolve_hil_item("hil-001")

Day 1 — Architecture (60-90 min)
──────────────────────────────────────────────────────
  Developer switches to "SDD: Architect" mode.

  Roo Code (sdd-architect mode):
    → MCP: get_next_task()          → { task_id: "design-l1", agent: "architect" }
    → MCP: get_constitution()       → constitution.md with updated manifest
      (manifest shows requirements.md = COMPLETED with path)
    → Read: .ai-sdd/outputs/requirements.md   (native Read tool)
    → Produces design/l1.md
    → MCP: complete_task("design-l1", "design/l1.md", <content>)

  Mode restriction enforced: sdd-architect mode prevents Roo Code from
  generating implementation code even if the developer accidentally asks.

Day 2 onwards: same pattern — switch mode, get_next_task, execute, complete_task
```

### Roo Code — Brownfield (Adding Feature to Existing Codebase)

```
PROJECT: Add multi-currency support to existing invoice service (50k LOC)

Setup (10 min)
──────────────────────────────────────────────────────
  $ ai-sdd init --tool roo_code --project ./existing-invoice-service
  $ ai-sdd serve --mcp &

  constitution.md filled with existing codebase context (see Claude Code brownfield).
  Serena MCP also running: enables sdd-pe to navigate existing code.

Developer switches to "SDD: Principal Engineer" mode.
(Skipping BA + L1 because requirements and high-level arch are known.)

  Roo Code (sdd-pe mode):
    → MCP: get_constitution()
      (sees existing architecture in Background section)
    → Serena: get_symbols_overview("src/invoices/")
      → returns compact tree of Invoice class + its methods
    → Serena: find_symbol("Invoice", include_body=True)
      → returns Invoice ORM model definition
    → Serena: find_referencing_symbols("Invoice", "src/invoices/models.py")
      → finds all code that uses Invoice

  Roo Code uses existing code symbols — no need to read entire files.
  Produces precise impact analysis grounded in the actual codebase.

  → MCP: complete_task("design-l2", "design/l2.md", <content>)

  T006 Evidence Gate T2: HIL required.
  get_hil_queue() returns the HIL item with full design/l2.md context.
  Tech lead reviews, calls: resolve_hil_item("hil-002", notes="Approved")

  Developer switches to "SDD: Developer" mode.
  sdd-dev: reads implementation tasks → writes code → MCP complete_task()
  sdd-reviewer: reviews code → GO/NO_GO against constitution Standards
```

---

## 5. OpenAI / Codex — How It Works

Two distinct integration paths:

```
Path A: codex CLI (interactive, in terminal)
──────────────────────────────────────────────────────
  codex reads AGENTS.md from project root (native project instructions)
  Developer runs 'codex' in terminal → reads AGENTS.md → SDD agent persona active
  codex uses shell tools to call 'ai-sdd' CLI and read/write artifacts

Path B: OpenAI API / OpenAIAdapter (programmatic, CI/batch)
──────────────────────────────────────────────────────
  ai-sdd engine dispatches tasks via Chat Completions API
  Agent persona injected as system message (from agent YAML)
  OpenAI function calling captures structured task output
  Suitable for: CI pipelines, batch processing, multi-model agent teams
```

### OpenAI/Codex — Greenfield (New SaaS Product)

#### Path A: codex CLI (interactive)

```
PROJECT: Invoice tracking SaaS for freelancers

Day 0 — Setup (5 min)
──────────────────────────────────────────────────────
  $ ai-sdd init --tool openai --project ./invoice-saas

Creates:
  AGENTS.md                              ← codex CLI reads this natively
  .ai-sdd/                               ← config + workflow

AGENTS.md content:
  ## Project Methodology
  This project uses ai-sdd for Specification-Driven Development.

  ## How to Work
  - Run `ai-sdd status` to find the next task.
  - Read constitution.md for project context and artifact locations.
  - Use shell tools to read inputs, write outputs.
  - Run `ai-sdd run --task <id>` to advance the workflow.

  ## SDD Rules
  - Write acceptance criteria in Gherkin format.
  - Justify architectural decisions.
  - Stay within your assigned agent role.

Day 1 — Requirements (30-60 min)
──────────────────────────────────────────────────────
  $ codex

  codex reads AGENTS.md automatically.
  Developer: "Start the SDD workflow for this project"

  codex:
    → shell: ai-sdd status --json        (finds define-requirements READY)
    → shell: cat constitution.md         (reads project context)
    → Conversation: requirements questions
    → shell: cat > .ai-sdd/outputs/requirements.md << EOF ... EOF
    → shell: ai-sdd run --task define-requirements

  T013, T016, T005 fire invisibly (same as other tools).

Day 1 — Architecture
──────────────────────────────────────────────────────
  Developer: "Now do the architecture task"
  codex:
    → shell: ai-sdd status --json        (design-l1 is READY)
    → shell: cat constitution.md         (reads manifest, sees requirements.md = COMPLETED)
    → shell: cat .ai-sdd/outputs/requirements.md
    → produces design/l1.md content
    → shell: ai-sdd run --task design-l1
```

#### Path B: OpenAI API / OpenAIAdapter (CI/batch)

```
PROJECT: Automated specification pipeline in CI

config:
  .ai-sdd/ai-sdd.yaml:
    adapter:
      type: openai
      model: gpt-4o

  Each agent can use a different model:
    .ai-sdd/agents/architect.yaml:
      llm:
        provider: openai
        model: o1-preview    ← reasoning model for architecture

CI pipeline (.github/workflows/sdd.yml):
  steps:
    - run: ai-sdd run --workflow .ai-sdd/workflows/feature-spec.yaml

  Engine:
    → OpenAIAdapter.dispatch(task, context, idempotency_key)
    → system_message: agent persona from agent YAML
    → user_message: task description + constitution (includes manifest)
    → tools: [write_task_output, get_workflow_status]
    → model calls write_task_output() → artifact saved
    → T013 validates, T016 updates manifest, T005 HIL if needed

  HIL in CI: pause + write to file queue → human resolves via:
    $ ai-sdd hil list
    $ ai-sdd hil resolve hil-001
    → CI pipeline polls until resolved, then continues
```

### OpenAI/Codex — Brownfield (Adding Feature to Existing Codebase)

```
PROJECT: Multi-currency feature on existing codebase
TEAM: Uses both OpenAI API (for spec pipeline) and codex CLI (for interactive review)

Setup
──────────────────────────────────────────────────────
  $ ai-sdd init --tool openai --project ./existing-invoice-service

  constitution.md with existing codebase context (same as other tools).

  # Hybrid approach: spec pipeline in CI (OpenAI API), interactive review with codex CLI
  .ai-sdd/ai-sdd.yaml:
    adapter:
      type: openai
    agents:
      directory: .ai-sdd/agents/
    # PE agent uses o1-preview for deeper reasoning on brownfield design
    # Dev agent uses gpt-4o for faster code generation

Spec pipeline (CI — Path B):
──────────────────────────────────────────────────────
  $ ai-sdd run --task design-l2

  OpenAIAdapter dispatches sdd-pe task with:
    system: "You are the Principal Engineer. You are working on an existing
             FastAPI/PostgreSQL service. Do NOT modify existing tables."
    user: "Task: design L2 component spec for multi-currency support.
           Context: [constitution.md content including existing arch]
           Note: existing Invoice model is at .ai-sdd/outputs/invoice-model-summary.md
                 (generated in constitution from earlier Serena snapshot)"

  O1-preview model produces thorough L2 design with impact analysis.
  T006 T2 Evidence Gate: pauses for human sign-off.
  $ ai-sdd hil list → shows design review pending
  $ ai-sdd hil resolve hil-001

Interactive clarification (codex CLI — Path A):
──────────────────────────────────────────────────────
  For tasks where interactive dialogue is needed (e.g., requirements clarification):
  $ codex
  Developer: "Review the L2 design for the currency feature"
  codex reads AGENTS.md → acts as sdd-reviewer
  → shell: cat .ai-sdd/outputs/design/l2.md
  → provides GO/NO_GO feedback inline in terminal
  → shell: ai-sdd run --task review-l2
```

---

## 6. Comparison: Claude Code vs. Roo Code vs. OpenAI/Codex

| Dimension | Claude Code | Roo Code | OpenAI/Codex |
|---|---|---|---|
| **Primary interaction** | `/sdd-run` slash command in chat | Mode switcher + MCP tools | `codex` CLI terminal or API call |
| **Agent persona** | CLAUDE.md instructions | `.roomodes` definitions | AGENTS.md (CLI) or system message (API) |
| **Role enforcement** | Instructional (CLAUDE.md steers) | Structural (.roomodes restricts tools/behavior) | Instructional (AGENTS.md/system message) |
| **Workflow state access** | Bash tool → `ai-sdd` CLI | MCP tools (real-time) | Bash tool → CLI (CLI path) or adapter polls (API path) |
| **HIL resolution** | `/sdd-hil` slash command in session | `resolve_hil_item()` MCP tool | `ai-sdd hil resolve` in terminal or CI |
| **Codebase navigation (brownfield)** | Read/Grep/Bash tools | Serena MCP + Roo Code's built-in tools | Shell tools (CLI) or injected summaries (API) |
| **Best for** | Interactive solo/team development | Teams wanting strict role enforcement + real-time state | CI pipelines, batch processing, multi-model teams |
| **Headless/CI path** | `ClaudeCodeAdapter` subprocess | CLI (`ai-sdd run`) + file-based HIL | `OpenAIAdapter` (native) |
| **Multi-model agents** | Configurable per agent YAML | Configurable per mode | Native — each agent can use different model |

---

## 7. Where T012–T017 Surface Across All Tools

| Task | Claude Code | Roo Code | OpenAI/Codex |
|---|---|---|---|
| **T012** Expression DSL | `ai-sdd validate-config` at startup catches bad exit conditions | MCP `get_workflow_status()` returns parse error | `ai-sdd run` fails fast before first API call |
| **T013** Artifact Contract | Session pauses: "requirements.md missing section" before `/sdd-run` continues | `complete_task()` rejects incomplete artifact | `OpenAIAdapter` task marked FAILED with specific reason; retried with corrected prompt |
| **T014** Overlay Composition | Guarantees no infinite loop when Paired + Evidence Gate both on | Same guarantee via MCP-driven workflow | Same guarantee in API dispatch path |
| **T015** Adapter Reliability | `ClaudeCodeAdapter` retries 429 transparently; session shows "retrying..." | CLI retries propagate through MCP status | `OpenAIAdapter` retries with exponential backoff; CI job doesn't fail on transient errors |
| **T016** Constitution Manifest | After each task: Read constitution.md and the manifest is already updated | `get_constitution()` MCP always returns current manifest | API: constitution (with manifest) passed in system message; agent pulls only what it needs |
| **T017** Security | Confluence export with injection → session shows HIL warning | `get_constitution()` returns sanitized content; injection → HIL item appears in queue | Input sanitized before injected into system/user message; injection → FAILED with reason |

---

## 8. Summary: Two Mental Models

**Developer mental model (what they work with):**
```
Write    → constitution.md (project context + rules)
Config   → ai-sdd.yaml (overlays, adapter, thresholds)
Run      → /sdd-run (Claude Code) | mode switch + MCP (Roo Code) | codex CLI or ai-sdd run (OpenAI)
Review   → HIL gates at each design layer
Inspect  → constitution.md manifest + ai-sdd status --metrics
```

**Framework mental model (what runs underneath — same regardless of tool):**
```
T001–T004 : Parse and execute the workflow DAG
T003+T016 : Keep constitution current (agents pull what they need)
T005–T009 : Quality gates and review loops
T010      : Every CLI command + ai-sdd init for tool setup
T011      : Every event logged with run_id and cost
T012      : Every exit_condition evaluated safely (no eval())
T013      : Every task output validated before handover
T014      : Every overlay combination guaranteed by CI
T015      : Every adapter failure handled consistently
T017      : Every input scanned; every output scrubbed
T018–T020 : Tool-native surface for each coding tool
```

The framework core (T001–T017) is **tool-agnostic**. T018/T019/T020 are thin adapters that
map each tool's native capabilities to the same underlying engine. A project can switch from
Claude Code to Roo Code by running `ai-sdd init --tool roo_code` — the workflow, constitution,
artifacts, and state all stay the same.
