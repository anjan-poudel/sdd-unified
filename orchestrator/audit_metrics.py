#!/usr/bin/env python3
"""
Policy-gate audit metrics utility.

Computes routing and audit quality metrics across one or more feature folders.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


ROUTE_PHASE_REVIEW_FILES = {
    "design-l1": ["review-l1-ba.json", "review-l1-pe.json", "review-l1-le.json"],
    "design-l2": ["review-l2-architect.json", "review-l2-le.json"],
    "design-l3": ["review-l3-pe.json", "review-l3-coder.json"],
}


def _load_json(path: Path) -> Optional[Dict[str, Any]]:
    if not path.exists():
        return None
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return None


def _normalize_decision(payload: Optional[Dict[str, Any]]) -> Optional[str]:
    if not payload:
        return None
    decision = payload.get("decision")
    if isinstance(decision, str):
        decision = decision.upper()
        if decision in {"GO", "NO_GO"}:
            return decision
    status = payload.get("status")
    if isinstance(status, str):
        status = status.upper()
        if status == "APPROVED":
            return "GO"
        if status in {"REJECTED", "REJECTED_WITH_FEEDBACK"}:
            return "NO_GO"
    return None


def _phase_from_route_file(path: Path) -> Optional[str]:
    payload = _load_json(path)
    if payload and isinstance(payload.get("phase"), str):
        return payload["phase"]
    stem = path.stem.replace("review_routing_", "")
    return stem.replace("_", "-") if stem else None


def _automated_decision(feature_dir: Path, phase: str, route: str) -> Optional[str]:
    if route == "AUTO_APPROVE":
        return "GO"
    if route != "AUTO_REVIEW":
        return None

    review_dir = feature_dir / "review"
    files = ROUTE_PHASE_REVIEW_FILES.get(phase, [])
    if not files:
        return None

    decisions: List[str] = []
    for fname in files:
        d = _normalize_decision(_load_json(review_dir / fname))
        if d:
            decisions.append(d)

    if not decisions:
        return None
    return "NO_GO" if "NO_GO" in decisions else "GO"


def compute_metrics(feature_dirs: List[Path]) -> Dict[str, Any]:
    route_distribution = {
        "AUTO_APPROVE": 0,
        "AUTO_REVIEW": 0,
        "HUMAN_QUEUE": 0,
        "NO_GO": 0,
        "UNKNOWN": 0,
    }
    total_routes = 0

    comparisons = 0
    disagreements = 0
    compared_items: List[Dict[str, Any]] = []
    rework_events = 0
    handover_events = 0

    for feature_dir in feature_dirs:
        review_dir = feature_dir / "review"
        context = _load_json(feature_dir / "context.json") or {}
        rework_events += sum(
            1
            for e in context.get("execution_log", [])
            if isinstance(e, dict)
            and str(e.get("task_id", "")).startswith("design-")
            and "rework" in str(e.get("task_id", ""))
            and str(e.get("status", "")).upper() == "COMPLETED"
        )
        handover_events += len(
            context.get("handover_notes", {}).get("history", [])
            if isinstance(context.get("handover_notes"), dict)
            else []
        )

        if not review_dir.exists():
            continue

        for route_file in sorted(review_dir.glob("review_routing_*.json")):
            route_payload = _load_json(route_file) or {}
            route = str(route_payload.get("route", "UNKNOWN")).upper()
            if route not in route_distribution:
                route = "UNKNOWN"
            route_distribution[route] += 1
            total_routes += 1

            phase = _phase_from_route_file(route_file)
            if not phase:
                continue

            auto_decision = _automated_decision(feature_dir, phase, route)
            human_audit_file = review_dir / f"human_audit_{phase.replace('-', '_')}.json"
            human_decision = _normalize_decision(_load_json(human_audit_file))

            if auto_decision and human_decision:
                comparisons += 1
                mismatch = auto_decision != human_decision
                if mismatch:
                    disagreements += 1
                compared_items.append(
                    {
                        "feature": feature_dir.name,
                        "phase": phase,
                        "route": route,
                        "auto_decision": auto_decision,
                        "human_decision": human_decision,
                        "disagreement": mismatch,
                    }
                )

    disagreement_rate = (disagreements / comparisons) if comparisons else None

    return {
        "features_scanned": len(feature_dirs),
        "routes_total": total_routes,
        "route_distribution": route_distribution,
        "rework_events_completed": rework_events,
        "handover_events": handover_events,
        "audit_comparisons": comparisons,
        "audit_disagreements": disagreements,
        "audit_disagreement_rate": disagreement_rate,
        "compared_items": compared_items,
    }


def _discover_feature_dirs(root: Path) -> List[Path]:
    # Feature dir is any directory with workflow.json and review/ folder.
    matches: List[Path] = []
    for workflow in root.rglob("workflow.json"):
        feature_dir = workflow.parent
        if (feature_dir / "review").exists():
            matches.append(feature_dir)
    # Stable de-duplication.
    unique = sorted({p.resolve() for p in matches})
    return unique


def main():
    parser = argparse.ArgumentParser(description="Compute policy-gate audit metrics.")
    parser.add_argument(
        "path",
        nargs="?",
        default="validation-tests/policy-gate-fixtures",
        help="Root path containing feature folders (default: validation-tests/policy-gate-fixtures)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="",
        help="Optional output JSON file path",
    )
    args = parser.parse_args()

    root = Path(args.path).expanduser().resolve()
    feature_dirs = _discover_feature_dirs(root)
    summary = compute_metrics(feature_dirs)

    print(json.dumps(summary, indent=2))

    if args.output:
        out = Path(args.output).expanduser().resolve()
        out.parent.mkdir(parents=True, exist_ok=True)
        with out.open("w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2)


if __name__ == "__main__":
    main()
