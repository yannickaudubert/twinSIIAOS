import json
import sys
import unittest
from copy import deepcopy
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXECUTION = HERE.parents[1] / "local" / "execution"
sys.path.insert(0, str(EXECUTION))

from plan_execution import compose_plan  # noqa: E402


def load(relative: str):
    return json.loads((HERE / relative).read_text(encoding="utf-8"))


class UserDecisionSimulationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sandy = load("personas/sandy-zero-budget.json")
        cls.office = load("personas/office-laptop-8gb.json")
        cls.unknown_gpu = load("personas/unknown-gpu.json")
        cls.profiles = load("profiles/common-profiles.json")
        cls.classify = load("workloads/classify-confidential-zero-budget.json")
        cls.summarize = load("workloads/summarize-zero-budget.json")
        cls.gpu_unknown = load("workloads/gpu-dependent-unknown.json")

    def test_01_sandy_prefers_deterministic_for_classification(self):
        plan = compose_plan(self.sandy, self.classify, self.profiles)
        self.assertEqual(plan["feasibility"]["status"], "feasible")
        self.assertEqual(plan["steps"][0]["execution_mode"], "deterministic")
        self.assertEqual(plan["steps"][0]["resource_ids"], ["tool:python"])

    def test_02_zero_budget_stays_zero(self):
        plan = compose_plan(self.sandy, self.summarize, self.profiles)
        self.assertEqual(plan["cost"]["incremental_eur"], 0)
        self.assertFalse(plan["cost"]["external_dependencies_required"])

    def test_03_local_only_never_selects_external_required(self):
        plan = compose_plan(self.sandy, self.summarize, self.profiles)
        self.assertNotIn("external_required", [step["execution_mode"] for step in plan["steps"]])
        self.assertEqual(plan["cost"]["external_dependencies"], [])

    def test_04_large_model_rejected_then_smaller_local_substitute_selected(self):
        plan = compose_plan(self.sandy, self.summarize, self.profiles)
        self.assertEqual(plan["feasibility"]["status"], "feasible")
        self.assertEqual(plan["steps"][0]["resource_ids"], ["model:small-local"])
        self.assertTrue(any("large-local-model" in item for item in plan["gap_analysis"]["rejected_options"]))
        self.assertTrue(any("profile:large-local-model -> profile:small-local-model" in item for item in plan["gap_analysis"]["substitutions_considered"]))

    def test_05_unknown_gpu_is_not_reported_as_insufficient(self):
        plan = compose_plan(self.unknown_gpu, self.gpu_unknown, self.profiles)
        self.assertEqual(plan["feasibility"]["status"], "unknown")
        joined = " ".join(plan["gap_analysis"]["rejected_options"])
        self.assertIn("VRAM non observee", joined)
        self.assertNotIn("VRAM insuffisante", joined)

    def test_06_office_laptop_can_use_existing_python_without_purchase(self):
        plan = compose_plan(self.office, self.classify, self.profiles)
        self.assertEqual(plan["feasibility"]["status"], "feasible")
        self.assertEqual(plan["steps"][0]["resource_ids"], ["tool:python"])
        self.assertEqual(plan["cost"]["incremental_eur"], 0)

    def test_07_missing_model_runtime_creates_real_gap(self):
        estate = deepcopy(self.sandy)
        estate["software"]["model_servers"] = []
        profiles = [p for p in self.profiles if p["resource_id"] != "service:external-api"]
        plan = compose_plan(estate, self.summarize, profiles)
        self.assertEqual(plan["feasibility"]["status"], "not_feasible")
        self.assertEqual(plan["gap_analysis"]["uncovered_capabilities"], ["summarization"])
        self.assertTrue(any("runtimes absents: lm-studio" in item for item in plan["gap_analysis"]["rejected_options"]))

    def test_08_external_api_is_rejected_by_zero_budget_even_if_policy_allows_external(self):
        estate = deepcopy(self.sandy)
        estate["policy"]["external_provider_dependency_allowed"] = True
        workload = deepcopy(self.summarize)
        workload["constraints"]["local_only"] = False
        only_external = [p for p in self.profiles if p["resource_id"] == "service:external-api"]
        plan = compose_plan(estate, workload, only_external)
        self.assertEqual(plan["feasibility"]["status"], "not_feasible")
        self.assertTrue(any("cout incremental hors budget" in item for item in plan["gap_analysis"]["rejected_options"]))

    def test_09_evidence_from_selected_profile_is_preserved(self):
        plan = compose_plan(self.sandy, self.summarize, self.profiles)
        self.assertIn("evidence:local-q4", plan["evidence_ids"])
        self.assertIn("evidence:local-q4", plan["steps"][0]["evidence_ids"])

    def test_10_preferred_capability_failure_does_not_block_required_work(self):
        workload = deepcopy(self.classify)
        workload["required_capabilities"].append({"capability": "nonexistent-optional", "priority": "preferred"})
        plan = compose_plan(self.sandy, workload, self.profiles)
        self.assertEqual(plan["feasibility"]["status"], "feasible")
        self.assertEqual(plan["gap_analysis"]["uncovered_capabilities"], [])

    def test_11_unknown_required_capability_blocks_qualification_without_fake_gap(self):
        profile = {
            "id": "profile:needs-unobserved-gpu",
            "resource_id": "model:gpu-only",
            "mode": {"name": "gpu-only", "execution_mode": "local_model"},
            "requirements": {"min_vram_mb": 1000},
            "capabilities": ["special-analysis"],
            "cost": {"incremental_eur": 0},
            "provenance": {"method": "declared", "observed_at": "2026-09-27T08:00:00Z"},
            "visibility": "local_private",
        }
        workload = deepcopy(self.gpu_unknown)
        workload["required_capabilities"] = [{"capability": "special-analysis", "priority": "required"}]
        plan = compose_plan(self.unknown_gpu, workload, [profile])
        self.assertEqual(plan["feasibility"]["status"], "unknown")
        self.assertEqual(plan["gap_analysis"]["unknown_capabilities"], ["special-analysis"])
        self.assertEqual(plan["gap_analysis"]["uncovered_capabilities"], [])

    def test_12_confidential_workload_never_adds_external_dependency(self):
        plan = compose_plan(self.sandy, self.classify, self.profiles)
        self.assertEqual(plan["cost"]["external_dependencies"], [])
        self.assertFalse(plan["cost"]["external_dependencies_required"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
