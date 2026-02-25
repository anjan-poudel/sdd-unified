#!/usr/bin/env python3
"""Constitution inheritance loading for ai-sdd."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

import yaml


def _read_constitution(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return data if isinstance(data, dict) else {}


def _deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    out = dict(base)
    for k, v in override.items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _deep_merge(out[k], v)
        else:
            out[k] = v
    return out


def load_recursive_constitution(project_root: Path, task_workdir: str = ".") -> Dict[str, Any]:
    """
    Merge constitution files recursively from project root to task workdir.
    Expected filename: constitution.yaml.
    """
    merged: Dict[str, Any] = {}
    root = project_root.resolve()
    target = (project_root / task_workdir).resolve()

    if root not in [target, *target.parents]:
        return merged

    chain = []
    p = target
    while True:
        chain.append(p)
        if p == root:
            break
        p = p.parent
    chain.reverse()

    for directory in chain:
        merged = _deep_merge(merged, _read_constitution(directory / "constitution.yaml"))

    return merged

