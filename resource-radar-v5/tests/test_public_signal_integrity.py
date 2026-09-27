import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FIXTURE = ROOT.parent / "ui" / "fixtures" / "radar-public.demo.json"


class PublicSignalIntegrityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(FIXTURE.read_text(encoding="utf-8"))
        cls.items = {item["id"]: item for item in cls.data["items"]}

    def test_23_fixture_is_explicitly_marked_as_fixture(self):
        self.assertIs(self.data.get("fixture"), True)
        self.assertIn("Ne pas publier", self.data.get("note", ""))

    def test_24_public_fixture_contains_no_private_execution_objects(self):
        forbidden = {
            "execution_estate", "execution_profile", "workload", "execution_plan",
            "estate_id", "workload_id", "control_profile", "augmentation"
        }
        for item in self.data["items"]:
            self.assertFalse(forbidden.intersection(item.keys()), item["id"])

    def test_25_deprecated_resource_is_explicitly_deprecated(self):
        flowise = self.items["workflow-flowise"]
        self.assertEqual(flowise["state"], "deprecated")
        self.assertLess(flowise["trend"]["delta_30d"], 0)
        self.assertTrue(any("archiv" in gap.lower() for gap in flowise["known_gaps"]))

    def test_26_observed_resource_with_evidence_is_not_silently_tested(self):
        vllm = self.items["runtime-vllm"]
        self.assertGreater(vllm["expert_available"]["evidence_count"], 0)
        self.assertEqual(vllm["state"], "observed")

    def test_27_public_explanation_states_what_resource_does_not_replace(self):
        qdrant = self.items["db-qdrant"]
        explanation = qdrant["public_explanation"]
        self.assertTrue(explanation["does_not_replace"])
        self.assertTrue(explanation["questions_to_ask"])

    def test_28_license_boundary_is_visible_in_public_metadata(self):
        phoenix = self.items["observability-phoenix"]
        langfuse = self.items["observability-langfuse"]
        self.assertIn("Elastic License", phoenix["license"])
        self.assertIn("Enterprise", langfuse["license"])

    def test_29_known_gap_survives_even_for_high_maturity_resource(self):
        n8n = self.items["workflow-n8n"]
        self.assertEqual(n8n["maturity"], "high")
        self.assertTrue(n8n["known_gaps"])

    def test_30_public_items_keep_verification_dates(self):
        for item in self.data["items"]:
            self.assertTrue(item.get("last_verified_at"), item["id"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
