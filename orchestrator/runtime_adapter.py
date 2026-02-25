#!/usr/bin/env python3
"""
Runtime adapter scaffold for task invocation.

The orchestrator stays runtime-agnostic by delegating command execution
to an adapter implementation.
"""

from __future__ import annotations

import os
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple


@dataclass
class Invocation:
    task_id: str
    agent: str
    command: str
    feature_path: Path
    strict: bool
    timeout_seconds: int
    env: Dict[str, str]


@dataclass
class TaskResult:
    success: bool
    status: str
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
        # Compatibility shim for command names that depend on external runtimes.
        if invocation.command.startswith("sdd-") and not invocation.strict:
            return TaskResult(
                success=True,
                status="COMPLETED",
                exit_code=0,
                stdout="[SIMULATED] Non-strict mode accepted sdd-* command",
                stderr="",
                error_type="NONE",
                summary="Simulated success for sdd-* command in non-strict mode",
            )

        try:
            result = subprocess.run(
                invocation.command,
                cwd=str(invocation.feature_path),
                shell=True,
                text=True,
                capture_output=True,
                timeout=max(1, int(invocation.timeout_seconds)),
                env=invocation.env,
            )
        except subprocess.TimeoutExpired as e:
            return TaskResult(
                success=False,
                status="FAILED",
                exit_code=124,
                stdout=e.stdout or "",
                stderr=e.stderr or "",
                error_type="TIMEOUT",
                summary=f"Command timed out after {invocation.timeout_seconds}s",
            )
        except Exception as e:
            return TaskResult(
                success=False,
                status="FAILED",
                exit_code=1,
                stdout="",
                stderr=str(e),
                error_type="INVOCATION_ERROR",
                summary=f"Invocation exception: {e}",
            )

        ok = result.returncode == 0
        return TaskResult(
            success=ok,
            status="COMPLETED" if ok else "FAILED",
            exit_code=result.returncode,
            stdout=result.stdout or "",
            stderr=result.stderr or "",
            error_type="NONE" if ok else "COMMAND_ERROR",
            summary="Command succeeded" if ok else "Command failed",
        )


class ClaudeCodeAdapter(RuntimeAdapter):
    """
    Scaffold adapter for Claude Code integration.

    This is intentionally a placeholder until runtime-specific transport
    and command contracts are finalized.
    """

    name = "claude_code"

    def invoke(self, invocation: Invocation) -> TaskResult:
        return TaskResult(
            success=False,
            status="FAILED",
            exit_code=2,
            stdout="",
            stderr="ClaudeCodeAdapter is not implemented yet.",
            error_type="NOT_IMPLEMENTED",
            summary="Adapter scaffold only; implementation pending",
        )


def resolve_runtime_adapter(name: str) -> Tuple[RuntimeAdapter, List[str]]:
    normalized = (name or "").strip().lower()
    warnings: List[str] = []

    if normalized in {"", "shell"}:
        return ShellAdapter(), warnings
    if normalized in {"claude", "claude_code", "claudecode"}:
        return ClaudeCodeAdapter(), warnings

    warnings.append(f"Unknown runtime adapter '{name}', falling back to 'shell'")
    return ShellAdapter(), warnings


def runtime_config_from_context(context: Dict) -> Dict:
    runtime = context.get("runtime", {}) if isinstance(context, dict) else {}
    strict_env = os.getenv("SDD_STRICT_COMMANDS", "0") == "1"
    timeout_env = os.getenv("SDD_TASK_TIMEOUT", "120")
    try:
        timeout_default = int(timeout_env)
    except ValueError:
        timeout_default = 120

    return {
        "adapter": os.getenv("SDD_RUNTIME_ADAPTER", runtime.get("adapter", "shell")),
        "strict": bool(runtime.get("strict", strict_env)),
        "timeout_seconds": int(runtime.get("timeout_seconds", timeout_default)),
    }
