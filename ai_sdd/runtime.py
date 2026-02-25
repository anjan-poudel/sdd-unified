#!/usr/bin/env python3
"""Runtime adapter interfaces for ai-sdd."""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple


@dataclass
class Invocation:
    task_id: str
    agent_id: str
    command: str
    cwd: Path
    strict: bool
    timeout_seconds: int
    env: Dict[str, str]


@dataclass
class TaskResult:
    success: bool
    exit_code: int
    stdout: str
    stderr: str
    error_type: str
    summary: str


class RuntimeAdapter:
    name = "base"

    def invoke(self, invocation: Invocation) -> TaskResult:
        raise NotImplementedError


class ShellAdapter(RuntimeAdapter):
    name = "shell"

    def invoke(self, invocation: Invocation) -> TaskResult:
        if invocation.command.startswith("ai-sdd-") and not invocation.strict:
            return TaskResult(
                success=True,
                exit_code=0,
                stdout="[SIMULATED] ai-sdd command accepted in non-strict mode",
                stderr="",
                error_type="NONE",
                summary="Simulated ai-sdd command",
            )
        try:
            p = subprocess.run(
                invocation.command,
                cwd=str(invocation.cwd),
                shell=True,
                text=True,
                capture_output=True,
                timeout=max(1, int(invocation.timeout_seconds)),
                env=invocation.env,
            )
        except subprocess.TimeoutExpired as e:
            return TaskResult(
                success=False,
                exit_code=124,
                stdout=e.stdout or "",
                stderr=e.stderr or "",
                error_type="TIMEOUT",
                summary=f"Command timed out after {invocation.timeout_seconds}s",
            )
        except Exception as e:
            return TaskResult(
                success=False,
                exit_code=1,
                stdout="",
                stderr=str(e),
                error_type="INVOCATION_ERROR",
                summary="Invocation exception",
            )
        return TaskResult(
            success=(p.returncode == 0),
            exit_code=p.returncode,
            stdout=p.stdout or "",
            stderr=p.stderr or "",
            error_type="NONE" if p.returncode == 0 else "COMMAND_ERROR",
            summary="Command succeeded" if p.returncode == 0 else "Command failed",
        )


class ClaudeCodeAdapter(RuntimeAdapter):
    name = "claude_code"

    def invoke(self, invocation: Invocation) -> TaskResult:
        return TaskResult(
            success=False,
            exit_code=2,
            stdout="",
            stderr="ClaudeCodeAdapter scaffold only",
            error_type="NOT_IMPLEMENTED",
            summary="Adapter not implemented",
        )


def resolve_runtime_adapter(name: str) -> Tuple[RuntimeAdapter, List[str]]:
    n = (name or "shell").strip().lower()
    if n in {"shell", ""}:
        return ShellAdapter(), []
    if n in {"claude", "claude_code", "claudecode"}:
        return ClaudeCodeAdapter(), []
    return ShellAdapter(), [f"Unknown adapter '{name}', fallback to shell"]

