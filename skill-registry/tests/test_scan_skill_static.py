import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
SCRIPT=ROOT/"skill-registry"/"scan_skill_static.py"

class StaticScanTests(unittest.TestCase):
    def run_scan(self,files):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            for name,content in files.items():
                p=root/name
                p.parent.mkdir(parents=True,exist_ok=True)
                p.write_text(content,encoding="utf-8")
            proc=subprocess.run([sys.executable,str(SCRIPT),str(root)],capture_output=True,text=True,check=True)
            return json.loads(proc.stdout)

    def test_clean_skill_is_low(self):
        r=self.run_scan({"SKILL.md":"---\nname: a\ndescription: b\n---\nDo analysis only."})
        self.assertEqual(r["heuristic_risk"],"LOW")

    def test_shell_and_delete_raise_risk(self):
        r=self.run_scan({"scripts/x.py":"import os\nos.system('echo x')\nos.remove('x')\n"})
        kinds={x["kind"] for x in r["findings"]}
        self.assertIn("shell_execution",kinds)
        self.assertIn("filesystem_delete",kinds)
        self.assertIn(r["heuristic_risk"],{"MEDIUM","HIGH"})

if __name__=="__main__":
    unittest.main()
