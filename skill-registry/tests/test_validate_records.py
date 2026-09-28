import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
SCRIPT=ROOT/"skill-registry"/"validate_records.py"
DIMS=["governance","delivery","operations","observability","security","data","ai_usage","automation","open_source","human_control"]

def rec():
    return {
      "record_id":"skill.x","object_type":"skill","name":"x",
      "capabilities":[{"capability_id":"skill.test","relation":"EXPERIMENT"}],
      "admission_state":"DISCOVERED","risk_class":"R1",
      "maturity_min":{k:0 for k in DIMS},
      "provenance":{"source":"skills://x"}
    }

class RecordValidatorTests(unittest.TestCase):
    def run_payload(self,payload):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"r.json"
            p.write_text(json.dumps(payload),encoding="utf-8")
            return subprocess.run([sys.executable,str(SCRIPT),str(p)],capture_output=True,text=True)

    def test_valid_record_passes(self):
        p=self.run_payload({"records":[rec()]})
        self.assertEqual(p.returncode,0,p.stdout+p.stderr)

    def test_duplicate_ids_fail(self):
        r=rec()
        p=self.run_payload({"records":[r,r]})
        self.assertNotEqual(p.returncode,0)

    def test_bad_maturity_fails(self):
        r=rec(); r["maturity_min"].pop("security")
        p=self.run_payload({"records":[r]})
        self.assertNotEqual(p.returncode,0)

if __name__=="__main__":
    unittest.main()
