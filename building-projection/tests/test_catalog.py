import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILDINGS = ROOT / "buildings"

class BuildingProjectionTests(unittest.TestCase):
    def load(self, path):
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)

    def test_catalog_files_exist(self):
        catalog = self.load(ROOT / "catalog.json")
        for rel in catalog["buildings"]:
            self.assertTrue((ROOT / rel).exists(), rel)

    def test_unique_building_floor_and_cell_ids(self):
        seen_buildings = set()
        seen_nodes = set()
        for path in BUILDINGS.glob("*.json"):
            doc = self.load(path)
            self.assertEqual(doc["schema_version"], "1.0")
            self.assertNotIn(doc["building_id"], seen_buildings)
            seen_buildings.add(doc["building_id"])
            for floor in doc["floors"]:
                self.assertNotIn(floor["floor_id"], seen_nodes)
                seen_nodes.add(floor["floor_id"])
                self.assertTrue(floor["service_cells"])
                for cell in floor["service_cells"]:
                    self.assertNotIn(cell["cell_id"], seen_nodes)
                    seen_nodes.add(cell["cell_id"])
                    self.assertTrue(cell["capability_refs"])

    def test_truth_separation(self):
        for path in BUILDINGS.glob("*.json"):
            doc = self.load(path)
            self.assertIn(doc["implementation_status"], {"DESIGNED", "CODED", "TESTED", "DEPLOYED", "OBSERVED"})
            self.assertIn("desired_state", doc)
            self.assertIn("observed_state", doc)
            self.assertEqual(doc["observed_state"], "UNKNOWN")

if __name__ == "__main__":
    unittest.main()
