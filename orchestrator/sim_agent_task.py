#!/usr/bin/env python3
"""
Simulated agent task runner for MVP concept demos.

Creates deterministic artifacts to demonstrate:
- multi-agent handovers
- review rejection -> rework loop
- policy routing and human queue integration
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict


def _read_json(path: Path, default: Dict[str, Any]) -> Dict[str, Any]:
    if not path.exists():
        return default
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return default


def _write_json(path: Path, payload: Dict[str, Any]):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)


def _write_text(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _sim_state(context: Dict[str, Any]) -> Dict[str, Any]:
    return context.setdefault("sim_state", {})


def run_task(feature_dir: Path, task_id: str, agent: str):
    context_file = feature_dir / "context.json"
    context = _read_json(context_file, {})
    state = _sim_state(context)

    if task_id == "define-requirements":
        _write_text(
            feature_dir / "spec" / "requirements.md",
            "# Requirements\n- REQ-001: MVP supports review loops.\n",
        )
        _write_json(
            feature_dir / "spec" / "spec.yaml",
            {
                "metadata": {"featureId": feature_dir.name},
                "functionalRequirements": [{"id": "REQ-001", "description": "Loop behavior"}],
            },
        )

    elif task_id in {"design-l1", "design-l1-rework"}:
        _write_text(
            feature_dir / "design" / "l1_architecture.md",
            "# L1 Architecture\n- service boundaries\n- review-safe assumptions\n",
        )
        if task_id == "design-l1-rework":
            state["l1_rework_done"] = True

    elif task_id in {"design-l2", "design-l2-rework"}:
        _write_text(
            feature_dir / "design" / "l2_component_design.md",
            "# L2 Component Design\n- contracts\n- data model\n",
        )
        if task_id == "design-l2-rework":
            state["l2_rework_done"] = True

    elif task_id in {"design-l3", "design-l3-rework"}:
        _write_text(
            feature_dir / "implementation" / "l3_plan.md",
            "# L3 Plan\n- task-001\n- task-002\n",
        )
        if task_id == "design-l3-rework":
            state["l3_rework_done"] = True

    elif task_id.startswith("review-l1-"):
        # Force one rejection on first pass, then approve after rework.
        rejected_once = bool(state.get("l1_rejected_once", False))
        is_rejecting_reviewer = task_id == "review-l1-ba"
        should_reject = (not rejected_once) and is_rejecting_reviewer and (not state.get("l1_rework_done", False))
        if should_reject:
            state["l1_rejected_once"] = True
        _write_json(
            feature_dir / "review" / f"{task_id}.json",
            {
                "featureId": feature_dir.name,
                "artifactReviewed": "design/l1_architecture.md",
                "reviewerRole": agent,
                "status": "REJECTED_WITH_FEEDBACK" if should_reject else "APPROVED",
                "decision": "NO_GO" if should_reject else "GO",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "summary": "Needs tighter boundaries" if should_reject else "Looks good",
            },
        )

    elif task_id.startswith("review-l2-"):
        _write_json(
            feature_dir / "review" / f"{task_id}.json",
            {
                "featureId": feature_dir.name,
                "artifactReviewed": "design/l2_component_design.md",
                "reviewerRole": agent,
                "status": "APPROVED",
                "decision": "GO",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "summary": "Approved",
            },
        )

    elif task_id.startswith("review-l3-"):
        _write_json(
            feature_dir / "review" / f"{task_id}.json",
            {
                "featureId": feature_dir.name,
                "artifactReviewed": "implementation/l3_plan.md",
                "reviewerRole": agent,
                "status": "APPROVED",
                "decision": "GO",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "summary": "Approved",
            },
        )

    context["sim_state"] = state
    _write_json(context_file, context)


def main():
    parser = argparse.ArgumentParser(description="Run a simulated SDD task.")
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--agent", required=True)
    parser.add_argument("--feature-dir", default=".")
    args = parser.parse_args()

    run_task(Path(args.feature_dir).resolve(), args.task_id, args.agent)


if __name__ == "__main__":
    main()
