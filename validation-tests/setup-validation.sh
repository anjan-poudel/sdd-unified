#!/bin/bash
# SDD Unified Framework - Validation Setup Script
#
# This script prepares your environment for validation testing.
# Run this before starting Phase 1.

set -e  # Exit on error

echo "============================================"
echo "SDD Unified Framework - Validation Setup"
echo "============================================"
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [ ! -f "VALIDATION_MASTER_PLAN.md" ]; then
    echo -e "${RED}ERROR: Run this script from sdd-unified/validation-tests/${NC}"
    exit 1
fi

echo "Step 1: Checking Prerequisites..."
echo ""

# Check for Claude Code
if command -v claude-code &> /dev/null; then
    echo -e "${GREEN}✓${NC} Claude Code found"
else
    echo -e "${YELLOW}⚠${NC} Claude Code not found in PATH"
    echo "  Install from: https://claude.ai/code"
    echo "  Or: You can still prepare the test environment"
    echo ""
fi

# Check for Python (for JSON validation)
if command -v python3 &> /dev/null; then
    echo -e "${GREEN}✓${NC} Python 3 found"
else
    echo -e "${YELLOW}⚠${NC} Python 3 not found (needed for JSON validation)"
fi

echo ""
echo "Step 2: Creating Claude Code directories..."
echo ""

# Create Claude Code config directories if they don't exist
mkdir -p ~/.claude-code/agents
mkdir -p ~/.claude-code/commands

echo -e "${GREEN}✓${NC} Created ~/.claude-code/agents"
echo -e "${GREEN}✓${NC} Created ~/.claude-code/commands"

echo ""
echo "Step 3: Preparing Phase 1 test files..."
echo ""

# Phase 1: Copy BA agent for initial test
if [ -f "../agents/configs/sdd-ba.yaml" ]; then
    cp ../agents/configs/sdd-ba.yaml phase1-agent-loading/sdd-ba.yaml
    echo -e "${GREEN}✓${NC} Copied BA agent config to phase1-agent-loading/"
else
    echo -e "${RED}✗${NC} BA agent config not found at ../agents/configs/sdd-ba.yaml"
    exit 1
fi

# Copy define-requirements command
if [ -f "../commands/ba/define-requirements.yaml" ]; then
    cp ../commands/ba/define-requirements.yaml phase1-agent-loading/define-requirements.yaml
    echo -e "${GREEN}✓${NC} Copied define-requirements command to phase1-agent-loading/"
else
    echo -e "${YELLOW}⚠${NC} define-requirements command not found"
fi

echo ""
echo "Step 4: Preparing Phase 2 workflow template..."
echo ""

# Create Phase 2 minimal workflow
cat > phase2-workflow-execution/workflow.json << 'EOF'
{
  "init": {
    "command": "echo 'Feature workspace initialized'",
    "status": "COMPLETED",
    "dependencies": []
  },
  "define-requirements": {
    "command": "sdd-ba-define-requirements --task_id=define-requirements",
    "status": "PENDING",
    "dependencies": ["init"]
  },
  "design-l1": {
    "command": "sdd-architect-design-l1 --task_id=design-l1",
    "status": "PENDING",
    "dependencies": ["define-requirements"]
  }
}
EOF

echo -e "${GREEN}✓${NC} Created minimal workflow.json for Phase 2"

# Create directory structure for Phase 2
mkdir -p phase2-workflow-execution/{spec,design,review}
echo -e "${GREEN}✓${NC} Created Phase 2 directory structure"

echo ""
echo "Step 5: Preparing Phase 3 complete test..."
echo ""

# Copy full workflow template for Phase 3
if [ -f "../templates/workflow.json.template" ]; then
    cp ../templates/workflow.json.template phase3-end-to-end/workflow.json
    echo -e "${GREEN}✓${NC} Copied complete workflow template to Phase 3"
else
    echo -e "${YELLOW}⚠${NC} workflow.json.template not found"
fi

# Copy FSM use case
if [ -f "../use_cases/FSM_PARALLEL_WORKFLOW_ENGINE.md" ]; then
    cp ../use_cases/FSM_PARALLEL_WORKFLOW_ENGINE.md phase3-end-to-end/requirements_input.md
    echo -e "${GREEN}✓${NC} Copied FSM use case to Phase 3"
else
    echo -e "${YELLOW}⚠${NC} FSM use case not found"
fi

# Create Phase 3 directory structure
mkdir -p phase3-end-to-end/{spec,design,design/l3_tasks,implementation,review}
echo -e "${GREEN}✓${NC} Created Phase 3 directory structure"

# Create context.json for Phase 3
cat > phase3-end-to-end/context.json << 'EOF'
{
  "feature_name": "FSM Parallel Workflow Engine",
  "feature_id": "phase3-validation",
  "current_phase": "requirements",
  "iteration_count": {
    "requirements": 0,
    "design_l1": 0,
    "design_l2": 0,
    "design_l3": 0,
    "implementation": 0
  },
  "decisions": [],
  "handover_notes": ""
}
EOF

echo -e "${GREEN}✓${NC} Created context.json for Phase 3"

echo ""
echo "============================================"
echo "Setup Complete!"
echo "============================================"
echo ""
echo "Next Steps:"
echo ""
echo "1. Read the master plan:"
echo "   cat VALIDATION_MASTER_PLAN.md"
echo ""
echo "2. Start Phase 1 (30-60 minutes):"
echo "   cd phase1-agent-loading"
echo "   cat README.md"
echo ""
echo "3. Follow each phase in sequence:"
echo "   Phase 1 → Phase 2 → Phase 3"
echo ""
echo "4. Document findings in each README.md"
echo ""
echo "5. Create final report after Phase 3"
echo ""
echo -e "${YELLOW}IMPORTANT:${NC} You must install agents/commands into Claude Code"
echo "during Phase 1. This script only prepares test files."
echo ""
echo "Good luck with validation!"
echo ""
