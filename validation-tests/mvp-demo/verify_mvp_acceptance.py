#!/usr/bin/env python3
"""
Machine-verifiable MVP acceptance checks.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List


def _read_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _assert(cond: bool, msg: str, failures: List[str]):
    if not cond:
        failures.append(msg)


def main() -> int:
    repo = Path(__file__).resolve().parents[2]
    results = repo / "validation-tests" / "mvp-demo" / "results"
    loop_log = results / "mvp_loop.log"
    queue_log = results / "mvp_queue.log"
    metrics_file = results / "mvp_metrics.json"

    loop_feature = repo / "validation-tests" / "mvp-demo" / "feature-loop"
    loop_context = loop_feature / "context.json"
    loop_workflow = loop_feature / "workflow.json"

    queue_feature = repo / "validation-tests" / "policy-gate-fixtures" / "t2_human_queue"
    queue_file = queue_feature / "review" / "human_review_queue.json"
    human_audit = queue_feature / "review" / "human_audit_design_l1.json"

    failures: List[str] = []

    # Artifacts exist.
    for p in [loop_log, queue_log, metrics_file, loop_context, loop_workflow, queue_file, human_audit]:
        _assert(p.exists(), f"Missing required artifact: {p}", failures)
    if failures:
        for f in failures:
            print(f"[FAIL] {f}")
        return 1

    loop_text = loop_log.read_text(encoding="utf-8")
    queue_text = queue_log.read_text(encoding="utf-8")
    context = _read_json(loop_context)
    workflow = _read_json(loop_workflow)
    metrics = _read_json(metrics_file)
    queue_items = _read_json(queue_file)

    # A. Multi-agent flow
    for agent in ["sdd-ba", "sdd-architect", "sdd-pe", "sdd-le", "sdd-coder"]:
        _assert(f"Agent: {agent}" in loop_text, f"Missing agent in loop log: {agent}", failures)
    _assert(len(context.get("execution_log", [])) > 0, "execution_log should be non-empty", failures)

    # B. Handover continuity
    history = context.get("handover_notes", {}).get("history", [])
    _assert(isinstance(history, list), "handover_notes.history must be a list", failures)
    _assert(len(history) >= 5, "handover history should have at least 5 entries", failures)
    if history:
        _assert("task_completed" in history[0], "handover entry missing task_completed", failures)
        _assert("from_agent" in history[0], "handover entry missing from_agent", failures)

    # C. Review loop
    _assert("Review rejected - forcing design-l1-rework to READY" in loop_text, "Missing rejection->rework signal", failures)
    _assert("Task: design-l1-rework" in loop_text, "Missing design-l1-rework execution", failures)
    _assert(loop_text.count("Task: review-l1-ba") >= 2, "review-l1-ba should rerun after rework", failures)
    _assert(workflow.get("design-l1-rework", {}).get("status") == "COMPLETED", "design-l1-rework status should be COMPLETED", failures)
    _assert(workflow.get("review-l1-ba", {}).get("status") == "COMPLETED", "review-l1-ba status should be COMPLETED", failures)

    # D. Policy routing
    for phase in ["design_l1", "design_l2", "design_l3"]:
        route_file = loop_feature / "review" / f"review_routing_{phase}.json"
        _assert(route_file.exists(), f"Missing routing file {route_file.name}", failures)
        if route_file.exists():
            r = _read_json(route_file)
            _assert("route" in r, f"{route_file.name} missing route", failures)
            _assert("risk_tier" in r, f"{route_file.name} missing risk_tier", failures)
            _assert("evidence_summary" in r, f"{route_file.name} missing evidence_summary", failures)

    # E. Human queue
    _assert(
        ("HUMAN_QUEUE" in queue_text) or ("Human review required" in queue_text),
        "Queue log missing HUMAN_QUEUE path",
        failures,
    )
    _assert(isinstance(queue_items, list) and len(queue_items) > 0, "Queue file should contain at least one item", failures)
    if queue_items:
        qi = queue_items[0]
        _assert("queue_id" in qi, "Queue item missing queue_id", failures)
        _assert("status" in qi, "Queue item missing status", failures)
        _assert(qi.get("backend") == "file", "Queue backend should be file", failures)

    # F. Metrics
    for key in ["route_distribution", "rework_events_completed", "handover_events", "audit_disagreement_rate"]:
        _assert(key in metrics, f"Metrics missing key: {key}", failures)
    _assert(int(metrics.get("rework_events_completed", 0)) >= 1, "Expected rework_events_completed >= 1", failures)
    _assert(int(metrics.get("handover_events", 0)) >= 5, "Expected handover_events >= 5", failures)

    if failures:
        for f in failures:
            print(f"[FAIL] {f}")
        return 1

    print("[PASS] MVP acceptance checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
