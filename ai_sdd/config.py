#!/usr/bin/env python3
"""Configuration loading and validation for ai-sdd."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

import yaml


def _read_yaml(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    if not isinstance(data, dict):
        raise ValueError(f"YAML root must be mapping: {path}")
    return data


def _deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    out = dict(base)
    for k, v in override.items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _deep_merge(out[k], v)
        else:
            out[k] = v
    return out


def load_yaml_with_default(default_path: Path, project_path: Path) -> Dict[str, Any]:
    return _deep_merge(_read_yaml(default_path), _read_yaml(project_path))


def load_context(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError(f"context root must be object: {path}")
    return data


def save_context(path: Path, payload: Dict[str, Any]):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)


def validate_agents_config(cfg: Dict[str, Any]) -> Tuple[bool, List[str]]:
    warnings: List[str] = []
    if "agents" not in cfg or not isinstance(cfg.get("agents"), dict):
        return False, ["agents.yaml must include an 'agents' mapping"]
    for agent_id, agent in cfg["agents"].items():
        if not isinstance(agent, dict):
            warnings.append(f"Agent '{agent_id}' should be mapping")
            continue
        if "role" not in agent:
            warnings.append(f"Agent '{agent_id}' missing 'role'")
        llm = agent.get("llm", {})
        if not isinstance(llm, dict):
            warnings.append(f"Agent '{agent_id}' llm config should be mapping")
    return True, warnings


def validate_workflow_config(cfg: Dict[str, Any]) -> Tuple[bool, List[str]]:
    warnings: List[str] = []
    tasks = cfg.get("tasks")
    if not isinstance(tasks, list) or not tasks:
        return False, ["workflow.yaml must include non-empty tasks list"]
    ids = set()
    for task in tasks:
        if not isinstance(task, dict):
            return False, ["Each task must be a mapping"]
        task_id = task.get("id")
        if not task_id:
            return False, ["Each task must have id"]
        if task_id in ids:
            return False, [f"Duplicate task id: {task_id}"]
        ids.add(task_id)
    for task in tasks:
        deps = task.get("dependencies", [])
        if not isinstance(deps, list):
            return False, [f"Task '{task.get('id')}' dependencies must be list"]
        for dep in deps:
            if dep not in ids:
                return False, [f"Task '{task.get('id')}' has unknown dependency '{dep}'"]
    return True, warnings


def validate_overlays_config(cfg: Dict[str, Any]) -> Tuple[bool, List[str]]:
    warnings: List[str] = []
    loops = cfg.get("loops", {})
    max_iter = loops.get("default_max_iterations", 3)
    try:
        max_iter_int = int(max_iter)
        if max_iter_int <= 0:
            warnings.append("loops.default_max_iterations should be > 0")
    except (TypeError, ValueError):
        warnings.append("loops.default_max_iterations should be integer")
    return True, warnings

