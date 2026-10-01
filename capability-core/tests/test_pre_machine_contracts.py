import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]


class PreMachineContractsTest(unittest.TestCase):
    def test_golden_mission_gates_cover_required_failures(self):
        data = json.loads((ROOT / "golden-mission-gates.json").read_text(encoding="utf-8"))
        ids = {item["id"] for item in data["gates"]}
        self.assertEqual(ids, {f"G{i}" for i in range(11)})

    def test_pre_machine_gates_do_not_require_runtime(self):
        data = json.loads((ROOT / "golden-mission-gates.json").read_text(encoding="utf-8"))
        pre_machine = {item["id"] for item in data["gates"] if not item["requires_runtime"]}
        self.assertTrue({"G2", "G3", "G4", "G5", "G6", "G7", "G8", "G9", "G10"}.issubset(pre_machine))

    def test_strategy_schema_contains_constraint_and_adversarial_modes(self):
        data = json.loads((ROOT / "cognitive-strategy.schema.json").read_text(encoding="utf-8"))
        values = set(data["properties"]["id"]["enum"])
        self.assertIn("constraint_deconstruction", values)
        self.assertIn("adversarial_verify", values)
        self.assertIn("simulate", values)


if __name__ == "__main__":
    unittest.main()
