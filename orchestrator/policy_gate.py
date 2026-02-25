#!/usr/bin/env python3
"""
Evidence-based policy gate evaluator.

This module routes review handling by risk tier and policy flags.
It intentionally does not use confidence score as a gating criterion.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple


class RouteDecision(str, Enum):
    NO_GO = "NO_GO"
    AUTO_APPROVE = "AUTO_APPROVE"
    AUTO_REVIEW = "AUTO_REVIEW"
    HUMAN_QUEUE = "HUMAN_QUEUE"


@dataclass
class PolicyGateResult:
    decision: RouteDecision
    rationale: List[str]
    failed_criteria: List[str]
    warnings: List[str]
    evidence_summary: Dict[str, str]


def validate_policy_config(policy_gate: Optional[Dict[str, Any]]) -> Tuple[bool, List[str]]:
    """Validate policy gate config shape; returns (is_valid, warnings)."""
    warnings: List[str] = []
    if policy_gate is None:
        warnings.append("policy_gate missing; using legacy AUTO_REVIEW fallback")
        return True, warnings

    rc = policy_gate.get("requirement_coverage", {})
    if rc:
        mode = str(rc.get("mode", "advisory")).lower()
        if mode not in {"advisory", "blocking"}:
            warnings.append(f"invalid requirement_coverage.mode={mode}; defaulting to advisory")
        mcp = rc.get("min_coverage_percent", 80)
        try:
            mcp_int = int(mcp)
            if mcp_int < 0 or mcp_int > 100:
                warnings.append("requirement_coverage.min_coverage_percent should be between 0 and 100")
        except (TypeError, ValueError):
            warnings.append("requirement_coverage.min_coverage_percent is not an integer")

    hq = policy_gate.get("human_queue", {})
    if hq:
        backend = str(hq.get("backend", "file")).lower()
        if backend != "file":
            warnings.append(f"unsupported human_queue backend={backend}; file backend will be used")
        if "pause_on_enqueue" in hq and not isinstance(hq.get("pause_on_enqueue"), bool):
            warnings.append("human_queue.pause_on_enqueue should be boolean")

    return True, warnings


def _status_is_pass(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.upper() in {"PASS", "PASSED", "TRUE", "OK"}
    return False


def _normalize_status(value: Any, default: str = "MISSING") -> str:
    if isinstance(value, str):
        return value.upper()
    if isinstance(value, bool):
        return "PASS" if value else "FAIL"
    return default


def _tier_operational_required(risk_tier: str) -> bool:
    return risk_tier.upper() == "T2"


def evaluate_policy_gate(
    risk_tier: str,
    policy_gate: Optional[Dict[str, Any]],
    evidence: Optional[Dict[str, Any]],
) -> PolicyGateResult:
    """
    Evaluate evidence and policy to produce a route decision.

    If policy_gate is missing entirely, fallback to legacy behavior and return
    AUTO_REVIEW to avoid breaking older workflows.
    """
    if policy_gate is None:
        return PolicyGateResult(
            decision=RouteDecision.AUTO_REVIEW,
            rationale=["policy_gate missing; defaulting to legacy AUTO_REVIEW"],
            failed_criteria=[],
            warnings=["policy_gate not configured"],
            evidence_summary={},
        )

    evidence = evidence or {}
    risk_tier = (risk_tier or "T1").upper()

    auto_review_enabled = bool(policy_gate.get("auto_review_enabled", True))
    auto_approve_enabled = bool(policy_gate.get("auto_approve_enabled", False))
    enforce_mandatory_evidence = bool(
        policy_gate.get("enforce_mandatory_evidence", True)
    )

    # Requirement coverage remains optional/tunable.
    req_cov_cfg = policy_gate.get("requirement_coverage", {}) or {}
    req_cov_enabled = bool(req_cov_cfg.get("enabled", False))
    req_cov_mode = str(req_cov_cfg.get("mode", "advisory")).lower()
    req_cov_min = int(req_cov_cfg.get("min_coverage_percent", 80))

    evidence_summary: Dict[str, str] = {
        "acceptance_evidence": _normalize_status(evidence.get("acceptance_evidence")),
        "verification_results": _normalize_status(evidence.get("verification_results")),
        "operational_readiness": _normalize_status(
            evidence.get("operational_readiness"),
            default="NOT_REQUIRED" if not _tier_operational_required(risk_tier) else "MISSING",
        ),
        "requirement_coverage": "NOT_ENFORCED" if not req_cov_enabled else "UNKNOWN",
    }

    failed_criteria: List[str] = []
    warnings: List[str] = []

    mandatory_checks = [
        ("acceptance_evidence", evidence.get("acceptance_evidence")),
        ("verification_results", evidence.get("verification_results")),
    ]
    if _tier_operational_required(risk_tier):
        mandatory_checks.append(("operational_readiness", evidence.get("operational_readiness")))

    if enforce_mandatory_evidence:
        for name, value in mandatory_checks:
            if not _status_is_pass(value):
                failed_criteria.append(name)

    if req_cov_enabled:
        measured = req_cov_cfg.get("measured_percent", evidence.get("requirement_coverage_percent"))
        status = "UNKNOWN"
        try:
            measured_int = int(measured)
            if measured_int >= req_cov_min:
                status = "PASS"
            else:
                status = "FAIL"
        except (TypeError, ValueError):
            measured_int = None
            status = "MISSING"

        evidence_summary["requirement_coverage"] = status
        if status != "PASS":
            if req_cov_mode == "blocking":
                failed_criteria.append("requirement_coverage")
            else:
                warnings.append(
                    "requirement_coverage below threshold or missing in advisory mode"
                )

    if failed_criteria:
        return PolicyGateResult(
            decision=RouteDecision.NO_GO,
            rationale=["mandatory evidence failed policy gate"],
            failed_criteria=failed_criteria,
            warnings=warnings,
            evidence_summary=evidence_summary,
        )

    # Routing by risk tier + policy.
    if risk_tier == "T2":
        return PolicyGateResult(
            decision=RouteDecision.HUMAN_QUEUE,
            rationale=["T2 policy requires human sign-off"],
            failed_criteria=[],
            warnings=warnings,
            evidence_summary=evidence_summary,
        )

    if risk_tier == "T1":
        decision = RouteDecision.AUTO_REVIEW if auto_review_enabled else RouteDecision.HUMAN_QUEUE
        return PolicyGateResult(
            decision=decision,
            rationale=[f"T1 policy routes to {decision.value}"],
            failed_criteria=[],
            warnings=warnings,
            evidence_summary=evidence_summary,
        )

    # Default T0 path.
    if auto_approve_enabled:
        decision = RouteDecision.AUTO_APPROVE
    elif auto_review_enabled:
        decision = RouteDecision.AUTO_REVIEW
    else:
        decision = RouteDecision.HUMAN_QUEUE

    return PolicyGateResult(
        decision=decision,
        rationale=[f"T0 policy routes to {decision.value}"],
        failed_criteria=[],
        warnings=warnings,
        evidence_summary=evidence_summary,
    )
