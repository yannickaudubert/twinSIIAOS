#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASES = json.loads((ROOT / "conformance" / "cases.json").read_text(encoding="utf-8"))
LIFECYCLE_CASES = json.loads((ROOT / "conformance" / "lifecycle-cases.json").read_text(encoding="utf-8"))

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
    for case in LIFECYCLE_CASES:
        envelope = {
            "protocol_version": "0.1",
            "operation": "transition",
            "record": case["record"],
            "target_state": case["target_state"],
            "transition": case.get("transition", {})
        }
        py = run([sys.executable, str(ROOT / "engine.py")], envelope)
        js = run(["node", str(ROOT / "engine.js")], envelope)
        py_result = py["result"]
        js_result = js["result"]
        if py_result["ok"] != case["expected_ok"] or js_result["ok"] != case["expected_ok"]:
            failures.append({"case": case["name"], "expected_ok": case["expected_ok"], "python": py_result, "javascript": js_result})
            continue
        expected_reasons = sorted(case.get("expected_reasons", []))
        if expected_reasons:
            if sorted(py_result.get("reasons", [])) != expected_reasons or sorted(js_result.get("reasons", [])) != expected_reasons:
                failures.append({"case": case["name"], "expected_reasons": expected_reasons, "python": py_result.get("reasons", []), "javascript": js_result.get("reasons", [])})
        if py_result["ok"] and js_result["ok"]:
            if py_result["record"]["admission_state"] != case["target_state"] or js_result["record"]["admission_state"] != case["target_state"]:
                failures.append({"case": case["name"], "expected_state": case["target_state"], "python": py_result["record"]["admission_state"], "javascript": js_result["record"]["admission_state"]})
    if failures:
        print(json.dumps({"ok": False, "failures": failures}, indent=2))
        return 1
    print(json.dumps({"ok": True, "assessment_cases": len(CASES), "lifecycle_cases": len(LIFECYCLE_CASES), "runtimes": ["python", "javascript"]}))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
