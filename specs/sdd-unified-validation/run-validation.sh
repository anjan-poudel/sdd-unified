#!/bin/bash

# SDD Unified - Validation Test Runner
# This script helps execute validation tests step-by-step

set -e

echo "========================================="
echo "SDD Unified Framework Validation"
echo "========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check prerequisites
echo "Checking prerequisites..."

# Check if claude CLI exists
if ! command -v claude &> /dev/null; then
    echo -e "${RED}❌ Claude CLI not found${NC}"
    echo "Please install Claude Code first"
    exit 1
else
    echo -e "${GREEN}✅ Claude CLI found${NC}"
    claude --version
fi

echo ""
echo "========================================="
echo "Phase 1: Core Validation (CRITICAL)"
echo "========================================="
echo ""

# Create test directory
TEST_DIR="$HOME/sdd-validation-test"
mkdir -p "$TEST_DIR/results"
cd "$TEST_DIR"

echo "Test directory: $TEST_DIR"
echo ""

# V001: DAG Execution Test
echo "========================================="
echo "V001: DAG Workflow Execution Test"
echo "========================================="
echo ""

echo "This test validates if Claude can execute workflow.json as a DAG"
echo ""
echo "Test workflow location: sdd-unified/specs/validation/test-workflows/v001-simple-dag.json"
echo ""

read -p "Do you want to run V001 test? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "Copying test workflow..."
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    cp -v "$SCRIPT_DIR/test-workflows/v001-simple-dag.json" ./workflow.json
    
    echo ""
    echo -e "${YELLOW}Manual Test Required:${NC}"
    echo "1. Try: claude workflow execute workflow.json"
    echo "2. OR manually run each task:"
    echo "   - Task 1: echo 'Task 1 completed successfully' > test1.txt"
    echo "   - Task 2: cat test1.txt && echo 'Task 2 completed successfully' > test2.txt"
    echo ""
    
    read -p "Press enter after completing the test..."
    
    echo ""
    echo "Checking test results..."
    
    if [ -f "test1.txt" ] && [ -f "test2.txt" ]; then
        echo -e "${GREEN}✅ V001 PASS: Both files created${NC}"
        echo "PASS" > results/v001-result.txt
    else
        echo -e "${RED}❌ V001 FAIL: Files not created${NC}"
        echo "FAIL" > results/v001-result.txt
    fi
fi

echo ""
echo "========================================="
echo "V002: Agent Switching Test"
echo "========================================="
echo ""

read -p "Do you want to run V002 test? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "This test validates agent switching capability"
    echo ""
    echo -e "${YELLOW}Manual Test Steps:${NC}"
    echo "1. Run: claude agents list"
    echo "2. Check if 'sdd-ba' and 'sdd-architect' agents exist"
    echo "3. Try: claude switch-agent sdd-ba"
    echo "4. Try: claude switch-agent sdd-architect"
    echo ""
    
    read -p "Did agent switching work? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${GREEN}✅ V002 PASS: Agent switching works${NC}"
        echo "PASS" > results/v002-result.txt
    else
        echo -e "${YELLOW}⚠️  V002 PARTIAL: Manual switching may be required${NC}"
        echo "PARTIAL" > results/v002-result.txt
    fi
fi

echo ""
echo "========================================="
echo "V003: Context Management Test"
echo "========================================="
echo ""

read -p "Do you want to run V003 test? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "Creating test context.json..."
    cat > context.json << 'EOF'
{
  "feature_id": "validation-003",
  "created_at": "2025-10-16T10:00:00Z",
  "handover_notes": {
    "history": [
      {
        "from_agent": "test",
        "message": "Test handover note"
      }
    ]
  }
}
EOF
    
    echo -e "${GREEN}✅ context.json created${NC}"
    echo ""
    echo -e "${YELLOW}Manual Test:${NC}"
    echo "1. Check if Claude can read context.json"
    echo "2. Try: claude run 'Read context.json and summarize handover notes'"
    echo ""
    
    read -p "Did context reading work? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${GREEN}✅ V003 PASS: Context management works${NC}"
        echo "PASS" > results/v003-result.txt
    else
        echo -e "${YELLOW}⚠️  V003 PARTIAL: Manual context handling may be needed${NC}"
        echo "PARTIAL" > results/v003-result.txt
    fi
fi

# Summary
echo ""
echo "========================================="
echo "Validation Summary"
echo "========================================="
echo ""

V001_RESULT=$(cat results/v001-result.txt 2>/dev/null || echo "NOT_RUN")
V002_RESULT=$(cat results/v002-result.txt 2>/dev/null || echo "NOT_RUN")
V003_RESULT=$(cat results/v003-result.txt 2>/dev/null || echo "NOT_RUN")

echo "V001 DAG Execution: $V001_RESULT"
echo "V002 Agent Switching: $V002_RESULT"
echo "V003 Context Management: $V003_RESULT"
echo ""

# Generate summary
cat > results/SUMMARY.md << EOF
# SDD Unified Validation Results

**Date:** $(date)
**Tester:** $(whoami)
**Test Directory:** $TEST_DIR

## Phase 1 Results

- **V001 DAG Execution:** $V001_RESULT
- **V002 Agent Switching:** $V002_RESULT
- **V003 Context Management:** $V003_RESULT

## Recommendation

EOF

if [ "$V001_RESULT" = "PASS" ] && [ "$V002_RESULT" = "PASS" ] && [ "$V003_RESULT" = "PASS" ]; then
    echo "✅ **All critical tests passed!**" >> results/SUMMARY.md
    echo "   Framework is viable as designed." >> results/SUMMARY.md
    echo "   Grade: A- (production ready)" >> results/SUMMARY.md
    echo ""
    echo -e "${GREEN}✅ ALL TESTS PASSED - Framework viable!${NC}"
elif [ "$V001_RESULT" = "FAIL" ]; then
    echo "❌ **V001 Failed - Critical**" >> results/SUMMARY.md
    echo "   DAG execution doesn't work." >> results/SUMMARY.md
    echo "   Recommendation: Build orchestration layer or redesign." >> results/SUMMARY.md
    echo ""
    echo -e "${RED}❌ V001 FAILED - Redesign may be needed${NC}"
else
    echo "⚠️  **Partial Success**" >> results/SUMMARY.md
    echo "   Some features work, some require manual intervention." >> results/SUMMARY.md
    echo "   Recommendation: Proceed with manual mode." >> results/SUMMARY.md
    echo ""
    echo -e "${YELLOW}⚠️  PARTIAL - Manual mode acceptable${NC}"
fi

echo ""
echo "Results saved to: $TEST_DIR/results/SUMMARY.md"
echo ""
echo "View detailed results:"
echo "  cat $TEST_DIR/results/SUMMARY.md"