# Evidence-Based Quality Gates (Tunable)

This document defines a tunable, evidence-based scoring system for quality gates that replaces confidence-based thresholds with objective, verifiable evidence.

## 1. Core Principle

**Evidence Over Confidence**: Gates use verifiable artifacts (tests, coverage, lint results) rather than subjective confidence scores.

## 2. Evidence Categories

Each category produces a **score** (0.0 to 1.0) and a **status** (PASS/WARN/FAIL).

### 2.1 Requirement Coverage (OPTIONAL, TUNABLE)

**Why Optional**: Requirement traceability is difficult to determine accurately and may not apply to all change types (refactoring, tech debt, bug fixes).

**Configuration**:
```json
{
  "requirement_coverage": {
    "enabled": true,
    "weight": 0.15,
    "thresholds": {
      "pass": 0.90,
      "warn": 0.70
    },
    "enforcement": "warn_only"
  }
}
```

**Scoring Logic**:
- **Score**: `mapped_requirements / total_requirements`
- **Status**:
  - `PASS` if score ≥ pass threshold
  - `WARN` if score ≥ warn threshold
  - `FAIL` if score < warn threshold
- **Enforcement**:
  - `mandatory`: FAIL blocks approval
  - `warn_only`: FAIL produces warning but doesn't block
  - `disabled`: Category not scored

**Evidence Required**:
```json
{
  "requirement_ids": ["REQ-001", "REQ-002"],
  "mapped_to": {
    "REQ-001": ["TASK-010", "TASK-011"],
    "REQ-002": ["TASK-012"]
  },
  "unmapped": []
}
```

### 2.2 Acceptance Criteria (MANDATORY for T1/T2)

**Configuration**:
```json
{
  "acceptance_criteria": {
    "enabled": true,
    "weight": 0.25,
    "thresholds": {
      "pass": 1.0,
      "warn": 0.8
    },
    "enforcement": "mandatory"
  }
}
```

**Scoring Logic**:
- **Score**: `(bdd_scenarios_present + testable_criteria) / (expected_scenarios + expected_criteria)`
- **Status**: PASS if all acceptance criteria are defined and testable

**Evidence Required**:
```json
{
  "bdd_scenarios": [
    {
      "scenario_id": "AC-REQ-001-1",
      "status": "testable",
      "gherkin_present": true
    }
  ],
  "coverage": {
    "scenarios_defined": 5,
    "scenarios_testable": 5,
    "scenarios_automated": 4
  }
}
```

### 2.3 Verification Results (MANDATORY)

**Configuration**:
```json
{
  "verification_results": {
    "enabled": true,
    "weight": 0.40,
    "thresholds": {
      "pass": 1.0,
      "warn": 0.95
    },
    "enforcement": "mandatory"
  }
}
```

**Scoring Logic**:
- **Score**: `passed_checks / total_checks`
- **Status**: PASS if all critical checks pass

**Evidence Required**:
```json
{
  "test_results": {
    "unit_tests": {"passed": 45, "failed": 0, "total": 45},
    "integration_tests": {"passed": 12, "failed": 0, "total": 12}
  },
  "static_analysis": {
    "lint": "PASS",
    "type_check": "PASS",
    "complexity": "PASS"
  },
  "security_checks": {
    "dependency_scan": "PASS",
    "sast": "PASS"
  }
}
```

### 2.4 Operational Readiness (MANDATORY for T2)

**Configuration**:
```json
{
  "operational_readiness": {
    "enabled": true,
    "weight": 0.20,
    "thresholds": {
      "pass": 1.0,
      "warn": 0.8
    },
    "enforcement": "risk_tiered"
  }
}
```

**Scoring Logic**:
- **Score**: `completed_items / required_items`
- **Status**: Risk-tier dependent (T2 must have all items)

**Evidence Required**:
```json
{
  "release_notes": "present",
  "rollback_plan": "present",
  "observability": {
    "metrics_added": ["api.latency", "db.connections"],
    "alerts_configured": true,
    "dashboards_updated": true
  },
  "runbook_updated": true
}
```

## 3. Composite Score Calculation

### 3.1 Weighted Score

```
composite_score = Σ(category_score × category_weight) / Σ(enabled_category_weights)
```

**Example** (with requirement coverage disabled):
```
composite_score = (0.25 × 1.0) + (0.40 × 0.98) + (0.20 × 1.0) / (0.25 + 0.40 + 0.20)
                = 0.642 / 0.85
                = 0.755 (75.5%)
```

### 3.2 Go/No-Go Decision

**Primary Rule**: ALL mandatory enforcement categories must PASS.

**Secondary Rule** (if all mandatory pass):
- `composite_score ≥ 0.90`: **GO** (auto-approve if configured)
- `composite_score ≥ 0.75`: **GO with WARNINGS** (human review recommended)
- `composite_score < 0.75`: **NO-GO** (human review required)

**Override Rule**: T2 changes always require human sign-off regardless of score.

## 4. Risk-Tiered Configuration

### T0 (Low-Risk: Docs, Minor Refactoring)

```json
{
  "risk_tier": "T0",
  "requirement_coverage": {"enabled": false},
  "acceptance_criteria": {"enforcement": "warn_only"},
  "verification_results": {"enforcement": "mandatory"},
  "operational_readiness": {"enabled": false}
}
```

### T1 (Standard: Features, API Changes)

```json
{
  "risk_tier": "T1",
  "requirement_coverage": {"enabled": true, "enforcement": "warn_only"},
  "acceptance_criteria": {"enforcement": "mandatory"},
  "verification_results": {"enforcement": "mandatory"},
  "operational_readiness": {"enforcement": "warn_only"}
}
```

### T2 (High-Risk: Auth, Payments, Data Model, Security)

```json
{
  "risk_tier": "T2",
  "requirement_coverage": {"enabled": true, "enforcement": "mandatory"},
  "acceptance_criteria": {"enforcement": "mandatory"},
  "verification_results": {"enforcement": "mandatory"},
  "operational_readiness": {"enforcement": "mandatory"},
  "human_signoff_required": true
}
```

## 5. Review Output Format

### 5.1 Raw Evidence Report

```json
{
  "review_id": "REV-2026-02-21-001",
  "artifact": "design/l2_component_design.md",
  "timestamp": "2026-02-21T10:30:00Z",
  "evidence_scores": {
    "requirement_coverage": {
      "enabled": true,
      "score": 0.85,
      "status": "WARN",
      "threshold_pass": 0.90,
      "threshold_warn": 0.70,
      "enforcement": "warn_only",
      "details": {
        "total_requirements": 10,
        "mapped_requirements": 8,
        "unmapped": ["REQ-009", "REQ-010"]
      }
    },
    "acceptance_criteria": {
      "enabled": true,
      "score": 1.0,
      "status": "PASS",
      "enforcement": "mandatory",
      "details": {
        "scenarios_defined": 5,
        "scenarios_testable": 5
      }
    },
    "verification_results": {
      "enabled": true,
      "score": 0.98,
      "status": "PASS",
      "enforcement": "mandatory",
      "details": {
        "tests_passed": 57,
        "tests_failed": 0,
        "lint": "PASS",
        "security": "PASS"
      }
    },
    "operational_readiness": {
      "enabled": true,
      "score": 1.0,
      "status": "PASS",
      "enforcement": "warn_only",
      "details": {
        "release_notes": "present",
        "rollback_plan": "present"
      }
    }
  },
  "composite_score": 0.96,
  "decision": "GO",
  "decision_rationale": "All mandatory categories PASS. Composite score 0.96 exceeds 0.90 threshold.",
  "warnings": [
    "Requirement coverage at 85% (below 90% threshold). Unmapped: REQ-009, REQ-010."
  ],
  "required_actions": []
}
```

### 5.2 Human-Readable Summary

```
╔══════════════════════════════════════════════════════════╗
║  REVIEW DECISION: GO (with warnings)                     ║
╚══════════════════════════════════════════════════════════╝

Composite Score: 96% (threshold: 90%)
Risk Tier: T1

Evidence Breakdown:
  ✓ Acceptance Criteria    100% [PASS] (mandatory)
  ✓ Verification Results    98% [PASS] (mandatory)
  ✓ Operational Readiness  100% [PASS] (warn only)
  ⚠ Requirement Coverage    85% [WARN] (warn only)

Warnings:
  ⚠ Requirement coverage at 85% (below 90% threshold)
     Unmapped requirements: REQ-009, REQ-010

Rationale:
  All mandatory categories pass. Composite score exceeds
  threshold. Warnings present but non-blocking for T1.

Next Steps:
  - Proceed to next workflow stage
  - Consider mapping REQ-009, REQ-010 in future iteration
```

## 6. Configuration Management

### 6.1 Global Defaults

Store in `.sdd_unified/config/quality_gates.json`:

```json
{
  "default_risk_tier": "T1",
  "categories": {
    "requirement_coverage": {
      "enabled": true,
      "weight": 0.15,
      "thresholds": {"pass": 0.90, "warn": 0.70},
      "enforcement": "warn_only"
    },
    "acceptance_criteria": {
      "enabled": true,
      "weight": 0.25,
      "thresholds": {"pass": 1.0, "warn": 0.8},
      "enforcement": "mandatory"
    },
    "verification_results": {
      "enabled": true,
      "weight": 0.40,
      "thresholds": {"pass": 1.0, "warn": 0.95},
      "enforcement": "mandatory"
    },
    "operational_readiness": {
      "enabled": true,
      "weight": 0.20,
      "thresholds": {"pass": 1.0, "warn": 0.8},
      "enforcement": "risk_tiered"
    }
  },
  "risk_tier_overrides": {
    "T0": {
      "requirement_coverage": {"enabled": false},
      "operational_readiness": {"enabled": false}
    },
    "T2": {
      "requirement_coverage": {"enforcement": "mandatory"},
      "operational_readiness": {"enforcement": "mandatory"},
      "human_signoff_required": true
    }
  }
}
```

### 6.2 Feature-Level Overrides

In feature's `context.json`:

```json
{
  "quality_gate_config": {
    "requirement_coverage": {
      "enabled": false,
      "rationale": "Tech debt cleanup - no explicit requirements"
    }
  }
}
```

## 7. Integration with workflow.json

Review tasks should execute with gate configuration:

```json
{
  "review-l2-pe": {
    "command": "sdd-pe-review-l2 --task_id=review-l2-pe --gate_config=.sdd_unified/config/quality_gates.json",
    "status": "PENDING",
    "dependencies": ["design-l2"]
  }
}
```

Review output includes evidence scores and decision rationale.

## 8. Tuning Guidelines

### When to Disable Requirement Coverage

- Tech debt or refactoring work without explicit requirements
- Bug fixes with incident tickets instead of requirement IDs
- Early exploration/prototyping phases

### When to Lower Thresholds

- Legacy codebases with incomplete test coverage
- Gradual adoption (ratcheting up over time)
- Experimental features with high uncertainty

### When to Raise Thresholds

- Production systems with high stability requirements
- Security-critical components
- After establishing baseline metrics

## 9. Success Metrics

Track over time to validate tuning:

- **Gate Effectiveness**: Defect escape rate by risk tier
- **False Positive Rate**: % of NO-GO decisions later reversed
- **Coverage Trends**: Requirement/test coverage over time
- **Review Cycle Time**: Time from artifact complete to gate decision

## 10. Relationship to Pair Review Overlay

This evidence-based gate system complements the pair review overlay:

1. **Pair Session** (Driver + Challenger) produces artifact
2. **Artifact DRI** signs off on completion
3. **Evidence-Based Gate** validates objective quality criteria
4. **Independent Reviewer** (if required by risk tier) provides final approval

The gate acts as an **objective filter** before human review, ensuring evidence exists regardless of who reviews.
