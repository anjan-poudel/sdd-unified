import json
import tempfile
import unittest
from pathlib import Path

from orchestrator.main import ExecutionMode, WorkflowOrchestrator


def _write_json(path: Path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f)


class RuntimeExecutionTests(unittest.TestCase):
    def test_real_command_execution_success(self):
        with tempfile.TemporaryDirectory() as tmp:
            feature = Path(tmp)
            _write_json(
                feature / "workflow.json",
                {
                    "task-1": {
                        "command": "python3 -c \"open('ok.txt','w').write('ok')\"",
                        "status": "PENDING",
                        "dependencies": [],
                    }
                },
            )
            _write_json(feature / "context.json", {})
            orch = WorkflowOrchestrator(feature, ExecutionMode.AUTONOMOUS)
            success = orch.execute_task("task-1")
            self.assertTrue(success)
            self.assertTrue((feature / "ok.txt").exists())
            self.assertEqual(orch.workflow["task-1"]["status"], "COMPLETED")

    def test_rejected_review_forces_rework_ready(self):
        with tempfile.TemporaryDirectory() as tmp:
            feature = Path(tmp)
            _write_json(
                feature / "workflow.json",
                {
                    "review-l1-ba": {
                        "command": "python3 -c \"import json;json.dump({'status':'REJECTED_WITH_FEEDBACK','decision':'NO_GO'},open('review/review-l1-ba.json','w'))\"",
                        "status": "PENDING",
                        "dependencies": [],
                    },
                    "design-l1-rework": {
                        "command": "python3 -c \"print('rework')\"",
                        "status": "PENDING",
                        "dependencies": ["review-l1-ba"],
                    },
                },
            )
            _write_json(feature / "context.json", {})
            (feature / "review").mkdir(parents=True, exist_ok=True)
            orch = WorkflowOrchestrator(feature, ExecutionMode.AUTONOMOUS)
            orch.execute_task("review-l1-ba")
            outcome = orch.check_review_outcome("review-l1-ba")
            self.assertEqual(outcome, "REJECTED_WITH_FEEDBACK")
            orch.handle_review_feedback("review-l1-ba")
            self.assertEqual(orch.workflow["review-l1-ba"]["status"], "FAILED")
            self.assertEqual(orch.workflow["design-l1-rework"]["status"], "READY")


if __name__ == "__main__":
    unittest.main()
