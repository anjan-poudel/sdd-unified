import json
import tempfile
import unittest
from pathlib import Path

from orchestrator.audit_metrics import compute_metrics


def _write_json(path: Path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f)


class AuditMetricsTests(unittest.TestCase):
    def test_metrics_and_disagreement_rate(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)

            # Feature 1: AUTO_APPROVE + human GO (agreement)
            f1 = root / "t0"
            _write_json(f1 / "workflow.json", {})
            (f1 / "review").mkdir(parents=True, exist_ok=True)
            _write_json(
                f1 / "review" / "review_routing_design_l1.json",
                {"phase": "design-l1", "route": "AUTO_APPROVE"},
            )
            _write_json(
                f1 / "review" / "human_audit_design_l1.json",
                {"decision": "GO"},
            )
            _write_json(
                f1 / "context.json",
                {
                    "execution_log": [{"task_id": "design-l1-rework", "status": "COMPLETED"}],
                    "handover_notes": {"history": [{"task_completed": "design-l1"}]},
                },
            )

            # Feature 2: AUTO_REVIEW + automated GO + human NO_GO (disagreement)
            f2 = root / "t1"
            _write_json(f2 / "workflow.json", {})
            (f2 / "review").mkdir(parents=True, exist_ok=True)
            _write_json(
                f2 / "review" / "review_routing_design_l1.json",
                {"phase": "design-l1", "route": "AUTO_REVIEW"},
            )
            _write_json(
                f2 / "review" / "review-l1-ba.json",
                {"status": "APPROVED"},
            )
            _write_json(
                f2 / "review" / "review-l1-pe.json",
                {"status": "APPROVED"},
            )
            _write_json(
                f2 / "review" / "review-l1-le.json",
                {"status": "APPROVED"},
            )
            _write_json(
                f2 / "review" / "human_audit_design_l1.json",
                {"decision": "NO_GO"},
            )
            _write_json(
                f2 / "context.json",
                {"execution_log": [], "handover_notes": {"history": []}},
            )

            summary = compute_metrics([f1, f2])
            self.assertEqual(summary["routes_total"], 2)
            self.assertEqual(summary["route_distribution"]["AUTO_APPROVE"], 1)
            self.assertEqual(summary["route_distribution"]["AUTO_REVIEW"], 1)
            self.assertEqual(summary["rework_events_completed"], 1)
            self.assertEqual(summary["handover_events"], 1)
            self.assertEqual(summary["audit_comparisons"], 2)
            self.assertEqual(summary["audit_disagreements"], 1)
            self.assertAlmostEqual(summary["audit_disagreement_rate"], 0.5)


if __name__ == "__main__":
    unittest.main()
