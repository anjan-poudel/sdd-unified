# Architecture Correction: Pure Configuration Model

**Date:** 2025-10-16  
**Status:** Critical Correction  

## The Fundamental Insight

**Previous Misunderstanding:** I designed an `orchestrator.py` script as an execution engine.

**Correct Architecture:** The framework should be **pure configuration** with minimal/no script dependencies. Claude Code executes workflow.json natively.

## What the Framework Should Be

### ✅ Configuration Files Only

The framework is a collection of declarative configuration files that Claude Code interprets and executes.

```
sdd-unified/
├── agents/configs/          # Agent persona definitions
│   ├── sdd-ba.yaml
│   ├── sdd-architect.yaml
│   ├── sdd-pe.yaml
│   ├── sdd-le.yaml
│   └── sdd-coder.yaml
│
├── commands/                # Task prompt templates  
│   ├── ba/define-requirements.yaml
│   ├── architect/design-l1.yaml
│   ├── pe/design-l2.yaml
│   ├── le/design-l3.yaml
│   └── coder/execute-task.yaml
│
├── templates/               # Workflow templates
│   ├── workflow.json.template
│   └── context.json.template
│
└── commands/slash/          # Slash command definitions
    └── feature.yaml
```

**Total code:** ~0 lines of Python/JavaScript  
**Total config:** ~20 YAML files  

### ❌ What Should Be Removed

```
sdd-unified/orchestrator/main.py       ← DELETE
sdd-unified/orchestrator/status.py     ← DELETE  
sdd-unified/requirements.txt           ← DELETE
sdd-unified/scripts/install_*.sh       ← SIMPLIFY (just copy configs)
```

**Why:** Claude Code handles all execution logic. We provide the configuration it interprets.

## Corrected Execution Model

### When User Types: `/feature "create auth API"`

**Claude Code Does:**
1. Recognizes `/feature` slash command from `commands/slash/feature.yaml`
2. Initializes feature workspace
3. Copies `workflow.json.template` → `features/auth-api/workflow.json`
4. **Natively parses workflow.json as a DAG**
5. Executes tasks in dependency order:
   - For each ready task, switches to the specified agent
   - Loads the command YAML as the prompt
   - Executes with agent's persona
   - Updates workflow.json status
6. Handles review loops automatically based on outcome files

**sdd-unified Provides:**
- workflow.json structure
- Agent configuration YAMLs
- Command prompt templates
- Documentation

**No scripts run. No Python executed. Pure configuration.**

## Simplified Installation

### Old (Wrong):
```bash
# 142 lines of bash installing Python, venv, pip packages...
python3 -m venv venv
source venv/bin/activate
pip3 install requirements.txt
# Creating shell aliases...
```

### New (Correct):
```bash
#!/bin/bash
# Copy agent configs to Claude Code
cp sdd-unified/agents/configs/*.yaml ~/.claude-code/agents/

# Copy slash commands
cp sdd-unified/commands/slash/*.yaml ~/.claude-code/commands/

# Done.
echo "Installation complete. Restart Claude Code."
```

**3 operations. No dependencies. No code execution.**

## Implications

### What This Means for Assessment

**Previous "Weaknesses" That Are Now Invalid:**

1. ❌ "No AI Integration" - **Invalid:** Claude Code provides this
2. ❌ "No Orchestrator" - **Invalid:** Claude Code IS the orchestrator  
3. ❌ "No State Persistence" - **Invalid:** Claude Code handles state
4. ❌ "Synchronous Architecture" - **Invalid:** Not our concern

**Actual Weaknesses:**

1. ⚠️ **Dependency on Claude Code Capabilities**
   - If Claude Code can't parse workflow.json as DAG, framework fails
   - If it can't load external agent configs, framework fails
   - Single point of dependency

2. ⚠️ **Limited Portability**
   - Designed specifically for Claude Code's model
   - May not work with other agentic tools without adaptation
   - Vendor-specific

3. ⚠️ **Assumption Risk**
   - Everything relies on Claude Code working exactly as we expect
   - No fallback if assumptions are wrong
   - High validation priority

## Revised Framework Value

### What We're Actually Building

**Not:** An AI development platform  
**Is:** A sophisticated SDD workflow definition standard for agentic coding tools

**Analogies:**
- Like OpenAPI spec (not Swagger Codegen - that's the runtime)
- Like Docker Compose files (not Docker Engine)
- Like Kubernetes manifests (not the Kubelet)

### Value Proposition (Corrected)

1. **Standardized Workflow Format**
   - Any tool that can parse workflow.json can execute SDD
   - Workflow becomes portable configuration
   - Version control friendly

2. **Optimized Agent Personas**
   - Pre-configured roles for SDD
   - Tested prompt engineering
   - Drop-in agent definitions

3. **Quality Gate Architecture**
   - Formal review structure
   - Iterative refinement loops
   - Circuit breaker safety

4. **Task-Level Verifiability**
   - BDD acceptance criteria
   - Discrete implementation units
   - Clear success conditions

## What Needs to Be Validated

**Critical Assumption Testing:**

1. Can Claude Code execute a workflow.json DAG?
2. Can it load agent configs from YAML files?
3. Can it switch agents mid-workflow?
4. Can agents read/write shared files (context.json)?
5. Does it support conditional logic (if review REJECTED, do rework)?

**Action Required:** Build proof-of-concept to validate each assumption.

**If All YES:** Framework is essentially ready  
**If Any NO:** Need to adapt or build minimal orchestration layer

## Revised Recommendations

### Immediate Priority

**Week 1: Validate with Claude Code**
```
1. Install Claude Code
2. Create ONE agent config (sdd-ba)
3. Create ONE command (define-requirements.yaml)
4. Test if Claude Code can:
   - Load the agent
   - Execute the command
   - Write to spec/spec.yaml
5. Document findings
```

**Week 2: Test Workflow Execution**
```
1. Create minimal workflow.json (2-3 tasks)
2. Test if Claude Code can:
   - Parse the DAG
   - Execute tasks in order
   - Switch between agents
3. Document how it actually works
```

### If Assumptions Validate

**Framework is 90% ready:**
- Remove orchestrator.py
- Simplify installation scripts
- Test with complete workflow
- Document Claude Code requirements
- Ship version 1.0

**Estimated time:** 2-4 weeks

### If Assumptions Fail

**Need Orchestration Layer:**
- Keep minimal orchestrator.py
- It calls Claude Code CLI for each task
- Acts as DAG execution engine
- More complex but still feasible

**Estimated time:** 2-3 months

## Final Corrected Assessment

### Framework Quality (As Configuration)

| Aspect | Rating | Notes |
|--------|--------|-------|
| **Workflow Spec** | 9/10 | Excellent DAG structure |
| **Agent Definitions** | 8/10 | Well-designed personas |
| **Prompt Quality** | 8/10 | Good command templates |
| **Documentation** | 9/10 | Comprehensive |
| **Simplicity** | 7/10 | Could be simpler, but good |
| **Integration Risk** | 6/10 | Unvalidated assumptions |

**Overall: 7.8/10** - High-quality configuration-driven framework with integration validation needed

### Competitive Position (Corrected)

**Compared to:** Other SDD workflow configurations

**Strengths:**
- More sophisticated than simple sequential scripts
- Better role separation than generic prompting
- Formal quality gates vs ad-hoc reviews
- Portable configuration vs hardcoded logic

**Weaknesses:**
- Untested with actual Claude Code
- Assumes specific runtime capabilities
- More complex than needed for simple features

### Bottom Line

**This is a well-designed workflow orchestration configuration.**

**The critical unknown:** Does Claude Code natively support DAG execution from JSON?

**If YES:** This framework is production-ready as pure config  
**If NO:** Need minimal orchestration layer, but still viable

**Action:** Validate assumptions THIS WEEK with real testing.