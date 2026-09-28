#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def validate_trigger_spec(payload):
    errors=[]
    ids=set()
    for case in payload.get("cases",[]):
        cid=case.get("id")
        if not cid or cid in ids:
            errors.append("duplicate_or_missing_case_id")
        ids.add(cid)
        if not case.get("utterance"):
            errors.append(f"{cid}:missing_utterance")
        if not case.get("expected_primary"):
            errors.append(f"{cid}:missing_expected_primary")
        if case.get("expected_primary") in set(case.get("forbidden_primary",[])):
            errors.append(f"{cid}:expected_is_forbidden")
    return errors

def validate_regression(payload):
    errors=[]
    ids=set()
    for inv in payload.get("invariants",[]):
        iid=inv.get("id")
        if not iid or iid in ids:
            errors.append("duplicate_or_missing_invariant_id")
        ids.add(iid)
        if not inv.get("statement"):
            errors.append(f"{iid}:missing_statement")
        if not inv.get("applies_to"):
            errors.append(f"{iid}:missing_scope")
    return errors

def evaluate_router_output(spec, results):
    by_id={x.get("id"):x for x in results.get("results",[])}
    failures=[]
    for case in spec.get("cases",[]):
        got=by_id.get(case["id"])
        if not got:
            failures.append({"id":case["id"],"reason":"missing_result"})
            continue
        primary=got.get("primary")
        if primary!=case["expected_primary"]:
            failures.append({"id":case["id"],"reason":"wrong_primary","expected":case["expected_primary"],"actual":primary})
        if primary in case.get("forbidden_primary",[]):
            failures.append({"id":case["id"],"reason":"forbidden_primary","actual":primary})
    return failures

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--triggers",default="skill-registry/tests/trigger-cases.json")
    ap.add_argument("--regression",default="skill-registry/tests/non-regression.json")
    ap.add_argument("--router-results")
    args=ap.parse_args()
    trigger=load(args.triggers)
    regression=load(args.regression)
    errors=validate_trigger_spec(trigger)+validate_regression(regression)
    if args.router_results:
        errors+=evaluate_router_output(trigger,load(args.router_results))
    print(json.dumps({"ok":not errors,"errors":errors,"trigger_cases":len(trigger.get("cases",[])),"invariants":len(regression.get("invariants",[]))},indent=2))
    raise SystemExit(1 if errors else 0)

if __name__=="__main__":
    main()
