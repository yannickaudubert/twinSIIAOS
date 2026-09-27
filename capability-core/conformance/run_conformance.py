#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASES = json.loads((ROOT / "conformance" / "cases.json").read_text(encoding="utf-8"))

def run(cmd, payload):
    proc = subprocess.run(
        cmd,
        input=json.dumps(payload),
        text=True,
        capture_output=True,
        cwd=ROOT.parent,
        check=False
    )
    if proc.returncode != 0:
        raise RuntimeError(f"{cmd} failed: {proc.stderr}")
    return json.loads(proc.stdout)

def main():
    failures = []
    for case in CASES:
        envelope = {
            "protocol_version": "0.1",
            "operation": "assess",
            "record": case["record"],
            "context": case.get("context", {})
        }
        py = run([sys.executable, str(ROOT / "engine.py")], envelope)
        js = run(["node", str(ROOT / "engine.js")], envelope)
        py_verdict = py["result"]["verdict"]
        js_verdict = js["result"]["verdict"]
        expected = case["expected"]
        if py_verdict != expected or js_verdict != expected or py_verdict != js_verdict:
            failures.append({
                "case": case["name"],
                "expected": expected,
                "python": py_verdict,
                "javascript": js_verdict
            })
    if failures:
        print(json.dumps({"ok": False, "failures": failures}, indent=2))
        return 1
    print(json.dumps({"ok": True, "cases": len(CASES), "runtimes": ["python", "javascript"]}))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
