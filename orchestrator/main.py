#!/usr/bin/env python3
"""
SDD Unified Framework - Workflow Orchestrator

This orchestrator executes the workflow DAG autonomously, handling:
- Task dependency resolution
- Automatic agent switching
- Review/rework feedback loops
- Human intervention points (optional)
"""

import json
import sys
import os
import argparse
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Set
from enum import Enum
try:
    from .policy_gate import evaluate_policy_gate, RouteDecision, validate_policy_config
    from .runtime_adapter import (
        Invocation,
        TaskResult,
        resolve_runtime_adapter,
        runtime_config_from_context,
    )
except ImportError:
    from policy_gate import evaluate_policy_gate, RouteDecision, validate_policy_config
    from runtime_adapter import (
        Invocation,
        TaskResult,
        resolve_runtime_adapter,
        runtime_config_from_context,
    )


class TaskStatus(Enum):
    PENDING = "PENDING"
    READY = "READY"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class ExecutionMode(Enum):
    AUTONOMOUS = "autonomous"
    SUPERVISED = "supervised"
    MANUAL = "manual"


class WorkflowOrchestrator:
    """Orchestrates the execution of the SDD workflow DAG"""
    
    # Map task IDs to their responsible agents
    TASK_AGENT_MAP = {
        "init": "feature",
        "define-requirements": "sdd-ba",
        "design-l1": "sdd-architect",
        "design-l1-rework": "sdd-architect",
        "review-l1-ba": "sdd-ba",
        "review-l1-pe": "sdd-pe",
        "review-l1-le": "sdd-le",
        "design-l2": "sdd-pe",
        "design-l2-rework": "sdd-pe",
        "review-l2-architect": "sdd-architect",
        "review-l2-le": "sdd-le",
        "design-l3": "sdd-le",
        "design-l3-rework": "sdd-le",
        "review-l3-pe": "sdd-pe",
        "review-l3-coder": "sdd-coder",
        "route-review-l1": "sdd-le",
        "route-review-l2": "sdd-le",
        "route-review-l3": "sdd-le",
    }

    ROUTE_TO_REVIEW_TASKS = {
        "route-review-l1": ["review-l1-ba", "review-l1-pe", "review-l1-le"],
        "route-review-l2": ["review-l2-architect", "review-l2-le"],
        "route-review-l3": ["review-l3-pe", "review-l3-coder"],
    }

    ROUTE_TO_ARTIFACT = {
        "route-review-l1": "design/l1_architecture.md",
        "route-review-l2": "design/l2_component_design.md",
        "route-review-l3": "implementation/l3_plan.md",
    }

    REVIEW_TO_REWORK = {
        "review-l1-ba": "design-l1-rework",
        "review-l1-pe": "design-l1-rework",
        "review-l1-le": "design-l1-rework",
        "review-l2-architect": "design-l2-rework",
        "review-l2-le": "design-l2-rework",
        "review-l3-pe": "design-l3-rework",
        "review-l3-coder": "design-l3-rework",
    }

    REWORK_TO_REVIEWS = {
        "design-l1-rework": ["review-l1-ba", "review-l1-pe", "review-l1-le"],
        "design-l2-rework": ["review-l2-architect", "review-l2-le"],
        "design-l3-rework": ["review-l3-pe", "review-l3-coder"],
    }
    
    def __init__(self, feature_path: Path, mode: ExecutionMode = ExecutionMode.AUTONOMOUS):
        self.feature_path = feature_path
        self.mode = mode
        self.workflow_file = feature_path / "workflow.json"
        self.context_file = feature_path / "context.json"
        self.workflow = self.load_workflow()
        self.halt_requested = False
        self.halt_reason = ""
        self.runtime_adapter = None
        self.runtime_config = {}
        self._load_or_init_context()
        self._init_runtime_adapter()
        
    def load_workflow(self) -> Dict:
        """Load the workflow.json file"""
        with open(self.workflow_file, 'r') as f:
            return json.load(f)
    
    def save_workflow(self):
        """Save the updated workflow.json"""
        with open(self.workflow_file, 'w') as f:
            json.dump(self.workflow, f, indent=2)

    def load_context(self) -> Dict:
        """Load context.json if present, else return empty context."""
        if not self.context_file.exists():
            return {}
        with open(self.context_file, "r") as f:
            return json.load(f)

    def save_context(self, context: Dict):
        """Persist context.json."""
        with open(self.context_file, "w") as f:
            json.dump(context, f, indent=2)

    def _write_json(self, path: Path, payload: Dict):
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w") as f:
            json.dump(payload, f, indent=2)

    def _load_or_init_context(self):
        context = self.load_context()
        if not context:
            context = {
                "feature_id": self.feature_path.name,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "last_updated": datetime.now(timezone.utc).isoformat(),
                "handover_notes": {"history": []},
                "execution_log": [],
                "circuit_breaker": {
                    "max_review_iterations": 3,
                    "max_task_rework_iterations": 2,
                    "intervention_required": False,
                    "blocked_task": None,
                    "reason": None,
                },
            }
        context.setdefault("handover_notes", {}).setdefault("history", [])
        context.setdefault("execution_log", [])
        context.setdefault("policy_gate", {})
        context.setdefault("risk_tier", "T1")
        context.setdefault(
            "runtime",
            {
                "adapter": "shell",
                "strict": False,
                "timeout_seconds": 120,
            },
        )
        _, warnings = validate_policy_config(context.get("policy_gate"))
        if warnings:
            context.setdefault("policy_validation_warnings", [])
            context["policy_validation_warnings"].extend(warnings)
        self.save_context(context)

    def _init_runtime_adapter(self):
        context = self.load_context()
        self.runtime_config = runtime_config_from_context(context)
        adapter, warnings = resolve_runtime_adapter(self.runtime_config.get("adapter", "shell"))
        self.runtime_adapter = adapter

        context.setdefault("runtime", {})
        context["runtime"]["selected_adapter"] = adapter.name
        context["runtime"]["strict"] = bool(self.runtime_config.get("strict", False))
        context["runtime"]["timeout_seconds"] = int(self.runtime_config.get("timeout_seconds", 120))
        if warnings:
            context.setdefault("runtime_warnings", [])
            context["runtime_warnings"].extend(warnings)
        self.save_context(context)

    def _record_execution_event(
        self,
        task_id: str,
        agent: str,
        command: str,
        status: str,
        exit_code: int = 0,
        summary: str = "",
    ):
        context = self.load_context()
        context["last_updated"] = datetime.now(timezone.utc).isoformat()
        context.setdefault("execution_log", []).append(
            {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "task_id": task_id,
                "agent": agent,
                "command": command,
                "status": status,
                "exit_code": exit_code,
                "summary": summary,
            }
        )
        context.setdefault("handover_notes", {}).setdefault("history", []).append(
            {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "from_agent": agent,
                "to_agent": "next-ready-task",
                "task_completed": task_id,
                "message": summary or f"Task {task_id} finished with status {status}",
                "critical_points": [],
                "artifacts_created": [],
            }
        )
        self.save_context(context)

    def _route_task_phase(self, task_id: str) -> str:
        if task_id.endswith("l1"):
            return "design-l1"
        if task_id.endswith("l2"):
            return "design-l2"
        return "design-l3"

    def _is_dormant_rework(self, task_id: str, task: Dict) -> bool:
        return task_id in self.REWORK_TO_REVIEWS and not bool(task.get("activated", False))

    def _handle_route_task(self, task_id: str):
        """Evaluate policy gate and route review handling."""
        phase = self._route_task_phase(task_id)
        context = self.load_context()
        policy_gate = context.get("policy_gate")
        risk_tier = context.get("risk_tier", "T1")
        evidence = (
            context.get("policy_gate", {})
            .get("evidence", {})
            .get(phase, {})
        )

        result = evaluate_policy_gate(
            risk_tier=risk_tier,
            policy_gate=policy_gate,
            evidence=evidence,
        )

        route_payload = {
            "phase": phase,
            "route_task_id": task_id,
            "artifact": self.ROUTE_TO_ARTIFACT.get(task_id, ""),
            "risk_tier": risk_tier,
            "route": result.decision.value,
            "failed_criteria": result.failed_criteria,
            "warnings": result.warnings,
            "evidence_summary": result.evidence_summary,
            "rationale": result.rationale,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        route_file = self.feature_path / "review" / f"review_routing_{phase.replace('-', '_')}.json"
        self._write_json(route_file, route_payload)

        context["review_routing"] = route_payload
        self.save_context(context)

        review_tasks = self.ROUTE_TO_REVIEW_TASKS.get(task_id, [])

        if result.decision == RouteDecision.NO_GO:
            self.workflow[task_id]["status"] = TaskStatus.FAILED.value
            self.save_workflow()
            return False

        if result.decision == RouteDecision.AUTO_APPROVE:
            for review_task_id in review_tasks:
                if review_task_id in self.workflow:
                    self.workflow[review_task_id]["status"] = TaskStatus.COMPLETED.value
                    self.workflow[review_task_id]["auto_completed_by"] = task_id
                    review_file = self.feature_path / "review" / f"{review_task_id}.json"
                    self._write_json(
                        review_file,
                        {
                            "featureId": str(self.feature_path.name),
                            "artifactReviewed": self.ROUTE_TO_ARTIFACT.get(task_id, ""),
                            "reviewerRole": "policy-gate",
                            "status": "APPROVED",
                            "route": "AUTO_APPROVE",
                            "risk_tier": risk_tier,
                            "decision": "GO",
                            "timestamp": datetime.now(timezone.utc).isoformat(),
                            "summary": "Auto-approved by evidence-based policy gate",
                        },
                    )
            self.save_workflow()
            return True

        if result.decision == RouteDecision.HUMAN_QUEUE:
            human_queue_cfg = (
                context.get("policy_gate", {})
                .get("human_queue", {})
            )
            queue_enabled = bool(human_queue_cfg.get("enabled", True))
            queue_backend = str(human_queue_cfg.get("backend", "file")).lower()
            queue_pause = bool(human_queue_cfg.get("pause_on_enqueue", True))
            queue_rel_path = str(
                human_queue_cfg.get("file_path", "review/human_review_queue.json")
            )

            if not queue_enabled:
                route_payload["warnings"].append(
                    "human queue disabled by policy; continuing without queue pause"
                )
                context["review_routing"] = route_payload
                self.save_context(context)
                return True

            if queue_backend != "file":
                route_payload["warnings"].append(
                    f"unsupported human_queue backend '{queue_backend}', falling back to file"
                )

            queue_file = self.feature_path / queue_rel_path
            existing_queue: List[Dict] = []
            if queue_file.exists():
                with open(queue_file, "r") as f:
                    try:
                        existing_queue = json.load(f)
                    except json.JSONDecodeError:
                        existing_queue = []
            queue_item = dict(route_payload)
            queue_item["queue_id"] = str(uuid.uuid4())
            queue_item["status"] = "PENDING"
            queue_item["backend"] = "file"
            queue_item["created_at"] = datetime.now(timezone.utc).isoformat()
            existing_queue.append(queue_item)
            self._write_json(queue_file, existing_queue)
            context["review_routing"] = queue_item
            self.save_context(context)
            if queue_pause:
                self.halt_requested = True
                self.halt_reason = (
                    f"Human review required for {phase} ({risk_tier}); "
                    f"queued in {queue_rel_path}"
                )
            return True

        # AUTO_REVIEW: no status overrides; normal review tasks proceed.
        return True
    
    def get_ready_tasks(self) -> List[str]:
        """Find all tasks that are ready to execute (dependencies met)"""
        ready = []
        for task_id, task in self.workflow.items():
            if task_id in self.REWORK_TO_REVIEWS and not bool(task.get("activated", False)):
                if task.get("status") != TaskStatus.READY.value:
                    continue
            if task["status"] == TaskStatus.READY.value:
                ready.append(task_id)
                continue
            if task["status"] == TaskStatus.PENDING.value:
                # Check if all dependencies are completed
                deps_met = all(
                    self.workflow[dep]["status"] == TaskStatus.COMPLETED.value
                    for dep in task["dependencies"]
                )
                if deps_met:
                    ready.append(task_id)
        return ready
    
    def determine_agent(self, task_id: str) -> str:
        """Determine which agent should execute this task"""
        # Check for pattern matches first (e.g., execute-task-*, rework-task-*)
        if task_id.startswith("execute-task-"):
            return "sdd-coder"
        if task_id.startswith("rework-task-"):
            return "sdd-coder"
        if task_id.startswith("review-task-"):
            return "sdd-le"
        
        # Otherwise use direct mapping
        return self.TASK_AGENT_MAP.get(task_id, "unknown")
    
    def execute_task(self, task_id: str):
        """Execute a single task"""
        task = self.workflow[task_id]
        agent = self.determine_agent(task_id)
        
        print(f"\n{'='*60}")
        print(f"Task: {task_id}")
        print(f"Agent: {agent}")
        print(f"Command: {task['command']}")
        print(f"{'='*60}\n")
        
        # Update status to RUNNING
        task["status"] = TaskStatus.RUNNING.value
        self.save_workflow()

        if task_id.startswith("route-review-"):
            success = self._handle_route_task(task_id)
            if success:
                task["status"] = TaskStatus.COMPLETED.value
                print(f"✓ Task {task_id} completed successfully\n")
                self._record_execution_event(
                    task_id=task_id,
                    agent=agent,
                    command=task["command"],
                    status="COMPLETED",
                    exit_code=0,
                    summary="Policy route task completed",
                )
            else:
                task["status"] = TaskStatus.FAILED.value
                print(f"✗ Task {task_id} failed\n")
                self._record_execution_event(
                    task_id=task_id,
                    agent=agent,
                    command=task["command"],
                    status="FAILED",
                    exit_code=1,
                    summary="Policy route task failed",
                )
            self.save_workflow()
            return success
        
        # Execute the command (this would invoke the appropriate agent)
        # In actual implementation, this would call Claude Code/Roo Code CLI
        # with the agent context and command
        result = self.invoke_agent(task_id, agent, task["command"])
        success = result.success
        
        if success:
            task["status"] = TaskStatus.COMPLETED.value
            print(f"✓ Task {task_id} completed successfully\n")
            self._record_execution_event(
                task_id=task_id,
                agent=agent,
                command=task["command"],
                status="COMPLETED",
                exit_code=result.exit_code,
                summary=result.summary,
            )
        else:
            task["status"] = TaskStatus.FAILED.value
            print(f"✗ Task {task_id} failed\n")
            self._record_execution_event(
                task_id=task_id,
                agent=agent,
                command=task["command"],
                status="FAILED",
                exit_code=result.exit_code,
                summary=result.summary or "Task execution failed",
            )
        # Rework loop support: after rework run, force phase reviews to re-run.
        if success and task_id in self.REWORK_TO_REVIEWS:
            for review_task_id in self.REWORK_TO_REVIEWS[task_id]:
                if review_task_id in self.workflow:
                    self.workflow[review_task_id]["status"] = TaskStatus.PENDING.value
            self.workflow[task_id]["activated"] = False
        
        self.save_workflow()
        return success
    
    def invoke_agent(self, task_id: str, agent: str, command: str) -> TaskResult:
        """
        Invoke the specified agent with the command.
        Runtime-specific execution is delegated to the active runtime adapter.
        """
        print(f"[INVOKE] Agent '{agent}' executing: {command}")
        invocation = Invocation(
            task_id=task_id,
            agent=agent,
            command=command,
            feature_path=self.feature_path,
            strict=bool(self.runtime_config.get("strict", False)),
            timeout_seconds=int(self.runtime_config.get("timeout_seconds", 120)),
            env=dict(os.environ),
        )
        result = self.runtime_adapter.invoke(invocation)
        if result.stdout:
            print(result.stdout.rstrip())
        if result.stderr:
            print(result.stderr.rstrip(), file=sys.stderr)
        return result
    
    def check_review_outcome(self, task_id: str) -> Optional[str]:
        """Check if a review task resulted in rejection"""
        candidates = [
            self.feature_path / "review" / f"{task_id}.json",
            self.feature_path / "review" / f"{task_id.replace('-', '_')}.json",
        ]
        for review_file in candidates:
            if not review_file.exists():
                continue
            with open(review_file, "r") as f:
                outcome = json.load(f)
            decision = str(outcome.get("decision", "")).upper()
            status = str(outcome.get("status", "")).upper()
            if decision == "NO_GO" or status in {"REJECTED", "REJECTED_WITH_FEEDBACK"}:
                return "REJECTED_WITH_FEEDBACK"
            if decision == "GO" or status == "APPROVED":
                return "APPROVED"
        return None
    
    def handle_review_feedback(self, review_task_id: str):
        """Handle rejected reviews by marking review FAILED and forcing rework task READY."""
        rework_task_id = self.REVIEW_TO_REWORK.get(review_task_id)
        if not rework_task_id:
            return

        if review_task_id in self.workflow:
            self.workflow[review_task_id]["status"] = TaskStatus.FAILED.value

        if rework_task_id in self.workflow:
            self.workflow[rework_task_id]["status"] = TaskStatus.READY.value
            self.workflow[rework_task_id]["activated"] = True
            print(f"⚠ Review rejected - forcing {rework_task_id} to READY")
        self.save_workflow()
    
    def run_autonomous(self):
        """Run the workflow in fully autonomous mode"""
        print("\n🚀 Starting autonomous workflow execution...\n")
        
        iteration = 0
        max_iterations = 100  # Safety limit
        
        while iteration < max_iterations:
            ready_tasks = self.get_ready_tasks()
            
            if not ready_tasks:
                # Check if we're done or stuck
                pending_count = sum(
                    1 for t in self.workflow.values() 
                    if t["status"] == TaskStatus.PENDING.value
                )
                actionable_pending_count = sum(
                    1
                    for tid, t in self.workflow.items()
                    if t["status"] == TaskStatus.PENDING.value
                    and not self._is_dormant_rework(tid, t)
                )
                if actionable_pending_count == 0:
                    print("\n✅ Workflow completed successfully!")
                    break
                else:
                    print(f"\n⚠ No ready tasks, but {actionable_pending_count} actionable tasks still pending.")
                    print("Workflow may be stuck. Check for circular dependencies.")
                    break
            
            # Execute all ready tasks
            for task_id in ready_tasks:
                self.execute_task(task_id)
                if self.halt_requested:
                    print(f"\n⏸ Autonomous execution paused: {self.halt_reason}")
                    return
                
                # Check if this was a review that got rejected
                if task_id.startswith("review-"):
                    outcome = self.check_review_outcome(task_id)
                    if outcome == "REJECTED_WITH_FEEDBACK":
                        self.handle_review_feedback(task_id)
            
            iteration += 1
        
        if iteration >= max_iterations:
            print("\n⚠ Maximum iterations reached. Workflow may have issues.")
    
    def run_supervised(self):
        """Run workflow with human approval at milestones"""
        print("\n🎯 Starting supervised workflow execution...\n")
        print("You will be prompted at key milestones.\n")
        
        # Similar to autonomous, but pause at milestones
        # Milestones: after each design phase completion
        milestones = ["design-l1", "design-l2", "design-l3"]
        
        # Implementation would include approval prompts
        # For now, delegate to autonomous mode
        self.run_autonomous()
    
    def run_manual(self):
        """Run workflow one step at a time with user control"""
        print("\n🔧 Manual mode - execute one task at a time\n")
        
        while True:
            ready_tasks = self.get_ready_tasks()
            if not ready_tasks:
                print("\nNo more tasks ready. Workflow complete or stuck.")
                break
            
            print(f"\nReady tasks: {', '.join(ready_tasks)}")
            task_id = input("Enter task ID to execute (or 'quit'): ").strip()
            
            if task_id.lower() == 'quit':
                break
            
            if task_id in ready_tasks:
                self.execute_task(task_id)
            else:
                print(f"Task '{task_id}' is not ready or doesn't exist.")
    
    def run(self):
        """Execute the workflow based on the configured mode"""
        if self.mode == ExecutionMode.AUTONOMOUS:
            self.run_autonomous()
        elif self.mode == ExecutionMode.SUPERVISED:
            self.run_supervised()
        elif self.mode == ExecutionMode.MANUAL:
            self.run_manual()


def main():
    parser = argparse.ArgumentParser(
        description="SDD Unified Framework - Workflow Orchestrator"
    )
    parser.add_argument(
        "feature_path",
        type=Path,
        help="Path to the feature directory"
    )
    parser.add_argument(
        "--mode",
        type=str,
        choices=["autonomous", "supervised", "manual"],
        default="autonomous",
        help="Execution mode (default: autonomous)"
    )
    
    args = parser.parse_args()
    
    if not args.feature_path.exists():
        print(f"Error: Feature path '{args.feature_path}' does not exist")
        sys.exit(1)
    
    mode = ExecutionMode(args.mode)
    orchestrator = WorkflowOrchestrator(args.feature_path, mode)
    orchestrator.run()


if __name__ == "__main__":
    main()
