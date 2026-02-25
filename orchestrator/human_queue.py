#!/usr/bin/env python3
"""
Human review queue manager (file backend).

Supports listing, acknowledging, and resolving queued review items.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


PHASE_TO_REVIEW_TASKS = {
    "design-l1": ["review-l1-ba", "review-l1-pe", "review-l1-le"],
    "design-l2": ["review-l2-architect", "review-l2-le"],
    "design-l3": ["review-l3-pe", "review-l3-coder"],
}

PHASE_TO_ROUTE_TASK = {
    "design-l1": "route-review-l1",
    "design-l2": "route-review-l2",
    "design-l3": "route-review-l3",
}


def _read_json(path: Path, default: Any):
    if not path.exists():
        return default
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return default


def _write_json(path: Path, payload: Any):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)


def _resolve_queue_file(feature_dir: Path) -> Path:
    context = _read_json(feature_dir / "context.json", {})
    rel = (
        context.get("policy_gate", {})
        .get("human_queue", {})
        .get("file_path", "review/human_review_queue.json")
    )
    return feature_dir / rel


def _load_queue(feature_dir: Path) -> List[Dict[str, Any]]:
    return _read_json(_resolve_queue_file(feature_dir), [])


def _save_queue(feature_dir: Path, queue: List[Dict[str, Any]]):
    _write_json(_resolve_queue_file(feature_dir), queue)


def list_queue(feature_dir: Path, status: str = ""):
    queue = _load_queue(feature_dir)
    for item in queue:
        if status and str(item.get("status", "")).upper() != status.upper():
            continue
        print(
            json.dumps(
                {
                    "queue_id": item.get("queue_id"),
                    "phase": item.get("phase"),
                    "risk_tier": item.get("risk_tier"),
                    "route": item.get("route"),
                    "status": item.get("status"),
                    "created_at": item.get("created_at"),
                    "assigned_reviewer": item.get("assigned_reviewer"),
                }
            )
        )


def ack_queue_item(feature_dir: Path, queue_id: str, reviewer: str):
    queue = _load_queue(feature_dir)
    found = False
    for item in queue:
        if item.get("queue_id") == queue_id:
            item["status"] = "ACKED"
            item["assigned_reviewer"] = reviewer
            item["acked_at"] = datetime.now(timezone.utc).isoformat()
            found = True
            break
    if not found:
        raise ValueError(f"queue_id not found: {queue_id}")
    _save_queue(feature_dir, queue)


def resolve_queue_item(
    feature_dir: Path,
    queue_id: str,
    decision: str,
    reviewer: str,
    summary: str,
):
    decision = decision.upper()
    if decision not in {"GO", "NO_GO"}:
        raise ValueError("decision must be GO or NO_GO")

    queue = _load_queue(feature_dir)
    item: Optional[Dict[str, Any]] = None
    for q in queue:
        if q.get("queue_id") == queue_id:
            item = q
            break
    if not item:
        raise ValueError(f"queue_id not found: {queue_id}")

    phase = str(item.get("phase", "design-l1"))
    review_dir = feature_dir / "review"
    workflow_file = feature_dir / "workflow.json"
    context_file = feature_dir / "context.json"
    workflow = _read_json(workflow_file, {})
    context = _read_json(context_file, {})

    human_status = "APPROVED" if decision == "GO" else "REJECTED_WITH_FEEDBACK"
    human_audit_file = review_dir / f"human_audit_{phase.replace('-', '_')}.json"
    _write_json(
        human_audit_file,
        {
            "queue_id": queue_id,
            "reviewerRole": "human-reviewer",
            "decision": decision,
            "status": human_status,
            "summary": summary,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
    )

    if decision == "GO":
        # Mark phase review tasks completed and persist review artifacts.
        for task_id in PHASE_TO_REVIEW_TASKS.get(phase, []):
            if task_id in workflow:
                workflow[task_id]["status"] = "COMPLETED"
                workflow[task_id]["human_resolved_by"] = reviewer
            _write_json(
                review_dir / f"{task_id}.json",
                {
                    "featureId": feature_dir.name,
                    "artifactReviewed": item.get("artifact", ""),
                    "reviewerRole": "human-reviewer",
                    "status": "APPROVED",
                    "route": "HUMAN_QUEUE",
                    "risk_tier": item.get("risk_tier"),
                    "decision": "GO",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "summary": summary,
                },
            )
    else:
        # Preserve conservative behavior: mark route task failed and require manual rework decision.
        route_task = PHASE_TO_ROUTE_TASK.get(phase)
        if route_task and route_task in workflow:
            workflow[route_task]["status"] = "FAILED"
            workflow[route_task]["human_resolved_by"] = reviewer

        circuit = context.get("circuit_breaker", {})
        circuit["intervention_required"] = True
        circuit["blocked_task"] = PHASE_TO_ROUTE_TASK.get(phase)
        circuit["reason"] = f"human NO_GO for {phase}: {summary}"
        context["circuit_breaker"] = circuit

    item["status"] = "RESOLVED" if decision == "GO" else "REJECTED"
    item["resolved_by"] = reviewer
    item["resolved_at"] = datetime.now(timezone.utc).isoformat()
    item["human_decision"] = decision
    item["resolution_summary"] = summary

    context["review_routing"] = {
        **context.get("review_routing", {}),
        "human_decision": decision,
        "human_resolved_by": reviewer,
        "human_resolved_at": item["resolved_at"],
    }

    _save_queue(feature_dir, queue)
    _write_json(workflow_file, workflow)
    _write_json(context_file, context)


def main():
    parser = argparse.ArgumentParser(description="Manage file-based human review queue.")
    parser.add_argument("feature_path", help="Feature directory path")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_list = sub.add_parser("list", help="List queue items")
    p_list.add_argument("--status", default="", help="Optional status filter")

    p_ack = sub.add_parser("ack", help="Acknowledge queue item")
    p_ack.add_argument("--queue-id", required=True)
    p_ack.add_argument("--reviewer", required=True)

    p_resolve = sub.add_parser("resolve", help="Resolve queue item")
    p_resolve.add_argument("--queue-id", required=True)
    p_resolve.add_argument("--decision", required=True, choices=["GO", "NO_GO"])
    p_resolve.add_argument("--reviewer", required=True)
    p_resolve.add_argument("--summary", required=True)

    args = parser.parse_args()
    feature_dir = Path(args.feature_path).expanduser().resolve()

    if args.cmd == "list":
        list_queue(feature_dir, status=args.status)
    elif args.cmd == "ack":
        ack_queue_item(feature_dir, queue_id=args.queue_id, reviewer=args.reviewer)
    elif args.cmd == "resolve":
        resolve_queue_item(
            feature_dir,
            queue_id=args.queue_id,
            decision=args.decision,
            reviewer=args.reviewer,
            summary=args.summary,
        )


if __name__ == "__main__":
    main()
