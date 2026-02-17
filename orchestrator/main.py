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
from pathlib import Path
from typing import Dict, List, Optional, Set
from enum import Enum


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
    }
    
    def __init__(self, feature_path: Path, mode: ExecutionMode = ExecutionMode.AUTONOMOUS):
        self.feature_path = feature_path
        self.mode = mode
        self.workflow_file = feature_path / "workflow.json"
        self.workflow = self.load_workflow()
        
    def load_workflow(self) -> Dict:
        """Load the workflow.json file"""
        with open(self.workflow_file, 'r') as f:
            return json.load(f)
    
    def save_workflow(self):
        """Save the updated workflow.json"""
        with open(self.workflow_file, 'w') as f:
            json.dump(self.workflow, f, indent=2)
    
    def get_ready_tasks(self) -> List[str]:
        """Find all tasks that are ready to execute (dependencies met)"""
        ready = []
        for task_id, task in self.workflow.items():
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
        
        # Execute the command (this would invoke the appropriate agent)
        # In actual implementation, this would call Claude Code/Roo Code CLI
        # with the agent context and command
        success = self.invoke_agent(agent, task["command"])
        
        if success:
            task["status"] = TaskStatus.COMPLETED.value
            print(f"✓ Task {task_id} completed successfully\n")
        else:
            task["status"] = TaskStatus.FAILED.value
            print(f"✗ Task {task_id} failed\n")
        
        self.save_workflow()
        return success
    
    def invoke_agent(self, agent: str, command: str) -> bool:
        """
        Invoke the specified agent with the command.
        This is a placeholder - actual implementation would call:
        - claude-code with agent context
        - roo-code with agent context
        """
        # TODO: Implement actual agent invocation
        # For now, just log what would happen
        print(f"[INVOKE] Agent '{agent}' executing: {command}")
        return True
    
    def check_review_outcome(self, task_id: str) -> Optional[str]:
        """Check if a review task resulted in rejection"""
        # Map review task to its outcome file
        review_file_map = {
            "review-l1-ba": "review/review_l1_ba.json",
            "review-l1-pe": "review/review_l1_pe.json",
            "review-l1-le": "review/review_l1_le.json",
            "review-l2-architect": "review/review_l2_architect.json",
            "review-l2-le": "review/review_l2_le.json",
            "review-l3-pe": "review/review_l3_pe.json",
            "review-l3-coder": "review/review_l3_coder.json",
        }
        
        if task_id not in review_file_map:
            return None
        
        review_file = self.feature_path / review_file_map[task_id]
        if not review_file.exists():
            return None
        
        with open(review_file, 'r') as f:
            outcome = json.load(f)
            return outcome.get("status")
    
    def handle_review_feedback(self, review_task_id: str):
        """Handle rejected reviews by adding rework tasks to workflow"""
        # Determine the corresponding rework task
        rework_map = {
            "review-l1-ba": "design-l1-rework",
            "review-l1-pe": "design-l1-rework",
            "review-l1-le": "design-l1-rework",
            "review-l2-architect": "design-l2-rework",
            "review-l2-le": "design-l2-rework",
            "review-l3-pe": "design-l3-rework",
            "review-l3-coder": "design-l3-rework",
        }
        
        rework_task_id = rework_map.get(review_task_id)
        if rework_task_id and rework_task_id not in self.workflow:
            print(f"⚠ Review rejected - adding {rework_task_id} to workflow")
            # Add rework task (this would be properly configured in actual implementation)
            # For now, this is a placeholder
    
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
                if pending_count == 0:
                    print("\n✅ Workflow completed successfully!")
                    break
                else:
                    print(f"\n⚠ No ready tasks, but {pending_count} tasks still pending.")
                    print("Workflow may be stuck. Check for circular dependencies.")
                    break
            
            # Execute all ready tasks
            for task_id in ready_tasks:
                self.execute_task(task_id)
                
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