import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
SCRIPT=ROOT/"skill-registry"/"inventory_to_records.py"

class ConverterTests(unittest.TestCase):
    def run_converter(self,payload,kind):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"input.json"
            p.write_text(json.dumps(payload),encoding="utf-8")
            proc=subprocess.run([sys.executable,str(SCRIPT),str(p),"--kind",kind],capture_output=True,text=True,check=True)
            return json.loads(proc.stdout)

    def test_chatgpt_presence_stays_discovered(self):
        payload={"observed_at":"2026-09-27","observed_environment":"ChatGPT","items":[{"uri":"skills://alpha","family":"context-governance"}]}
        out=self.run_converter(payload,"chatgpt")
        record=out["records"][0]
        self.assertEqual(record["admission_state"],"DISCOVERED")
        self.assertEqual(record["evidence"][0]["status"],"observed")
        self.assertEqual(record["evidence"][0]["environment"],"ChatGPT")
        self.assertIsNone(record["provenance"]["license"])

    def test_local_hash_does_not_imply_admission(self):
        payload={"environment":"SandY-test","roots":[{"skills":[{"name":"alpha","description":"A","entrypoint":"alpha/SKILL.md","skill_dir":"alpha","entrypoint_sha256":"abc","file_count":1,"files":[{"path":"SKILL.md","bytes":1,"sha256":"abc"}]}]}]}
        out=self.run_converter(payload,"local")
        record=out["records"][0]
        self.assertEqual(record["provenance"]["artifact_hash"],"sha256:abc")
        self.assertEqual(record["admission_state"],"DISCOVERED")
        self.assertEqual(record["registry_meta"]["inventory_environment"],"SandY-test")

    def test_candidate_has_no_fake_commit_or_license(self):
        payload={"items":[{"id":"x.y","source_repo":"https://github.com/x/y","family":"git-code","capability":"debug","relation":"NEW"}]}
        record=self.run_converter(payload,"candidates")["records"][0]
        self.assertIsNone(record["provenance"]["source_commit"])
        self.assertIsNone(record["provenance"]["license"])
        self.assertEqual(record["admission_state"],"DISCOVERED")

if __name__=="__main__":
    unittest.main()
