import json, os, sys, unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import engine

CASES=json.load(open(os.path.join(os.path.dirname(__file__),'..','conformance','cases.json'),encoding='utf-8'))
GATES=json.load(open(os.path.join(os.path.dirname(__file__),'..','golden-mission-gates.json'),encoding='utf-8'))
STRATEGY_SCHEMA=json.load(open(os.path.join(os.path.dirname(__file__),'..','cognitive-strategy.schema.json'),encoding='utf-8'))

class CapabilityCoreTests(unittest.TestCase):
    def test_conformance_cases(self):
        for case in CASES:
            with self.subTest(case=case["name"]):
                self.assertEqual(
                    engine.assess(case["record"], case.get("context"))["verdict"],
                    case["expected"]
                )

    def test_pre_machine_contracts(self):
        ids={item["id"] for item in GATES["gates"]}
        self.assertEqual(ids,{f"G{i}" for i in range(11)})
        pre_machine={item["id"] for item in GATES["gates"] if not item["requires_runtime"]}
        self.assertTrue({"G2","G3","G4","G5","G6","G7","G8","G9","G10"}.issubset(pre_machine))
        strategies=set(STRATEGY_SCHEMA["properties"]["id"]["enum"])
        self.assertIn("constraint_deconstruction",strategies)
        self.assertIn("adversarial_verify",strategies)
        self.assertIn("simulate",strategies)

    def test_duplicate_detection(self):
        candidate={
            "record_id":"new",
            "name":"New",
            "admission_state":"CANDIDATE",
            "risk_class":"R1",
            "maturity_min":{},
            "capabilities":[{"capability_id":"same","relation":"NEW"}],
            "local_feasibility":{}
        }
        admitted={
            "record_id":"existing",
            "name":"Existing",
            "admission_state":"ADMITTED",
            "risk_class":"R0",
            "maturity_min":{},
            "capabilities":[{"capability_id":"same","relation":"NEW"}],
            "local_feasibility":{}
        }
        self.assertEqual(
            engine.assess(candidate,{"admittedRecords":[admitted]})["verdict"],
            "DUPLICATE"
        )

if __name__=="__main__":
    unittest.main()
