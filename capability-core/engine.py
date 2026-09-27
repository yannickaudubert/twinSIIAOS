#!/usr/bin/env python3
import json
import sys

DIMS = ["governance","delivery","operations","observability","security","data","ai_usage","automation","open_source","human_control"]
RISK = {"R0":0,"R1":1,"R2":2,"R3":3,"R4":4}
TERMINAL = {"BLOCKED","REJECTED","RETIRED","HOLD"}

def profile(p=None):
    p = p or {}
    out = {}
    for k in DIMS:
        try:
            v = int(p.get(k,0))
        except Exception:
            v = 0
        out[k] = max(0,min(4,v))
    return out

def maturity_fit(rec, p=None):
    a, req = profile(p), profile(rec.get("maturity_min"))
    gaps = [{"dimension":k,"actual":a[k],"required":req[k],"gap":req[k]-a[k]} for k in DIMS if a[k] < req[k]]
    return {"meets":not gaps,"actual":a,"required":req,"gaps":gaps,"total_gap":sum(x["gap"] for x in gaps)}

def risk_gate(rec, policy=None):
    policy = policy or {}
    risk = RISK.get(rec.get("risk_class"),4)
    max_wo = RISK.get(policy.get("maxRiskWithoutHuman","R2"),2)
    max_allowed = RISK.get(policy.get("maxAllowedRisk","R4"),4)
    if risk > max_allowed:
        return {"allowed":False,"human_gate":True,"reason":"RISK_EXCEEDS_POLICY"}
    if risk >= 3 or risk > max_wo:
        return {"allowed":True,"human_gate":True,"reason":"HUMAN_GATE_REQUIRED"}
    return {"allowed":True,"human_gate":False,"reason":"RISK_WITHIN_POLICY"}

def cap_ids(rec):
    return {x.get("capability_id") for x in rec.get("capabilities",[]) if x.get("capability_id")}

def overlap(candidate, admitted):
    ids = cap_ids(candidate)
    out = []
    for e in admitted or []:
        if e.get("admission_state") not in {"ADMITTED","PINNED","OBSERVED"}:
            continue
        for cid in cap_ids(e):
            if cid in ids:
                out.append({"capability_id":cid,"record_id":e.get("record_id"),"name":e.get("name")})
    return out

def local_fit(rec, prefs=None):
    prefs = prefs or {}
    local = rec.get("local_feasibility") or {}
    reasons = []
    if prefs.get("requireOffline") is True and local.get("offline_capable") is not True:
        reasons.append("OFFLINE_NOT_PROVEN")
    if prefs.get("avoidExternalApi") is True and local.get("external_api_dependency") is True:
        reasons.append("EXTERNAL_API_DEPENDENCY")
    m = prefs.get("maxSubscriptionCost")
    c = local.get("subscription_cost")
    if isinstance(m,(int,float)) and isinstance(c,(int,float)) and c > m:
        reasons.append("SUBSCRIPTION_COST_EXCEEDS_POLICY")
    return {"meets":not reasons,"reasons":reasons}

def assess(rec, ctx=None):
    ctx = ctx or {}
    state = rec.get("admission_state")
    if state in TERMINAL:
        return {"record":rec,"verdict":state,"eligible":False,"reasons":["STATE_"+state],"maturity":None,"risk":None,"overlap":[],"local":None}
    mat = maturity_fit(rec, ctx.get("profile"))
    if not mat["meets"]:
        reasons = [f"MATURITY_{g['dimension'].upper()}_{g['actual']}_LT_{g['required']}" for g in mat["gaps"]]
        return {"record":rec,"verdict":"MATURITY_GAP","eligible":False,"reasons":reasons,"maturity":mat,"risk":None,"overlap":[],"local":None}
    rg = risk_gate(rec, ctx.get("policy"))
    if not rg["allowed"]:
        return {"record":rec,"verdict":"BLOCKED","eligible":False,"reasons":[rg["reason"]],"maturity":mat,"risk":rg,"overlap":[],"local":None}
    ov = overlap(rec, ctx.get("admittedRecords",[]))
    rel = {x.get("relation") for x in rec.get("capabilities",[])}
    if ov and not (rel & {"AUGMENT","REPLACE","DUPLICATE"}):
        return {"record":rec,"verdict":"DUPLICATE","eligible":False,"reasons":["CAPABILITY_ALREADY_ADMITTED"],"maturity":mat,"risk":rg,"overlap":ov,"local":None}
    lf = local_fit(rec, ctx.get("preferences"))
    if not lf["meets"]:
        return {"record":rec,"verdict":"LOCAL_POLICY_GAP","eligible":False,"reasons":lf["reasons"],"maturity":mat,"risk":rg,"overlap":ov,"local":lf}
    if rg["human_gate"]:
        return {"record":rec,"verdict":"HUMAN_GATE","eligible":True,"reasons":[rg["reason"]],"maturity":mat,"risk":rg,"overlap":ov,"local":lf}
    return {"record":rec,"verdict":"ELIGIBLE","eligible":True,"reasons":["FIT"],"maturity":mat,"risk":rg,"overlap":ov,"local":lf}

def score(a):
    if not a["eligible"]:
        return -1000 - ((a.get("maturity") or {}).get("total_gap") or 0)
    s = 100 - RISK.get(a["record"].get("risk_class"),4)*10
    if a["verdict"] == "HUMAN_GATE":
        s -= 15
    local = a["record"].get("local_feasibility") or {}
    if local.get("offline_capable") is True:
        s += 10
    if local.get("external_api_dependency") is False:
        s += 8
    if local.get("subscription_cost") == 0:
        s += 4
    return s

def route(records, ctx=None):
    out = []
    for r in records or []:
        a = assess(r,ctx)
        a["score"] = score(a)
        out.append(a)
    out.sort(key=lambda x:(-x["score"], str(x["record"].get("name",""))))
    return out


ALLOWED_TRANSITIONS = {
    "DISCOVERED": {"CANDIDATE", "REJECTED"},
    "CANDIDATE": {"SCANNED", "BLOCKED", "REJECTED"},
    "SCANNED": {"REVIEWED", "BLOCKED", "REJECTED"},
    "REVIEWED": {"EXPERIMENT", "BLOCKED", "REJECTED"},
    "EXPERIMENT": {"ADMITTED", "BLOCKED", "REJECTED"},
    "ADMITTED": {"PINNED", "HOLD", "RETIRED"},
    "PINNED": {"OBSERVED", "HOLD", "RETIRED"},
    "OBSERVED": {"HOLD", "RETIRED"},
    "HOLD": {"EXPERIMENT", "RETIRED"},
    "UNKNOWN": {"CANDIDATE", "REJECTED"},
}

def _evidence_kinds(evidence):
    return {str(e.get("kind","")).lower() for e in evidence or []}

def _verified_evidence(evidence, kinds=None):
    for item in evidence or []:
        if item.get("status") != "verified":
            continue
        if kinds is None or str(item.get("kind","")).lower() in kinds:
            return True
    return False

def transition(rec, target_state, request=None):
    request = request or {}
    current = rec.get("admission_state", "UNKNOWN")
    target = str(target_state or "").upper()
    allowed = ALLOWED_TRANSITIONS.get(current, set())
    reasons = []

    if target not in allowed:
        reasons.append("TRANSITION_NOT_ALLOWED")

    supplied_evidence = request.get("evidence") or []
    combined_evidence = list(rec.get("evidence") or []) + list(supplied_evidence)
    kinds = _evidence_kinds(combined_evidence)
    risk = RISK.get(rec.get("risk_class"), 4)

    if target == "SCANNED":
        for required in ("provenance", "license", "security"):
            if required not in kinds:
                reasons.append("MISSING_" + required.upper() + "_EVIDENCE")

    if target == "EXPERIMENT":
        experiment = request.get("experiment") or rec.get("experiment") or {}
        if not experiment.get("hypothesis"):
            reasons.append("MISSING_EXPERIMENT_HYPOTHESIS")
        if not experiment.get("success_metrics"):
            reasons.append("MISSING_EXPERIMENT_SUCCESS_METRICS")
        if not experiment.get("rollback"):
            reasons.append("MISSING_EXPERIMENT_ROLLBACK")
        if risk >= RISK["R3"] and request.get("human_approved") is not True:
            reasons.append("HUMAN_APPROVAL_REQUIRED")

    if target == "ADMITTED":
        accepted = _verified_evidence(combined_evidence, {"experiment_result", "admission_exception"})
        if not accepted:
            reasons.append("VERIFIED_EXPERIMENT_OR_EXCEPTION_REQUIRED")
        if risk >= RISK["R3"] and request.get("human_approved") is not True:
            reasons.append("HUMAN_APPROVAL_REQUIRED")

    if target == "PINNED":
        provenance = dict(rec.get("provenance") or {})
        provenance.update(request.get("provenance") or {})
        if not provenance.get("artifact_hash"):
            reasons.append("ARTIFACT_HASH_REQUIRED")
        if not (provenance.get("source_commit") or provenance.get("version")):
            reasons.append("IMMUTABLE_VERSION_REQUIRED")

    if target == "OBSERVED":
        observed = any(
            e.get("status") in {"observed", "verified"} and e.get("environment")
            for e in combined_evidence
        )
        if not observed:
            reasons.append("RUNTIME_EVIDENCE_REQUIRED")

    if target in {"HOLD", "RETIRED", "REJECTED", "BLOCKED"} and not request.get("reason"):
        reasons.append("REASON_REQUIRED")

    if reasons:
        return {
            "ok": False,
            "from_state": current,
            "target_state": target,
            "reasons": reasons,
            "record": rec,
        }

    updated = dict(rec)
    updated["admission_state"] = target
    updated["evidence"] = combined_evidence

    if request.get("experiment") is not None:
        updated["experiment"] = request.get("experiment")

    if request.get("provenance") is not None:
        provenance = dict(updated.get("provenance") or {})
        provenance.update(request.get("provenance") or {})
        updated["provenance"] = provenance

    history = list(updated.get("lifecycle_history") or [])
    history.append({
        "from": current,
        "to": target,
        "timestamp": request.get("timestamp"),
        "reason": request.get("reason"),
        "human_approved": request.get("human_approved") is True,
        "evidence_ids": [e.get("evidence_id") for e in supplied_evidence if e.get("evidence_id")],
    })
    updated["lifecycle_history"] = history

    return {
        "ok": True,
        "from_state": current,
        "target_state": target,
        "reasons": [],
        "record": updated,
    }

def execute(env):
    op = env.get("operation")
    if op == "assess":
        return {"protocol_version":"0.1","result":assess(env["record"],env.get("context"))}
    if op == "route":
        return {"protocol_version":"0.1","result":route(env.get("records",[]),env.get("context"))}
    if op == "transition":
        return {"protocol_version":"0.1","result":transition(env["record"], env["target_state"], env.get("transition"))}
    raise ValueError("Unsupported operation")

def main():
    data = json.load(sys.stdin)
    json.dump(execute(data),sys.stdout,ensure_ascii=False,separators=(",",":"))
    sys.stdout.write("\n")

if __name__ == "__main__":
    main()
