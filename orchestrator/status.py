#!/usr/bin/env python3
"""
SDD Unified Framework - Workflow Status Reporter

Reads a feature workflow.json and prints a compact status summary.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, Tuple


def load_workflow(workflow_file: Path) -> Dict:
    with workflow_file.open("r", encoding="utf-8") as f:
        return json.load(f)


def resolve_feature_path(path_arg: str) -> Tuple[Path, Path]:
    feature_path = Path(path_arg).expanduser().resolve()
    workflow_file = feature_path / "workflow.json"
    if workflow_file.exists():
        return feature_path, workflow_file
    raise FileNotFoundError(f"workflow.json not found at: {workflow_file}")


def summarize(workflow: Dict) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for task in workflow.values():
        status = task.get("status", "UNKNOWN")
        counts[status] = counts.get(status, 0) + 1
    counts["TOTAL"] = len(workflow)
    return counts


def print_report(feature_path: Path, workflow: Dict):
    counts = summarize(workflow)

    print("SDD Unified Workflow Status")
    print("=" * 32)
    print(f"Feature path: {feature_path}")
    print(f"Total tasks:  {counts.get('TOTAL', 0)}")
    print(f"READY:        {counts.get('READY', 0)}")
    print(f"PENDING:      {counts.get('PENDING', 0)}")
    print(f"RUNNING:      {counts.get('RUNNING', 0)}")
    print(f"COMPLETED:    {counts.get('COMPLETED', 0)}")
    print(f"FAILED:       {counts.get('FAILED', 0)}")
    print("")

    ready = [tid for tid, t in workflow.items() if t.get("status") == "READY"]
    running = [tid for tid, t in workflow.items() if t.get("status") == "RUNNING"]
    failed = [tid for tid, t in workflow.items() if t.get("status") == "FAILED"]

    if running:
        print("Running tasks:")
        for tid in running:
            print(f"- {tid}")
        print("")

    if ready:
        print("Ready tasks:")
        for tid in ready:
            print(f"- {tid}")
        print("")

    if failed:
        print("Failed tasks:")
        for tid in failed:
            print(f"- {tid}")
        print("")


def main():
    parser = argparse.ArgumentParser(description="Show workflow status for an SDD feature.")
    parser.add_argument("feature_path", nargs="?", default=".", help="Feature directory path")
    args = parser.parse_args()

    feature_path, workflow_file = resolve_feature_path(args.feature_path)
    workflow = load_workflow(workflow_file)
    print_report(feature_path, workflow)


if __name__ == "__main__":
    main()
