# SDD Unified Framework

**Version:** 1.0.0-alpha  
**Status:** Design Complete, Validation Needed  
**Last Updated:** 2025-10-16

> A configuration-driven orchestration system for specification-driven development (SDD) using agentic AI tools.

## What is sdd_unified?

sdd_unified is a **steering configuration layer** that makes agentic coding tools (like Claude Code or Roo Code) follow rigorous specification-driven development methodology.

**Think of it as:**
- Agentic Tool (Claude Code) = Capable but undisciplined developer
- sdd_unified = Rigorous development process they must follow

**Result:** Deterministic, verifiable, specification-driven development instead of ad-hoc code generation.

## Quick Start

```bash
# 1. Copy configuration files
cp -r sdd_unified/.sdd_unified /your/project/

# 2. Register agents in Claude Code
# See docs/3_integration/claude_code.md

# 3. Start a feature
/feature "Create user authentication API"

# 4. Watch the structured workflow execute
```

**See:** [Quick Start Guide](docs/1_getting_started/quick_start.md) for detailed instructions.

## Key Features

### 🎯 Structured Workflow (DAG-Based)
- Directed Acyclic Graph defines task dependencies
- Automatic agent switching
- Parallel execution where possible
- Complete audit trail

### 👥 Five Specialized Agents
- **sdd-ba:** Business requirements and specifications
- **sdd-architect:** High-level system architecture
- **sdd-pe:** Detailed component design
- **sdd-le:** Implementation task planning
- **sdd-coder:** Code execution

### ✅ Task-Driven BDD Implementation
- Discrete implementation tasks (not monolithic plans)
- Gherkin acceptance criteria for every task
- Verifiable, testable outcomes
- Granular progress tracking

### 🔄 Iterative Review Cycles
- Formal review at every design layer
- Automatic rework when reviews reject
- Circuit breakers prevent infinite loops
- Human intervention when needed

### 📋 Context Management
- context.json manifest for agent handover
- Decision tracking with rationale
- Iteration counting
- Complete review history

## Architecture

```
User Request
     ↓
/feature command
     ↓
┌─────────────────────────────────┐
│  Claude Code (Execution)         │
│  - Reads workflow.json           │
│  - Switches agents               │
│  - Calls LLMs                    │
│  - Manages state                 │
└─────────────┬───────────────────┘
              ↓ consults
┌─────────────────────────────────┐
│  sdd_unified (Configuration)     │
│  - workflow.json (structure)     │
│  - agents/*.yaml (personas)      │
│  - commands/*.yaml (prompts)     │
│  - context.json (state schema)   │
└─────────────────────────────────┘
```

**See:** [Architecture Overview](docs/2_architecture/overview.md) for details.

## Documentation

### 📚 Complete Documentation Index
**Start here:** [Documentation Index](docs/INDEX.md)

### Quick Links

**Getting Started:**
- [Quick Start Guide](docs/1_getting_started/quick_start.md) - 5 minute setup
- [Feature Development Workflow](docs/1_getting_started/feature_development_workflow.md) - End-to-end guide
- [Claude Code Integration](docs/3_integration/claude_code.md) - Installation

**Understanding the Framework:**
- [Architecture Overview](docs/2_architecture/overview.md) - What is sdd_unified?
- [Workflow Engine](docs/2_architecture/workflow_engine.md) - DAG execution
- [Task-Driven Implementation](docs/2_architecture/task_driven_implementation.md) - BDD tasks
- [Iterative Reviews](docs/2_architecture/iterative_reviews.md) - Review cycles
- [Context Management](docs/2_architecture/context_management.md) - Agent handover

**Evaluation & Analysis:**
- [Framework Assessment](docs/6_analysis/framework_assessment.md) - Honest evaluation
- [Competitive Analysis](docs/6_analysis/competitive_analysis.md) - vs other frameworks

### Documentation Organization

```
docs/
├── README.md              # This index
├── INDEX.md               # Complete navigation guide
├── 1_getting_started/     # New user guides
├── 2_architecture/        # How it works
├── 3_integration/         # Claude Code, Roo Code setup
├── 4_guides/              # Practical usage
├── 5_reference/           # Technical specs
└── 6_analysis/            # Evaluation & comparison
```

## Project Structure

```
sdd_unified/
├── README.md                    # This file
├── ARCHITECTURE.md              # High-level design
├── PLAYBOOK.md                  # Operational guide
├── agents/
│   ├── configs/                 # Agent registration (Claude Code)
│   └── roles/                   # Agent persona definitions
├── commands/
│   ├── ba/                      # Business analyst commands
│   ├── architect/               # Architect commands
│   ├── pe/                      # Principal engineer commands
│   ├── le/                      # Lead engineer commands
│   ├── coder/                   # Implementation commands
│   └── feature/                 # Feature initialization
├── templates/
│   └── workflow.json.template   # Workflow DAG definition
├── spec/
│   └── spec.yaml                # Feature specification schema
├── docs/                        # Comprehensive documentation
└── use_cases/
    └── examples/                # Complete workflow examples
```

## Example Workflow

### User Request
```
/feature "Create user authentication API"
```

### Automated Execution
```
1. sdd-ba        → requirements.md, spec.yaml
2. sdd-architect → l1_architecture.md
3. Reviews       → BA, PE, LE validate L1
4. (if rejected) → design-l1-rework (max 3 iterations)
5. sdd-pe        → l2_component_design.md
6. Reviews       → Architect, LE validate L2
7. sdd-le        → tasks/task-001.md, task-002.md, ...
8. Review        → PE validates task breakdown
9. sdd-coder     → Implements task-001, task-002, ... (parallel)
10. Reviews      → LE validates each task
11. (if needed)  → Task rework (max 2 iterations)
12. Done         → Complete, reviewed code
```

**See:** [Feature Development Workflow](docs/1_getting_started/feature_development_workflow.md)

## Current Status

### ✅ Complete
- Comprehensive workflow architecture (DAG-based)
- Five specialized agent definitions
- Task-driven BDD implementation design
- Formal iterative review system
- Context management for agent handover
- Complete documentation (60+ pages)

### ⚠️ Needs Validation
- Claude Code can execute workflow.json as DAG
- Agent switching with context preservation
- Conditional branching based on review outcomes
- Parallel task execution
- State persistence mechanisms

### 🚧 In Progress
- End-to-end testing with real projects
- BDD validation mechanism
- "Lite" workflow templates for simple features
- Error recovery procedures

**Grade:** B+ (8.5/10) - Excellent design, needs validation

**See:** [Framework Assessment](docs/6_analysis/framework_assessment.md) for detailed evaluation.

## Comparison to Alternatives

| Framework | Type | Strengths | Limitations |
|-----------|------|-----------|-------------|
| **sdd_unified** | Config orchestration | DAG workflow, formal reviews, BDD tasks | Unvalidated |
| spec-kit | Template library | Good templates | No orchestration |
| BMAD | Process methodology | Business alignment | No automation |
| a-sdd-starter | Shell scripts | Works today | Imperative, not declarative |
| AgentOS | Platform | Flexible | Requires coding |
| LangChain | LLM framework | Mature ecosystem | Not SDD-specific |

**See:** [Competitive Analysis](docs/6_analysis/competitive_analysis.md) for full comparison.

## Installation

### Prerequisites
- Claude Code or Roo Code installed
- Basic understanding of YAML and JSON

### Quick Install

```bash
# 1. Clone or download sdd_unified
git clone https://github.com/your-org/sdd_unified.git

# 2. Copy to your project
cd /your/project
cp -r /path/to/sdd_unified/.sdd_unified .

# 3. Register agents in Claude Code
# (See integration guide for your specific tool)

# 4. Verify setup
# Check that all 5 agents appear in Claude Code
```

**See:** [Claude Code Integration](docs/3_integration/claude_code.md) for detailed setup.

## Usage

### Start a New Feature

**Method 1: Slash Command**
```
/feature "User authentication API"
```

**Method 2: Manual**
```bash
mkdir -p features/feature-001-auth/{spec,design,implementation,review}
cp .sdd_unified/templates/workflow.json.template features/feature-001-auth/workflow.json
# Then follow workflow manually
```

### Monitor Progress

```
/sdd-status
```

Shows:
- Current phase
- Completed tasks
- Active agent
- Iteration counts
- Next steps

## Key Concepts

### Workflow DAG
Directed Acyclic Graph defines task dependencies and execution order.

### Five Agents
Specialized sub-agents with focused responsibilities (BA, Architect, PE, LE, Coder).

### Three Design Layers
- **L1:** High-level architecture
- **L2:** Component specifications
- **L3:** Implementation tasks

### BDD Tasks
Every implementation task has Gherkin acceptance criteria (Given/When/Then).

### Iterative Reviews
Formal review at each layer with automatic rework and circuit breakers.

### Context Management
context.json manifest carries state and handover notes between agents.

## Contributing

Contributions welcome! Areas needing help:

1. **Validation Testing** - Test with Claude Code/Roo Code
2. **Lite Workflows** - Simpler templates for common cases
3. **BDD Validation** - Mechanism to verify Gherkin criteria
4. **Examples** - More complete workflow examples
5. **Integration Guides** - For other agentic tools

**See:** [Enhancement Proposal](docs/6_analysis/enhancement_proposal.md)

## Known Limitations

1. **Unvalidated Integration** - Core assumptions not tested with Claude Code
2. **Complexity Overhead** - Full workflow heavy for simple tasks
3. **No Validation Mechanism** - BDD criteria defined but not executed
4. **Tool-Specific** - Designed for Claude Code specifically
5. **Context Loading** - Mechanism underspecified

**See:** [Framework Assessment](docs/6_analysis/framework_assessment.md#weaknesses)

## Roadmap

### Phase 1: Validation (Weeks 1-2)
- ✅ Design complete
- 🚧 Validate with Claude Code
- 🚧 Test basic workflow
- 🚧 Document actual behavior

### Phase 2: Simplification (Weeks 3-4)
- Create lite workflow templates
- Remove unnecessary complexity
- Improve error handling

### Phase 3: Enhancement (Months 2-3)
- Add BDD validation mechanism
- Support multiple tools
- Build example library
- Community feedback

## Support

- **Documentation:** [docs/](docs/) directory
- **Examples:** [use_cases/examples/](use_cases/examples/)
- **Issues:** GitHub issues
- **Discussions:** GitHub discussions

## License

[License Type] - See LICENSE file

## Credits

Built by the sdd_unified team with inspiration from:
- GitHub Actions (workflow DAG)
- spec-kit (SDD templates)
- a-sdd-starter (practical SDD)
- AgentOS (multi-agent systems)

## Summary

**sdd_unified provides:**
- ✅ Rigorous SDD methodology for AI agents
- ✅ Declarative configuration (YAML/JSON)
- ✅ Sophisticated quality gates (reviews + circuit breakers)
- ✅ Task-level BDD verification
- ⚠️ Needs validation with real tools

**Next step:** Validate assumptions with Claude Code  
**Timeline:** 2-4 weeks to production (if validation succeeds)  
**Status:** Well-designed, needs proof it works

---

**Version:** 1.0.0-alpha  
**Last Updated:** 2025-10-16  
**Documentation:** [docs/INDEX.md](docs/INDEX.md)