import json
import tempfile
import unittest
from pathlib import Path

from orchestrator.main import ExecutionMode, WorkflowOrchestrator
from orchestrator.human_queue import resolve_queue_item


def _write_json(path: Path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f)


def _read_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


class HumanQueueTests(unittest.TestCase):
    def test_human_queue_disabled_does_not_pause(self):
        with tempfile.TemporaryDirectory() as tmp:
            feature = Path(tmp)
            _write_json(
                feature / "workflow.json",
                {
                    "route-review-l1": {
                        "command": "sdd-route-review-l1 --task_id=route-review-l1",
                        "status": "PENDING",
                        "dependencies": [],
                    }
                },
            )
            _write_json(
                feature / "context.json",
                {
                    "risk_tier": "T2",
                    "policy_gate": {
                        "auto_review_enabled": True,
                        "enforce_mandatory_evidence": True,
                        "human_queue": {
                            "enabled": False,
                            "backend": "file",
                            "pause_on_enqueue": True,
                        },
                        "evidence": {
                            "design-l1": {
                                "acceptance_evidence": "PASS",
                                "verification_results": "PASS",
                                "operational_readiness": "PASS",
                            }
                        },
                    },
                },
            )

            orch = WorkflowOrchestrator(feature, ExecutionMode.AUTONOMOUS)
            success = orch.execute_task("route-review-l1")
            self.assertTrue(success)
            self.assertFalse(orch.halt_requested)
            self.assertEqual(orch.workflow["route-review-l1"]["status"], "COMPLETED")

    def test_resolve_go_marks_reviews_completed(self):
        with tempfile.TemporaryDirectory() as tmp:
            feature = Path(tmp)
            review_dir = feature / "review"
            review_dir.mkdir(parents=True, exist_ok=True)

            queue_item = {
                "queue_id": "q-1",
                "phase": "design-l1",
                "risk_tier": "T2",
                "route": "HUMAN_QUEUE",
                "artifact": "design/l1_architecture.md",
                "status": "PENDING",
            }
            _write_json(review_dir / "human_review_queue.json", [queue_item])
            _write_json(
                feature / "workflow.json",
                {
                    "route-review-l1": {"status": "COMPLETED", "dependencies": [], "command": "x"},
                    "review-l1-ba": {"status": "PENDING", "dependencies": ["route-review-l1"], "command": "x"},
                    "review-l1-pe": {"status": "PENDING", "dependencies": ["route-review-l1"], "command": "x"},
                    "review-l1-le": {"status": "PENDING", "dependencies": ["route-review-l1"], "command": "x"},
                },
            )
            _write_json(
                feature / "context.json",
                {
                    "policy_gate": {
                        "human_queue": {
                            "enabled": True,
                            "backend": "file",
                            "pause_on_enqueue": True,
                            "file_path": "review/human_review_queue.json",
                        }
                    }
                },
            )

            resolve_queue_item(
                feature,
                queue_id="q-1",
                decision="GO",
                reviewer="principal",
                summary="Approved after human review",
            )

            queue = _read_json(review_dir / "human_review_queue.json")
            self.assertEqual(queue[0]["status"], "RESOLVED")
            self.assertEqual(queue[0]["human_decision"], "GO")

            wf = _read_json(feature / "workflow.json")
            self.assertEqual(wf["review-l1-ba"]["status"], "COMPLETED")
            self.assertEqual(wf["review-l1-pe"]["status"], "COMPLETED")
            self.assertEqual(wf["review-l1-le"]["status"], "COMPLETED")
            self.assertTrue((review_dir / "human_audit_design_l1.json").exists())


if __name__ == "__main__":
    unittest.main()
