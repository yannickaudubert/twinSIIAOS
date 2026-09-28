#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

DIMS={"governance","delivery","operations","observability","security","data","ai_usage","automation","open_source","human_control"}
STATES={"DISCOVERED","CANDIDATE","SCANNED","REVIEWED","EXPERIMENT","ADMITTED","PINNED","OBSERVED","BLOCKED","HOLD","REJECTED","RETIRED","UNKNOWN"}
RISKS={"R0","R1","R2","R3","R4"}
RELATIONS={"NEW","REPLACE","AUGMENT","DUPLICATE","EXPERIMENT"}

def validate_record(r):
    errors=[]
    for key in ("record_id","object_type","name","capabilities","admission_state","risk_class","maturity_min","provenance"):
        if key not in r:
            errors.append("missing:"+key)
    if r.get("object_type")!="skill":
        errors.append("object_type:not_skill")
    if r.get("admission_state") not in STATES:
        errors.append("bad_state")
    if r.get("risk_class") not in RISKS:
        errors.append("bad_risk")
    maturity=r.get("maturity_min") or {}
    if set(maturity)!=DIMS:
        errors.append("maturity_dimensions_mismatch")
    else:
        for k,v in maturity.items():
            if not isinstance(v,int) or not 0<=v<=4:
                errors.append("bad_maturity:"+k)
    caps=r.get("capabilities") or []
    if not caps:
        errors.append("no_capabilities")
    for i,c in enumerate(caps):
        if not c.get("capability_id"):
            errors.append(f"capability[{i}]:missing_id")
        if c.get("relation") not in RELATIONS:
            errors.append(f"capability[{i}]:bad_relation")
    prov=r.get("provenance") or {}
    if not prov.get("source"):
        errors.append("provenance:missing_source")
    if r.get("admission_state")=="DISCOVERED":
        # Discovery must not silently pretend evidence of admission/pinning.
        if prov.get("verified_at") and not r.get("evidence"):
            errors.append("discovered_verified_without_evidence")
    return errors

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("files",nargs="+")
    args=ap.parse_args()
    failures=[]
    total=0
    ids=set()
    for fn in args.files:
        payload=json.loads(Path(fn).read_text(encoding="utf-8"))
        for r in payload.get("records",[]):
            total+=1
            rid=r.get("record_id")
            if rid in ids:
                failures.append({"file":fn,"record_id":rid,"errors":["duplicate_record_id"]})
                continue
            ids.add(rid)
            errs=validate_record(r)
            if errs:
                failures.append({"file":fn,"record_id":rid,"errors":errs})
    print(json.dumps({"ok":not failures,"records":total,"failures":failures},indent=2))
    raise SystemExit(1 if failures else 0)

if __name__=="__main__":
    main()
