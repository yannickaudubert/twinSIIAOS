import unittest
from copy import deepcopy

from assess_admission import assess_admission


BASE_CONTEXT = {
    "id": "org:test",
    "maturity": {
        "governance": 2, "delivery": 2, "operations": 2, "observability": 2,
        "security": 2, "data": 2, "ai_usage": 2, "automation": 2,
        "open_source": 2, "human_control": 2
    },
    "risk_policy": {
        "human_gate_from": "R3",
        "max_autonomous_risk": "R2",
        "allow_external_writes": False,
        "allow_shell_access": False,
        "allow_elevated_privileges": False
    },
    "visibility": "local_private"
}

BASE_PROFILE = {
    "id": "admission:test",
    "resource_id": "tool:test",
    "admission_state": "candidate",
    "risk_class": "R1",
    "maturity_min": {"governance": 1, "security": 1},
    "permissions": {"shell_access": False, "privilege_level": "user"},
    "network": {"external_writes": False},
    "reversibility": {"rollback_defined": True},
    "evidence_ids": ["evidence:test"],
    "visibility": "local_private"
}


class AdmissionDecisionTests(unittest.TestCase):
    def test_41_low_risk_candidate_is_eligible(self):
        result = assess_admission(BASE_PROFILE, BASE_CONTEXT)
        self.assertEqual(result["verdict"], "eligible")

    def test_42_r3_requires_human_gate_even_when_otherwise_eligible(self):
        profile = deepcopy(BASE_PROFILE)
        profile["risk_class"] = "R3"
        result = assess_admission(profile, BASE_CONTEXT)
        self.assertEqual(result["verdict"], "human_gate")
        self.assertTrue(result["human_gate_reasons"])

    def test_43_r4_requires_human_gate(self):
        profile = deepcopy(BASE_PROFILE)
        profile["risk_class"] = "R4"
        result = assess_admission(profile, BASE_CONTEXT)
        self.assertEqual(result["verdict"], "human_gate")

    def test_44_maturity_gap_blocks_admission(self):
        profile = deepcopy(BASE_PROFILE)
        profile["maturity_min"]["security"] = 4
        result = assess_admission(profile, BASE_CONTEXT)
        self.assertEqual(result["verdict"], "blocked")
        self.assertIn("security", result["maturity_gaps"])

    def test_45_hold_state_blocks_even_low_risk_resource(self):
        profile = deepcopy(BASE_PROFILE)
        profile["admission_state"] = "hold"
        result = assess_admission(profile, BASE_CONTEXT)
        self.assertEqual(result["verdict"], "blocked")

    def test_46_shell_permission_can_block_technical_candidate(self):
        profile = deepcopy(BASE_PROFILE)
        profile["permissions"]["shell_access"] = True
        result = assess_admission(profile, BASE_CONTEXT)
        self.assertEqual(result["verdict"], "blocked")
        self.assertTrue(any("shell" in reason for reason in result["blocking_reasons"]))

    def test_47_external_write_policy_blocks_resource(self):
        profile = deepcopy(BASE_PROFILE)
        profile["network"]["external_writes"] = True
        result = assess_admission(profile, BASE_CONTEXT)
        self.assertEqual(result["verdict"], "blocked")

    def test_48_missing_maturity_dimension_stays_unknown(self):
        context = deepcopy(BASE_CONTEXT)
        context["maturity"].pop("security")
        result = assess_admission(BASE_PROFILE, context)
        self.assertEqual(result["verdict"], "unknown")
        self.assertTrue(any("security" in item for item in result["unknowns"]))

    def test_49_admitted_resource_without_rollback_is_blocked(self):
        profile = deepcopy(BASE_PROFILE)
        profile["admission_state"] = "admitted"
        profile["reversibility"]["rollback_defined"] = False
        result = assess_admission(profile, BASE_CONTEXT)
        self.assertEqual(result["verdict"], "blocked")

    def test_50_evidence_references_survive_assessment(self):
        result = assess_admission(BASE_PROFILE, BASE_CONTEXT)
        self.assertEqual(result["evidence_ids"], ["evidence:test"])


if __name__ == "__main__":
    unittest.main()
