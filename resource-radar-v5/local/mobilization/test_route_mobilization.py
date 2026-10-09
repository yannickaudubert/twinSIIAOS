import unittest
from copy import deepcopy

from route_mobilization import route_mobilization


BASE = {
    "id": "route:test",
    "unknowns": [],
    "execution": {"status": "feasible"},
    "admission": {"verdict": "eligible"},
    "complexity": {
        "technical": 1, "organisational": 1, "financial": 0,
        "legal_regulatory": 0, "security": 1, "data": 1,
        "human_change": 0, "territorial_ecosystem": 0, "urgency": 1
    },
    "needs": {
        "required_capabilities": ["local-analysis"],
        "required_domains": [],
        "human_judgement_required": False,
        "structured_delivery_required": False,
        "collective_coordination_required": False,
        "self_service_gap": [],
        "authority_scope": []
    },
    "context_boundary": {
        "shareable_fields": ["public_problem_statement"],
        "local_only_fields": ["estate", "client_data"]
    },
    "evidence_ids": ["evidence:test"]
}


class MobilizationRoutingTests(unittest.TestCase):
    def test_61_local_self_service_is_default_when_sufficient(self):
        result = route_mobilization(BASE)
        self.assertEqual(result["route"], "siiaos_local")
        self.assertFalse(result["mandate"]["required"])

    def test_62_unknown_execution_does_not_create_a_mission(self):
        ctx = deepcopy(BASE)
        ctx["execution"]["status"] = "unknown"
        ctx["unknowns"] = ["VRAM non observee"]
        result = route_mobilization(ctx)
        self.assertEqual(result["route"], "no_activation")

    def test_63_blocked_admission_does_not_create_a_mission(self):
        ctx = deepcopy(BASE)
        ctx["admission"] = {"verdict": "blocked", "blocking_reasons": ["policy"]}
        result = route_mobilization(ctx)
        self.assertEqual(result["route"], "no_activation")

    def test_64_human_judgement_routes_to_consultant(self):
        ctx = deepcopy(BASE)
        ctx["needs"]["human_judgement_required"] = True
        result = route_mobilization(ctx)
        self.assertEqual(result["route"], "yannick_consultant")
        self.assertTrue(result["mandate"]["human_gate"])

    def test_65_structured_delivery_routes_to_augmented_cabinet(self):
        ctx = deepcopy(BASE)
        ctx["needs"]["structured_delivery_required"] = True
        result = route_mobilization(ctx)
        self.assertEqual(result["route"], "cabinet_augmente")
        self.assertTrue(result["context_boundary"]["context_pack_required"])

    def test_66_two_domains_route_to_agoria(self):
        ctx = deepcopy(BASE)
        ctx["needs"]["required_domains"] = ["finance", "change"]
        result = route_mobilization(ctx)
        self.assertEqual(result["route"], "agoria_collective")
        self.assertEqual(result["team_shape"], "multi_domain")

    def test_67_collective_coordination_routes_to_agoria_even_single_domain(self):
        ctx = deepcopy(BASE)
        ctx["needs"]["required_domains"] = ["territory"]
        ctx["needs"]["collective_coordination_required"] = True
        result = route_mobilization(ctx)
        self.assertEqual(result["route"], "agoria_collective")
        self.assertEqual(result["team_shape"], "single_specialist")

    def test_68_territorial_complexity_can_trigger_collective_route(self):
        ctx = deepcopy(BASE)
        ctx["complexity"]["territorial_ecosystem"] = 3
        result = route_mobilization(ctx)
        self.assertEqual(result["route"], "agoria_collective")

    def test_69_high_organisational_change_routes_to_cabinet(self):
        ctx = deepcopy(BASE)
        ctx["complexity"]["organisational"] = 3
        result = route_mobilization(ctx)
        self.assertEqual(result["route"], "cabinet_augmente")

    def test_70_admission_human_gate_never_stays_silent_local_execution(self):
        ctx = deepcopy(BASE)
        ctx["admission"] = {"verdict": "human_gate"}
        result = route_mobilization(ctx)
        self.assertEqual(result["route"], "yannick_consultant")
        self.assertTrue(result["mandate"]["required"])

    def test_71_local_only_context_is_not_promoted_to_shareable(self):
        result = route_mobilization(BASE)
        self.assertIn("estate", result["context_boundary"]["local_only_fields"])
        self.assertNotIn("estate", result["context_boundary"]["shareable_fields"])

    def test_72_agoria_route_is_proposed_not_activated(self):
        ctx = deepcopy(BASE)
        ctx["needs"]["required_domains"] = ["finance", "technology"]
        result = route_mobilization(ctx)
        self.assertEqual(result["state"], "proposed")
        self.assertTrue(result["mandate"]["client_or_user_acceptance_required"])


if __name__ == "__main__":
    unittest.main()
