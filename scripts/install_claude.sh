#!/bin/bash

# Installation script for SDD Unified Framework with Claude Code
# Properly registers agents and slash commands

set -e  # Exit on error

echo "=========================================="
echo "SDD Unified Framework - Claude Code Setup"
echo "=========================================="
echo ""

# Parse arguments
SCOPE="local"
while [[ $# -gt 0 ]]; do
  case $1 in
    --scope=*)
      SCOPE="${1#*=}"
      shift
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT"

echo "Installation scope: $SCOPE"
echo ""

# 1. Check dependencies
echo "Checking dependencies..."
command -v python3 >/dev/null 2>&1 || { echo "ERROR: Python 3 is required"; exit 1; }
command -v pip3 >/dev/null 2>&1 || { echo "ERROR: pip3 is required"; exit 1; }
echo "✓ Dependencies found"
echo ""

# 2. Set up Python virtual environment
echo "Setting up Python environment..."
if [ -d "venv" ]; then
    echo "✓ Virtual environment already exists"
else
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

source venv/bin/activate
pip3 install -r requirements.txt > /dev/null 2>&1
echo "✓ Python dependencies installed"
echo ""

# 3. Determine Claude Code config directory
if [ "$SCOPE" = "global" ]; then
    CLAUDE_CONFIG_DIR="$HOME/.claude-code"
else
    CLAUDE_CONFIG_DIR=".claude-code"
fi

echo "Claude Code config directory: $CLAUDE_CONFIG_DIR"
mkdir -p "$CLAUDE_CONFIG_DIR/agents" "$CLAUDE_CONFIG_DIR/commands"

# 4. Register agents
echo ""
echo "Registering SDD agents with Claude Code..."
AGENTS=("sdd-ba" "sdd-architect" "sdd-pe" "sdd-le" "sdd-coder")

for agent in "${AGENTS[@]}"; do
    cp "$REPO_ROOT/agents/configs/${agent}.yaml" "$CLAUDE_CONFIG_DIR/agents/"
    echo "✓ Registered agent: $agent"
done

# 5. Register slash commands
echo ""
echo "Registering slash commands..."
cp "$REPO_ROOT/commands/slash/"*.yaml "$CLAUDE_CONFIG_DIR/commands/"
echo "✓ Registered /feature command"
echo "✓ Registered /feature-status command"

# 6. Make orchestrator executable
chmod +x "$REPO_ROOT/orchestrator/main.py"
if [ -f "$REPO_ROOT/orchestrator/status.py" ]; then
    chmod +x "$REPO_ROOT/orchestrator/status.py"
fi
echo ""
echo "✓ Orchestrator configured"

# 7. Create quick-start helper
HELPER_FILE="$CLAUDE_CONFIG_DIR/sdd_quickstart.md"
cat > "$HELPER_FILE" << 'EOL'
# SDD Unified Framework Quick Start

## Available Slash Commands

### `/feature <description> [--mode=<mode>]`
Create and develop a complete feature autonomously.

**Modes:**
- `autonomous` (default): Fully automatic execution
- `supervised`: Pause at milestones for approval
- `manual`: Step-by-step execution

**Examples:**
```
/feature "Create user authentication API with JWT tokens"
/feature "Add password reset" --mode=supervised
/feature @specs/payment-integration.md
```

### `/feature-status [feature-name]`
Show the current workflow status and progress.

## Registered Agents

The framework uses 5 specialized agents:
- `sdd-ba`: Business Analyst (requirements, business validation)
- `sdd-architect`: System Architect (L1 architecture)
- `sdd-pe`: Principal Engineer (L2 component design, technical reviews)
- `sdd-le`: Lead Engineer (L3 task planning, code reviews)
- `sdd-coder`: Implementation Engineer (code execution)

The orchestrator switches between these agents automatically.

## Workflow

Before running `/feature` in a project, copy framework files into that project:
```bash
mkdir -p .sdd_unified
cp -R /path/to/sdd-unified/{agents,commands,templates,orchestrator,spec} .sdd_unified/
```

1. `/feature "your feature description"`
2. Orchestrator initializes workspace
3. Auto-executes: requirements → L1 → review → L2 → review → L3 → tasks → review
4. Each review that fails triggers automatic rework
5. Feature complete when all tasks approved
EOL

echo ""
echo "✓ Quick-start guide created at: $HELPER_FILE"

# 8. Final instructions
echo ""
echo "=========================================="
echo "Installation Complete!"
echo "=========================================="
echo ""
echo "To start using the framework in Claude Code:"
echo "1. Restart or reload your Claude Code environment"
echo "2. The agents and commands are now registered"
echo "3. Use /feature to start autonomous development"
echo ""
echo "Quick reference: cat $HELPER_FILE"
echo ""

deactivate
