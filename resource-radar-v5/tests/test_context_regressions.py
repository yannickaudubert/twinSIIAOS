import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACTS = ROOT / "contracts"


def load(name):
    return json.loads((CONTRACTS / name).read_text(encoding="utf-8"))


class ContextRegressionTests(unittest.TestCase):
    def test_54_resource_truth_states_include_proven_rejected_watch_unknown(self):
        schema = load("resource-record.schema.json")
        states = set(schema["properties"]["state"]["enum"])
        self.assertTrue({"proven","rejected","watch","unknown"} <= states)

    def test_55_resource_kinds_preserve_repo_deployment_runtime_authority_distinction(self):
        schema = load("resource-record.schema.json")
        kinds = set(schema["properties"]["kind"]["enum"])
        self.assertTrue({"repository","deployment","runtime","data_store","authority","projection"} <= kinds)
        self.assertIn("surface_role", schema["properties"])

    def test_56_observation_can_carry_explicit_claim_truth_state(self):
        schema = load("observation.schema.json")
        statuses = set(schema["properties"]["claim_status"]["enum"])
        self.assertEqual(statuses, {"observed","realised","verified","blocked","unknown"})

    def test_57_usage_perception_has_no_canonical_aggregate_score(self):
        schema = load("usage-evaluation.schema.json")
        perception = schema["properties"]["perception"]["properties"]
        self.assertNotIn("score", perception)
        self.assertTrue({"understanding","utility","trust","autonomy","risk_perception","intention_to_use"} <= set(perception))

    def test_58_digital_metabolism_keeps_value_unknown_nullable(self):
        schema = load("digital-metabolism.schema.json")
        value = schema["properties"]["value"]["properties"]
        for key in ["resource_utilisation_gap","avoided_spend_eur","reuse_ratio"]:
            self.assertIn("null", value[key]["type"])

    def test_59_admission_and_execution_are_separate_contracts(self):
        admission = load("admission-profile.schema.json")
        execution = load("execution-plan.schema.json")
        self.assertIn("risk_class", admission["properties"])
        self.assertNotIn("risk_class", execution["properties"])
        self.assertIn("estate_id", execution["properties"])
        self.assertNotIn("estate_id", admission["properties"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
