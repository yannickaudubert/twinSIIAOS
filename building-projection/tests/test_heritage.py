import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILDINGS = ROOT / "buildings"

class HeritageTests(unittest.TestCase):
    def load(self, path):
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)

    def test_city_fabric_building_ids_present(self):
        baseline = self.load(ROOT / "city-fabric-baseline.json")
        catalog = self.load(ROOT / "catalog.json")
        docs = {}
        for rel in catalog["buildings"]:
            p = ROOT / rel
            doc = self.load(p)
            docs[doc["building_id"]] = doc
        for building_id in baseline["buildings"]:
            self.assertIn(building_id, docs)

    def test_six_complementary_views_preserved(self):
        views = self.load(ROOT / "views.json")["views"]
        self.assertEqual(
            [v["name"] for v in views],
            ["Immeuble", "Carte SI", "Missions", "Agents", "Stack", "Preuves"],
        )

    def test_historical_lineage_does_not_claim_runtime(self):
        heritage = self.load(ROOT / "heritage-map.json")
        current = next(x for x in heritage["lineage"] if x["id"] == "BUILDING-PROJECTION-V1")
        self.assertEqual(current["observed_runtime"], "UNKNOWN")
        for item in heritage["lineage"]:
            self.assertNotEqual(item.get("evidence_state"), "OBSERVED_ON_SANDY")

if __name__ == "__main__":
    unittest.main()
