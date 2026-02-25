import unittest

from orchestrator.policy_gate import evaluate_policy_gate, RouteDecision


class PolicyGateTests(unittest.TestCase):
    def test_missing_policy_defaults_to_auto_review(self):
        result = evaluate_policy_gate("T1", None, None)
        self.assertEqual(result.decision, RouteDecision.AUTO_REVIEW)

    def test_mandatory_evidence_failure_returns_no_go(self):
        policy = {
            "auto_review_enabled": True,
            "auto_approve_enabled": False,
            "enforce_mandatory_evidence": True,
        }
        evidence = {
            "acceptance_evidence": "PASS",
            "verification_results": "FAIL",
        }
        result = evaluate_policy_gate("T1", policy, evidence)
        self.assertEqual(result.decision, RouteDecision.NO_GO)
        self.assertIn("verification_results", result.failed_criteria)

    def test_t2_with_passing_evidence_routes_human_queue(self):
        policy = {
            "auto_review_enabled": True,
            "enforce_mandatory_evidence": True,
        }
        evidence = {
            "acceptance_evidence": "PASS",
            "verification_results": "PASS",
            "operational_readiness": "PASS",
        }
        result = evaluate_policy_gate("T2", policy, evidence)
        self.assertEqual(result.decision, RouteDecision.HUMAN_QUEUE)

    def test_t0_auto_approve_when_enabled(self):
        policy = {
            "auto_review_enabled": True,
            "auto_approve_enabled": True,
            "enforce_mandatory_evidence": True,
        }
        evidence = {
            "acceptance_evidence": "PASS",
            "verification_results": "PASS",
        }
        result = evaluate_policy_gate("T0", policy, evidence)
        self.assertEqual(result.decision, RouteDecision.AUTO_APPROVE)

    def test_requirement_coverage_blocking_can_force_no_go(self):
        policy = {
            "auto_review_enabled": True,
            "enforce_mandatory_evidence": True,
            "requirement_coverage": {
                "enabled": True,
                "mode": "blocking",
                "min_coverage_percent": 80,
                "measured_percent": 60,
            },
        }
        evidence = {
            "acceptance_evidence": "PASS",
            "verification_results": "PASS",
        }
        result = evaluate_policy_gate("T1", policy, evidence)
        self.assertEqual(result.decision, RouteDecision.NO_GO)
        self.assertIn("requirement_coverage", result.failed_criteria)

    def test_requirement_coverage_advisory_only_warns(self):
        policy = {
            "auto_review_enabled": True,
            "enforce_mandatory_evidence": True,
            "requirement_coverage": {
                "enabled": True,
                "mode": "advisory",
                "min_coverage_percent": 80,
                "measured_percent": 60,
            },
        }
        evidence = {
            "acceptance_evidence": "PASS",
            "verification_results": "PASS",
        }
        result = evaluate_policy_gate("T1", policy, evidence)
        self.assertEqual(result.decision, RouteDecision.AUTO_REVIEW)
        self.assertGreater(len(result.warnings), 0)


if __name__ == "__main__":
    unittest.main()
