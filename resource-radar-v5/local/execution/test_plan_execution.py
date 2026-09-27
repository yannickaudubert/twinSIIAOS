import unittest

from plan_execution import compose_plan


class ExecutionPlannerTests(unittest.TestCase):
    def setUp(self):
        self.estate = {
            "id": "estate:test",
            "hardware": {
                "memory": {"ram_mb": 32768},
                "accelerators": [{"kind": "gpu", "model": "test-gpu", "vram_mb": 16384}],
                "storage": [{"id": "nvme", "kind": "nvme", "free_gb": 500}],
            },
            "software": {
                "model_servers": ["lm-studio"],
                "service_ids": ["local-search"],
                "tool_ids": ["python"],
            },
            "policy": {
                "incremental_budget_eur": 0,
                "local_first": True,
                "external_provider_dependency_allowed": False,
            },
        }
        self.workload = {
            "id": "workload:test",
            "required_capabilities": [
                {"capability": "classification", "priority": "required"}
            ],
            "constraints": {
                "incremental_budget_eur": 0,
                "local_only": True,
            },
        }

    def test_zero_budget_local_plan_is_feasible(self):
        profiles = [{
            "id": "profile:local",
            "resource_id": "model:local",
            "mode": {"name": "local-q4"},
            "requirements": {
                "min_ram_mb": 8192,
                "min_vram_mb": 8192,
                "storage_gb": 20,
                "runtime_ids": ["lm-studio"],
            },
            "capabilities": ["classification"],
            "cost": {"incremental_eur": 0},
            "provenance": {
                "method": "benchmarked",
                "observed_at": "2026-09-27T00:00:00Z",
                "evidence_ids": ["evidence:test"],
            },
        }]
        plan = compose_plan(self.estate, self.workload, profiles)
        self.assertEqual(plan["feasibility"]["status"], "feasible")
        self.assertEqual(plan["cost"]["incremental_eur"], 0)
        self.assertFalse(plan["cost"]["external_dependencies_required"])
        self.assertEqual(plan["steps"][0]["resource_ids"], ["model:local"])

    def test_unknown_cost_is_not_treated_as_free(self):
        profiles = [{
            "id": "profile:unknown-cost",
            "resource_id": "model:unknown-cost",
            "mode": {"name": "local"},
            "requirements": {"min_ram_mb": 1024},
            "capabilities": ["classification"],
            "provenance": {"method": "declared", "observed_at": "2026-09-27T00:00:00Z"},
        }]
        plan = compose_plan(self.estate, self.workload, profiles)
        self.assertEqual(plan["feasibility"]["status"], "unknown")
        self.assertTrue(any("cout incremental non observe" in item for item in plan["gap_analysis"]["rejected_options"]))

    def test_quality_floor_without_quality_evidence_is_unknown(self):
        workload = dict(self.workload)
        workload["required_capabilities"] = [{"capability": "classification", "priority": "required", "quality_floor": "high"}]
        profiles = [{
            "id": "profile:no-quality-proof",
            "resource_id": "model:no-quality-proof",
            "mode": {"name": "local"},
            "requirements": {"min_ram_mb": 1024},
            "capabilities": ["classification"],
            "cost": {"incremental_eur": 0},
            "provenance": {"method": "declared", "observed_at": "2026-09-27T00:00:00Z"},
        }]
        plan = compose_plan(self.estate, workload, profiles)
        self.assertEqual(plan["feasibility"]["status"], "unknown")
        self.assertTrue(any("qualite non prouvee" in item for item in plan["gap_analysis"]["rejected_options"]))

    def test_quality_floor_on_other_profile_capability_does_not_poison_current_capability(self):
        workload = dict(self.workload)
        workload["required_capabilities"] = [
            {"capability": "classification", "priority": "required"},
            {"capability": "summarization", "priority": "preferred", "quality_floor": "high"}
        ]
        profiles = [{
            "id": "profile:multi",
            "resource_id": "tool:multi",
            "mode": {"name": "local"},
            "requirements": {"min_ram_mb": 1024},
            "capabilities": ["classification", "summarization"],
            "quality_claims": [{"capability": "classification", "level": "basic", "evidence_ids": ["evidence:basic"]}],
            "cost": {"incremental_eur": 0},
            "provenance": {"method": "declared", "observed_at": "2026-09-27T00:00:00Z"},
        }]
        plan = compose_plan(self.estate, workload, profiles)
        self.assertTrue(any(step["capability"] == "classification" for step in plan["steps"]))

    def test_insufficient_vram_creates_gap_without_cloud_fallback(self):
        profiles = [{
            "id": "profile:too-large",
            "resource_id": "model:too-large",
            "mode": {"name": "native"},
            "requirements": {"min_vram_mb": 24000},
            "capabilities": ["classification"],
            "cost": {"incremental_eur": 0},
            "provenance": {"method": "declared", "observed_at": "2026-09-27T00:00:00Z"},
        }]
        plan = compose_plan(self.estate, self.workload, profiles)
        self.assertEqual(plan["feasibility"]["status"], "not_feasible")
        self.assertEqual(plan["gap_analysis"]["uncovered_capabilities"], ["classification"])
        self.assertFalse(plan["cost"]["external_dependencies_required"])
        self.assertIn("VRAM insuffisante", plan["gap_analysis"]["rejected_options"][0])


if __name__ == "__main__":
    unittest.main()
