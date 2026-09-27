import json, os, sys, unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import engine

CASES=json.load(open(os.path.join(os.path.dirname(__file__),'..','conformance','cases.json'),encoding='utf-8'))

class CapabilityCoreTests(unittest.TestCase):
    def test_conformance_cases(self):
        for case in CASES:
            with self.subTest(case=case["name"]):
                self.assertEqual(
                    engine.assess(case["record"], case.get("context"))["verdict"],
                    case["expected"]
                )

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
