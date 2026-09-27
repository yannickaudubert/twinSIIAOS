import json
import os
import subprocess
import sys
import time
import unittest
import urllib.request
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

class SidecarTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        env=os.environ.copy()
        env["SIIAOS_CORE_PORT"]="18765"
        env["SIIAOS_CORE_TOKEN"]="test-token"
        cls.proc=subprocess.Popen(
            [sys.executable, str(ROOT/"sidecar.py")],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=env
        )
        deadline=time.time()+5
        while time.time()<deadline:
            try:
                with urllib.request.urlopen("http://127.0.0.1:18765/health", timeout=.25) as r:
                    if r.status==200:
                        return
            except Exception:
                time.sleep(.1)
        raise RuntimeError("sidecar did not start")

    @classmethod
    def tearDownClass(cls):
        cls.proc.terminate()
        try:
            cls.proc.wait(timeout=2)
        except subprocess.TimeoutExpired:
            cls.proc.kill()

    def test_health(self):
        with urllib.request.urlopen("http://127.0.0.1:18765/health") as r:
            payload=json.load(r)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["protocol_version"],"0.1")

    def test_assess(self):
        envelope={
            "protocol_version":"0.1",
            "operation":"assess",
            "record":{
                "record_id":"test",
                "name":"Test",
                "admission_state":"CANDIDATE",
                "risk_class":"R1",
                "maturity_min":{},
                "capabilities":[{"capability_id":"test.cap","relation":"NEW"}],
                "local_feasibility":{"offline_capable":True,"external_api_dependency":False}
            },
            "context":{}
        }
        req=urllib.request.Request(
            "http://127.0.0.1:18765/v0.1/execute",
            data=json.dumps(envelope).encode(),
            headers={
                "Content-Type":"application/json",
                "Authorization":"Bearer test-token"
            },
            method="POST"
        )
        with urllib.request.urlopen(req) as r:
            payload=json.load(r)
        self.assertEqual(payload["result"]["verdict"],"ELIGIBLE")

if __name__=="__main__":
    unittest.main()
