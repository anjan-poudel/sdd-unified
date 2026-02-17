# SDD Unified Framework - Validation Master Plan

**Status:** Ready to Execute
**Priority:** CRITICAL
**Estimated Total Time:** 8-12 hours over 2-4 days

---

## Executive Summary

This validation plan tests the **critical assumption** that Claude Code can natively execute the sdd_unified framework's workflow.json as a DAG with agent switching and status management.

**If validation succeeds:** Framework is production-ready, no code dependencies needed
**If validation fails:** Need orchestrator.py or significant architecture revision

---

## Three-Phase Validation Strategy

### Phase 1: Agent Loading (30-60 min)
**Tests:** Can Claude Code load external agent configurations?

- Install single agent (sdd-ba)
- Test persona adherence
- Test command execution
- Test file creation

**Success = Proceed to Phase 2**

→ [Phase 1 Guide](phase1-agent-loading/README.md)

---

### Phase 2: Workflow Execution (2-3 hours)
**Tests:** Can Claude Code execute workflow.json as a DAG?

- Create minimal 3-task workflow
- Test dependency resolution
- Test sequential execution
- Test status persistence
- Test agent switching

**Success = Proceed to Phase 3**

→ [Phase 2 Guide](phase2-workflow-execution/README.md)

---

### Phase 3: End-to-End Feature (4-8 hours)
**Tests:** Complete feature development with all capabilities

- Use FSM Parallel Workflow Engine use case
- Test all 5 agents
- Test parallel reviews
- Test rework loops
- Test complete L1 → L2 → L3 → Implementation flow

**Success = Framework validated, ready for production**

→ [Phase 3 Guide](phase3-end-to-end/README.md)

---

## Quick Start

### Prerequisites

1. **Claude Code installed and running**
   ```bash
   # Verify Claude Code is available
   which claude-code || echo "Claude Code not found"
   ```

2. **Repository cloned**
   ```bash
   cd /Users/anjan/workspace/projects/SDD/sdd_unified
   ```

3. **Time allocated**
   - Phase 1: 30-60 minutes (can do immediately)
   - Phase 2: 2-3 hours (half day)
   - Phase 3: 4-8 hours (full day or spread over 2 days)

### Execution Sequence

**Day 1 Morning: Phase 1**
```bash
cd validation-tests/phase1-agent-loading
# Follow README.md step by step
# Record results in README.md checkboxes
```

**Day 1 Afternoon: Phase 2** (if Phase 1 passed)
```bash
cd ../phase2-workflow-execution
# Follow README.md step by step
# Record critical findings
```

**Day 2: Phase 3** (if Phase 2 passed)
```bash
cd ../phase3-end-to-end
# Follow README.md - full feature development
# This is the comprehensive test
```

---

## Decision Tree

```
START
  ↓
Phase 1: Agent Loading
  ├─ PASS → Continue to Phase 2
  └─ FAIL → BLOCKER: Claude Code can't load external agents
             └─ Investigate: Version issue? Configuration? Fundamental limitation?

Phase 2: Workflow Execution
  ├─ PASS → Continue to Phase 3
  └─ FAIL → CRITICAL: Need orchestrator.py
             └─ Decision: Keep orchestrator or redesign framework

Phase 3: End-to-End
  ├─ Grade A (30-35/35) → ✅ Production Ready
  ├─ Grade B (25-29/35) → ⚠️ Minor fixes needed
  ├─ Grade C (20-24/35) → ⚠️ Significant rework
  └─ Below 20/35 → ❌ Major redesign required
```

---

## Critical Questions Being Answered

### Question 1: Pure Configuration Model Viable?
**Can sdd_unified work without any Python/code dependencies?**

**Phase 1 tests:** Agent loading from YAML
**Phase 2 tests:** Workflow execution from JSON
**Phase 3 tests:** Complete workflow without scripts

**Answer determines:**
- Whether to keep/remove orchestrator.py
- Installation complexity
- Framework portability
- Maintenance burden

---

### Question 2: Native DAG Execution?
**Does Claude Code execute workflow.json as a dependency graph?**

**Phase 2 tests:** Dependency resolution, sequential execution
**Phase 3 tests:** Full DAG with parallel branches

**Answer determines:**
- If parallel reviews work
- If conditional branching works (rework loops)
- If workflow.json is truly "single source of truth"

---

### Question 3: Agent Context Preservation?
**Does context persist across agent switches?**

**Phase 2 tests:** Simple agent switching
**Phase 3 tests:** Complex multi-agent handoffs

**Answer determines:**
- If context.json mechanism works
- If agents can build on each other's work
- Quality of agent collaboration

---

### Question 4: Status Management?
**Who updates workflow.json - Claude Code or external script?**

**Phase 2 tests:** Basic status updates
**Phase 3 tests:** Complex status management with reviews

**Answer determines:**
- If orchestrator.py needed for state management
- If workflow.json is read-only or read-write
- Level of automation achievable

---

## Success Criteria (Overall)

### Minimum Viable Validation (MVP)

**Must Pass:**
- ✅ Phase 1: Agent loading works
- ✅ Phase 2: Basic workflow execution works
- ✅ Phase 3: At least Grade C (20+/35)

**With these, framework is viable** (even if needs orchestrator.py)

---

### Ideal Validation (Pure Config Model)

**Must Pass:**
- ✅ Phase 1: Perfect score
- ✅ Phase 2: All critical tests pass
- ✅ Phase 3: Grade A (30+/35)
- ✅ No manual intervention needed
- ✅ No orchestrator.py required

**With these, framework is production-ready as pure configuration**

---

## Failure Modes and Responses

### Failure Mode 1: Phase 1 Fails
**Symptom:** Claude Code can't load external agent configs

**Investigation:**
1. Check Claude Code version/documentation
2. Verify YAML syntax
3. Test with minimal agent config
4. Check file permissions

**Response:**
- Try inline agent definitions
- Use MCP server approach
- Consider alternative tool (Roo Code, Aider)

---

### Failure Mode 2: Phase 2 Fails - No DAG Execution
**Symptom:** Claude Code doesn't parse workflow.json automatically

**Response:**
- **Option A:** Keep orchestrator.py (it reads workflow.json and invokes Claude Code)
- **Option B:** Manual workflow (user triggers each task)
- **Option C:** Simplify to linear workflow (remove DAG complexity)

**Timeline Impact:** +4-6 weeks for orchestrator integration

---

### Failure Mode 3: Phase 2 Fails - No Status Management
**Symptom:** workflow.json doesn't get updated automatically

**Response:**
- **Option A:** orchestrator.py manages status
- **Option B:** Manual status updates
- **Option C:** Use alternative state tracking (context.json only)

**Timeline Impact:** +2-4 weeks

---

### Failure Mode 4: Phase 3 Fails - Low Score
**Symptom:** Multiple issues, score below 20/35

**Response:**
- Document all blockers
- Categorize: Fixable vs. Fundamental
- Decision meeting: Continue or pivot?
- Consider alternative frameworks or tools

**Timeline Impact:** +2-3 months for major revision

---

## After Validation: Next Steps

### If Validation Succeeds (Grade A/B)

**Week 1:**
1. Document actual behavior in ARCHITECTURE_CORRECTION.md
2. Update CLAUDE.md with validated workflows
3. Remove or minimize orchestrator.py
4. Simplify installation scripts

**Week 2:**
5. Create "lite" workflow templates
6. Add more use case examples
7. Write user guides based on actual behavior
8. Prepare v1.0 release

**Week 3:**
9. Community testing
10. Bug fixes
11. Release v1.0

---

### If Validation Partially Succeeds (Grade C)

**Week 1-2:**
1. Fix documented issues
2. Keep orchestrator.py with clear role
3. Update documentation

**Week 3-4:**
4. Re-test specific areas
5. Create hybrid model documentation
6. Release v1.0-beta

**Week 5-8:**
7. Gather feedback
8. Iterate
9. Release v1.0

---

### If Validation Fails (Below Grade C)

**Week 1:**
1. Full retrospective on findings
2. Identify fundamental vs. fixable issues
3. Decision: Pivot or persist?

**Week 2-4:**
4. Design alternative architecture
5. Prototype new approach
6. Re-validate

**Month 2-3:**
7. Full rebuild if needed
8. New validation cycle

---

## Validation Team Roles

### Primary Validator (You)
- Execute all three phases
- Record findings meticulously
- Make go/no-go decisions at each phase
- Document workarounds

### Secondary Review (Optional)
- Review validation results
- Challenge assumptions
- Verify findings independently
- Provide alternative perspective

---

## Documentation Outputs

### During Validation

Create these files as you progress:

1. **phase1-results.md**
   - Test outcomes
   - Screenshots (if helpful)
   - Blockers encountered

2. **phase2-results.md**
   - Critical findings
   - Workflow execution model
   - Status management behavior

3. **phase3-results.md**
   - Score breakdown
   - What worked / what didn't
   - Recommendations

### After Validation

4. **VALIDATION_FINAL_REPORT.md**
   - Executive summary
   - Overall grade
   - Architecture decision (keep/remove orchestrator)
   - Timeline to v1.0
   - Next steps

5. **Update existing docs:**
   - ARCHITECTURE_CORRECTION.md → confirmed behavior
   - CLAUDE.md → validated workflows
   - README.md → installation based on findings

---

## Risk Management

### High-Risk Scenario
**Both Phase 1 AND Phase 2 fail**

**Mitigation:**
- Allocate 1 day for troubleshooting before giving up
- Have backup plan: orchestrator.py + manual workflow
- Consider alternative tools in parallel

### Medium-Risk Scenario
**Phase 3 shows major gaps**

**Mitigation:**
- Partial implementation is still valuable
- Document working subset
- Release as "beta" or "experimental"
- Gather community feedback

### Low-Risk Scenario
**Minor issues, but overall success**

**Mitigation:**
- Create issue tracker
- Prioritize fixes
- Ship v1.0 with known limitations
- Iterate quickly based on usage

---

## Timeline Estimates

### Optimistic Path (Everything Works)
- **Week 1:** Validation complete, Grade A
- **Week 2:** Documentation updates
- **Week 3:** v1.0 release
- **Total: 3 weeks**

### Realistic Path (Minor Issues)
- **Week 1:** Validation complete, Grade B
- **Week 2-3:** Fixes and refinement
- **Week 4:** v1.0 release
- **Total: 4 weeks**

### Pessimistic Path (Significant Issues)
- **Week 1:** Validation shows problems
- **Week 2-4:** Architecture revision
- **Week 5-6:** Re-validation
- **Week 7-8:** v1.0-beta release
- **Total: 8 weeks**

### Worst Case (Fundamental Redesign)
- **Month 1:** Validation fails, redesign needed
- **Month 2:** Rebuild core components
- **Month 3:** Re-validation and release
- **Total: 3 months**

---

## Getting Started NOW

**You can start Phase 1 immediately** (30-60 minutes):

```bash
cd /Users/anjan/workspace/projects/SDD/sdd_unified/validation-tests/phase1-agent-loading

# Follow the README.md step-by-step
# This will answer the first critical question:
# "Can Claude Code load external agent configs?"

# No preparation needed, just execute and observe
```

**After Phase 1**, you'll know if the pure configuration model is even possible.

---

## Questions?

Before starting, clarify:
1. ✅ Claude Code installed and working?
2. ✅ Time allocated for validation?
3. ✅ Ready to document findings thoroughly?
4. ✅ Prepared for any outcome (success or need for pivot)?

**If yes to all → BEGIN WITH PHASE 1**

---

**Good luck! This validation will definitively answer whether the sdd_unified framework works as designed.**
