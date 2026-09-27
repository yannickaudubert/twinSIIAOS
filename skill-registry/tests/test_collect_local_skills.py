import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT=Path(__file__).resolve().parents[1]/"collect_local_skills.py"

class CollectorTests(unittest.TestCase):
    def test_collects_skill_without_executing_it(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            skill=root/"alpha"
            skill.mkdir()
            (skill/"SKILL.md").write_text("---\nname: alpha\ndescription: Test skill\n---\n# Alpha\n",encoding="utf-8")
            scripts=skill/"scripts"
            scripts.mkdir()
            marker=root/"EXECUTED"
            (scripts/"danger.py").write_text(f"from pathlib import Path\nPath({str(marker)!r}).write_text('bad')\n",encoding="utf-8")
            proc=subprocess.run([sys.executable,str(SCRIPT),str(root),"--environment","test"],capture_output=True,text=True,check=True)
            payload=json.loads(proc.stdout)
            self.assertEqual(payload["environment"],"test")
            self.assertEqual(payload["roots"][0]["skill_count"],1)
            found=payload["roots"][0]["skills"][0]
            self.assertEqual(found["name"],"alpha")
            self.assertEqual(found["description"],"Test skill")
            self.assertFalse(marker.exists())
            self.assertEqual(found["file_count"],2)
            self.assertTrue(found["entrypoint_sha256"])

if __name__=="__main__":
    unittest.main()
