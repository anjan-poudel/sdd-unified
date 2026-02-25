import json
import tempfile
import unittest
from pathlib import Path

from orchestrator.main import WorkflowOrchestrator, ExecutionMode


class OrchestratorRoutingTests(unittest.TestCase):
    def test_route_review_l1_auto_approves_and_writes_artifacts(self):
        with tempfile.TemporaryDirectory() as tmp:
            feature_path = Path(tmp)
            (feature_path / "review").mkdir(parents=True, exist_ok=True)

            workflow = {
                "route-review-l1": {
                    "command": "sdd-route-review-l1 --task_id=route-review-l1",
                    "status": "PENDING",
                    "dependencies": [],
                },
                "review-l1-ba": {
                    "command": "sdd-ba-review-design-l1 --task_id=review-l1-ba",
                    "status": "PENDING",
                    "dependencies": ["route-review-l1"],
                },
                "review-l1-pe": {
                    "command": "sdd-pe-review-design-l1 --task_id=review-l1-pe",
                    "status": "PENDING",
                    "dependencies": ["route-review-l1"],
                },
                "review-l1-le": {
                    "command": "sdd-le-review-design-l1 --task_id=review-l1-le",
                    "status": "PENDING",
                    "dependencies": ["route-review-l1"],
                },
            }
            with (feature_path / "workflow.json").open("w") as f:
                json.dump(workflow, f)

            context = {
                "risk_tier": "T0",
                "policy_gate": {
                    "auto_approve_enabled": True,
                    "auto_review_enabled": True,
                    "enforce_mandatory_evidence": True,
                    "evidence": {
                        "design-l1": {
                            "acceptance_evidence": "PASS",
                            "verification_results": "PASS",
                        }
                    },
                },
            }
            with (feature_path / "context.json").open("w") as f:
                json.dump(context, f)

            orch = WorkflowOrchestrator(feature_path, ExecutionMode.AUTONOMOUS)
            success = orch.execute_task("route-review-l1")

            self.assertTrue(success)
            self.assertEqual(
                orch.workflow["route-review-l1"]["status"],
                "COMPLETED",
            )
            self.assertEqual(orch.workflow["review-l1-ba"]["status"], "COMPLETED")
            self.assertEqual(orch.workflow["review-l1-pe"]["status"], "COMPLETED")
            self.assertEqual(orch.workflow["review-l1-le"]["status"], "COMPLETED")

            routing_file = feature_path / "review" / "review_routing_design_l1.json"
            self.assertTrue(routing_file.exists())


if __name__ == "__main__":
    unittest.main()
