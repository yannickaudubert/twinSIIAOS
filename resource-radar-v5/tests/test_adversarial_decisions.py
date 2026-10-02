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


class AdversarialDecisionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sandy = load("personas/sandy-zero-budget.json")
        cls.office = load("personas/office-laptop-8gb.json")
        cls.profiles = load("profiles/common-profiles.json")
        cls.summarize = load("workloads/summarize-zero-budget.json")
        cls.classify = load("workloads/classify-confidential-zero-budget.json")

    def test_13_offline_required_blocks_external_even_if_provider_policy_allows(self):
        estate = deepcopy(self.sandy)
        estate["policy"]["external_provider_dependency_allowed"] = True
        workload = deepcopy(self.summarize)
        workload["constraints"]["local_only"] = False
        workload["constraints"]["offline_required"] = True
        external = [p for p in self.profiles if p["resource_id"] == "service:external-api"]
        plan = compose_plan(estate, workload, external)
        self.assertEqual(plan["feasibility"]["status"], "not_feasible")
        self.assertTrue(any("provider externe interdit" in item for item in plan["gap_analysis"]["rejected_options"]))

    def test_14_privacy_class_forces_local_even_without_workload_local_only_flag(self):
        estate = deepcopy(self.sandy)
        estate["policy"]["external_provider_dependency_allowed"] = True
        workload = deepcopy(self.classify)
        workload["constraints"]["local_only"] = False
        external = [p for p in self.profiles if p["resource_id"] == "service:external-api"]
        plan = compose_plan(estate, workload, external)
        self.assertEqual(plan["feasibility"]["status"], "not_feasible")
        self.assertTrue(any("provider externe interdit" in item for item in plan["gap_analysis"]["rejected_options"]))

    def test_15_storage_pressure_rejects_profile(self):
        estate = deepcopy(self.sandy)
        estate["hardware"]["storage"][0]["free_gb"] = 2
        local = [p for p in self.profiles if p["resource_id"] == "model:small-local"]
        plan = compose_plan(estate, self.summarize, local)
        self.assertEqual(plan["feasibility"]["status"], "not_feasible")
        self.assertTrue(any("stockage libre insuffisant" in item for item in plan["gap_analysis"]["rejected_options"]))

    def test_16_deterministic_beats_local_model_when_both_cover_same_capability(self):
        model = deepcopy(next(p for p in self.profiles if p["resource_id"] == "model:small-local"))
        model["capabilities"] = ["classification"]
        profiles = [model, next(p for p in self.profiles if p["resource_id"] == "tool:python")]
        plan = compose_plan(self.sandy, self.classify, profiles)
        self.assertEqual(plan["steps"][0]["execution_mode"], "deterministic")

    def test_17_cheaper_profile_wins_within_same_execution_mode(self):
        base = deepcopy(next(p for p in self.profiles if p["resource_id"] == "model:small-local"))
        expensive = deepcopy(base)
        expensive["id"] = "profile:expensive-local"
        expensive["resource_id"] = "model:expensive-local"
        expensive["cost"]["incremental_eur"] = 5
        workload = deepcopy(self.summarize)
        workload["constraints"]["incremental_budget_eur"] = 10
        estate = deepcopy(self.sandy)
        estate["policy"]["incremental_budget_eur"] = 10
        plan = compose_plan(estate, workload, [expensive, base])
        self.assertEqual(plan["steps"][0]["resource_ids"], ["model:small-local"])

    def test_18_external_can_be_used_only_when_policy_and_budget_both_allow_it(self):
        estate = deepcopy(self.sandy)
        estate["policy"]["external_provider_dependency_allowed"] = True
        estate["policy"]["incremental_budget_eur"] = 50
        workload = deepcopy(self.summarize)
        workload["constraints"]["local_only"] = False
        workload["constraints"]["privacy_class"] = "public"
        workload["constraints"]["incremental_budget_eur"] = 50
        workload["constraints"]["allowed_external_providers"] = ["external-api"]
        external = [p for p in self.profiles if p["resource_id"] == "service:external-api"]
        plan = compose_plan(estate, workload, external)
        self.assertEqual(plan["feasibility"]["status"], "feasible")
        self.assertTrue(plan["cost"]["external_dependencies_required"])
        self.assertEqual(plan["cost"]["incremental_eur"], 20)

    def test_19_external_provider_requires_explicit_workload_allowlist(self):
        estate = deepcopy(self.sandy)
        estate["policy"]["external_provider_dependency_allowed"] = True
        estate["policy"]["incremental_budget_eur"] = 50
        workload = deepcopy(self.summarize)
        workload["constraints"]["local_only"] = False
        workload["constraints"]["privacy_class"] = "public"
        workload["constraints"]["incremental_budget_eur"] = 50
        workload["constraints"]["allowed_external_providers"] = []
        external = [p for p in self.profiles if p["resource_id"] == "service:external-api"]
        plan = compose_plan(estate, workload, external)
        self.assertEqual(plan["feasibility"]["status"], "not_feasible")
        self.assertTrue(any("aucun provider externe explicitement autorise" in item for item in plan["gap_analysis"]["rejected_options"]))

    def test_20_unknown_storage_remains_unknown_not_insufficient(self):
        estate = deepcopy(self.sandy)
        estate["hardware"].pop("storage", None)
        local = [p for p in self.profiles if p["resource_id"] == "model:small-local"]
        plan = compose_plan(estate, self.summarize, local)
        self.assertEqual(plan["feasibility"]["status"], "unknown")
        joined = " ".join(plan["gap_analysis"]["rejected_options"])
        self.assertIn("stockage libre non observe", joined)
        self.assertNotIn("stockage libre insuffisant", joined)

    def test_21_zero_budget_rejects_paid_local_tool_too(self):
        paid_local = {
            "id":"profile:paid-local",
            "resource_id":"tool:paid-local",
            "mode":{"name":"paid local","execution_mode":"local_service"},
            "requirements":{"runtime_ids":["python"]},
            "capabilities":["classification"],
            "cost":{"incremental_eur":25,"external_required":False},
            "provenance":{"method":"declared","observed_at":"2026-09-27T08:00:00Z"},
            "visibility":"local_private",
        }
        plan = compose_plan(self.sandy, self.classify, [paid_local])
        self.assertEqual(plan["feasibility"]["status"], "not_feasible")
        self.assertTrue(any("cout incremental hors budget" in item for item in plan["gap_analysis"]["rejected_options"]))

    def test_22_missing_required_service_is_explicit(self):
        profile = {
            "id":"profile:needs-index",
            "resource_id":"tool:indexed",
            "mode":{"name":"indexed","execution_mode":"local_service"},
            "requirements":{"service_ids":["missing-index"]},
            "capabilities":["classification"],
            "cost":{"incremental_eur":0},
            "provenance":{"method":"declared","observed_at":"2026-09-27T08:00:00Z"},
            "visibility":"local_private",
        }
        plan = compose_plan(self.sandy, self.classify, [profile])
        self.assertEqual(plan["feasibility"]["status"], "not_feasible")
        self.assertTrue(any("services absents: missing-index" in item for item in plan["gap_analysis"]["rejected_options"]))

    def test_23_no_profile_for_required_capability_is_real_gap(self):
        workload = deepcopy(self.classify)
        workload["required_capabilities"] = [{"capability":"quantum-telepathy","priority":"required"}]
        plan = compose_plan(self.sandy, workload, self.profiles)
        self.assertEqual(plan["feasibility"]["status"], "not_feasible")
        self.assertEqual(plan["gap_analysis"]["uncovered_capabilities"], ["quantum-telepathy"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
