import json
import sys
import unittest
from copy import deepcopy
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXECUTION = HERE.parent / "local" / "execution"
sys.path.insert(0, str(EXECUTION))

from plan_execution import compose_plan  # noqa: E402


def load(relative):
    return json.loads((HERE / relative).read_text(encoding="utf-8"))


class CompositionDecisionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sandy = load("personas/sandy-zero-budget.json")
        cls.profiles = load("profiles/common-profiles.json")
        cls.classify = load("workloads/classify-confidential-zero-budget.json")

    def test_32_duplicate_capability_is_planned_once(self):
        workload = deepcopy(self.classify)
        workload["required_capabilities"] = [
            {"capability":"classification","priority":"required"},
            {"capability":"classification","priority":"preferred"},
        ]
        plan = compose_plan(self.sandy, workload, self.profiles)
        self.assertEqual([s["capability"] for s in plan["steps"]], ["classification"])

    def test_33_required_priority_wins_over_duplicate_preferred(self):
        workload = deepcopy(self.classify)
        workload["required_capabilities"] = [
            {"capability":"classification","priority":"preferred"},
            {"capability":"classification","priority":"required"},
        ]
        plan = compose_plan(self.sandy, workload, self.profiles)
        self.assertEqual(plan["feasibility"]["status"], "feasible")
        self.assertEqual(len(plan["steps"]), 1)

    def test_34_two_required_capabilities_create_two_steps(self):
        workload = deepcopy(self.classify)
        workload["required_capabilities"] = [
            {"capability":"classification","priority":"required"},
            {"capability":"summarization","priority":"required"},
        ]
        plan = compose_plan(self.sandy, workload, self.profiles)
        self.assertEqual(plan["feasibility"]["status"], "feasible")
        self.assertEqual({s["capability"] for s in plan["steps"]}, {"classification","summarization"})

    def test_35_gap_on_one_required_capability_preserves_feasible_steps(self):
        workload = deepcopy(self.classify)
        workload["required_capabilities"] = [
            {"capability":"classification","priority":"required"},
            {"capability":"missing-capability","priority":"required"},
        ]
        plan = compose_plan(self.sandy, workload, self.profiles)
        self.assertEqual(plan["feasibility"]["status"], "not_feasible")
        self.assertTrue(any(s["capability"] == "classification" for s in plan["steps"]))
        self.assertEqual(plan["gap_analysis"]["uncovered_capabilities"], ["missing-capability"])

    def test_36_available_preferred_capability_is_added_without_becoming_required(self):
        workload = deepcopy(self.classify)
        workload["required_capabilities"].append({"capability":"summarization","priority":"preferred"})
        plan = compose_plan(self.sandy, workload, self.profiles)
        self.assertEqual(plan["feasibility"]["status"], "feasible")
        self.assertEqual({s["capability"] for s in plan["steps"]}, {"classification","summarization"})

    def test_37_evidence_union_contains_all_selected_profiles(self):
        workload = deepcopy(self.classify)
        workload["required_capabilities"] = [
            {"capability":"classification","priority":"required"},
            {"capability":"summarization","priority":"required"},
        ]
        plan = compose_plan(self.sandy, workload, self.profiles)
        self.assertIn("evidence:python", plan["evidence_ids"])
        self.assertIn("evidence:local-q4", plan["evidence_ids"])

    def test_38_human_fallback_beats_external_required(self):
        workload = deepcopy(self.classify)
        workload["required_capabilities"] = [{"capability":"manual-review","priority":"required"}]
        human = {
            "id":"profile:human-review","resource_id":"role:human",
            "mode":{"name":"human review","execution_mode":"human"},
            "requirements":{},"capabilities":["manual-review"],
            "cost":{"incremental_eur":0},
            "provenance":{"method":"manually_verified","observed_at":"2026-09-27T08:00:00Z","evidence_ids":["evidence:human"]},
            "visibility":"local_private"
        }
        external = {
            "id":"profile:external-review","resource_id":"service:external-review",
            "mode":{"name":"external review","execution_mode":"external_required"},
            "requirements":{},"capabilities":["manual-review"],
            "cost":{"incremental_eur":0,"external_dependency":"external-review","external_required":True},
            "provenance":{"method":"declared","observed_at":"2026-09-27T08:00:00Z"},
            "visibility":"local_private"
        }
        plan = compose_plan(self.sandy, workload, [external,human])
        self.assertEqual(plan["steps"][0]["execution_mode"], "human")

    def test_39_external_optional_is_not_preferred_over_local_model(self):
        workload = {
            "id":"workload:drafting","title":"Draft","intent":"Draft locally",
            "required_capabilities":[{"capability":"drafting","priority":"required"}],
            "constraints":{"incremental_budget_eur":0,"privacy_class":"internal","local_only":False,"offline_required":False,"human_gate":False,"allowed_external_providers":["external-optional"]},
            "visibility":"local_private"
        }
        estate = deepcopy(self.sandy)
        estate["policy"]["external_provider_dependency_allowed"] = True
        local = deepcopy(next(p for p in self.profiles if p["resource_id"]=="model:small-local"))
        optional = {
            "id":"profile:external-optional","resource_id":"service:external-optional",
            "mode":{"name":"external optional","execution_mode":"external_optional"},
            "requirements":{},"capabilities":["drafting"],
            "cost":{"incremental_eur":0,"external_dependency":"external-optional","external_required":False},
            "provenance":{"method":"declared","observed_at":"2026-09-27T08:00:00Z"},
            "visibility":"local_private"
        }
        plan = compose_plan(estate, workload, [optional, local])
        self.assertEqual(plan["steps"][0]["resource_ids"], ["model:small-local"])

    def test_40_node_references_without_observed_resources_do_not_create_fake_capacity(self):
        estate = deepcopy(self.sandy)
        estate["hardware"] = {"cpu":{"architecture":"x86_64"},"memory":{}}
        estate["network"]["node_ids"] = ["node:secondary"]
        profile = deepcopy(next(p for p in self.profiles if p["resource_id"]=="model:small-local"))
        plan = compose_plan(estate, {
            "id":"workload:node-test","title":"Node test","intent":"Use cluster",
            "required_capabilities":[{"capability":"summarization","priority":"required"}],
            "constraints":{"incremental_budget_eur":0,"privacy_class":"internal","local_only":True,"offline_required":False,"human_gate":False,"allowed_external_providers":[]},
            "visibility":"local_private"
        }, [profile])
        self.assertEqual(plan["feasibility"]["status"], "unknown")
        self.assertIn("summarization", plan["gap_analysis"]["unknown_capabilities"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
