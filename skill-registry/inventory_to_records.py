#!/usr/bin/env python3
import argparse
import hashlib
import json
from pathlib import Path
from urllib.parse import urlparse

DIMS=["governance","delivery","operations","observability","security","data","ai_usage","automation","open_source","human_control"]

def zero_maturity():
    return {k:0 for k in DIMS}

def stable_id(value):
    out=[]
    for ch in value.lower():
        out.append(ch if ch.isalnum() else ".")
    return ".".join(filter(None,"".join(out).split(".")))

def capability_from_family(family):
    return "skill."+stable_id(family or "unclassified")

def chatgpt_item_to_record(item, environment, observed_at):
    uri=item["uri"]
    name=uri.rstrip("/").split("/")[-1]
    return {
        "record_id":"skill."+stable_id(uri.replace("skills://","")),
        "object_type":"skill",
        "name":name,
        "description":None,
        "capabilities":[{
            "capability_id":capability_from_family(item.get("family")),
            "relation":"EXPERIMENT"
        }],
        "admission_state":"DISCOVERED",
        "risk_class":"R1",
        "maturity_min":zero_maturity(),
        "permissions":{
            "filesystem_scopes":[],
            "process_execution":None,
            "shell_access":None,
            "gpu_access":None,
            "privilege_level":None
        },
        "network":{
            "outbound_required":None,
            "allowed_destinations":[],
            "inbound_listeners":[],
            "localhost_only":None
        },
        "data_scope":{
            "personal_data":None,
            "confidential_data":None,
            "customer_data":None,
            "secrets_credentials":None,
            "persistence_location":None,
            "retention":None
        },
        "local_feasibility":{
            "cpu":None,"ram":None,"gpu":None,"vram":None,"disk":None,
            "persistent_service":None,"external_api_dependency":None,
            "subscription_cost":None,"offline_capable":None,"degraded_mode":None
        },
        "provenance":{
            "source":uri,
            "source_repo":None,
            "source_commit":None,
            "version":None,
            "artifact_hash":None,
            "license":None,
            "verified_at":None
        },
        "evidence":[{
            "evidence_id":"observed-"+stable_id(environment)+"-"+stable_id(name),
            "kind":"environment_inventory",
            "source":uri,
            "timestamp":observed_at+"T00:00:00Z",
            "subject":name,
            "claim":"Skill is observable in the named environment inventory only.",
            "status":"observed",
            "artifact_hash":None,
            "environment":environment,
            "notes":"Presence does not prove installation or execution in any other environment."
        }],
        "skill":{
            "skill_name":name,
            "trigger_description":None,
            "source_type":"local",
            "connectors":[],
            "tools":[],
            "scripts":[],
            "conflicts_with":[],
            "depends_on":[],
            "tests":[],
            "trigger_tests":[],
            "non_regression_tests":[],
            "last_verified_at":None
        },
        "registry_meta":{
            "family":item.get("family"),
            "inventory_environment":environment,
            "inventory_observed_at":observed_at
        }
    }

def local_skill_to_record(skill, environment):
    name=skill["name"]
    digest=skill.get("entrypoint_sha256")
    source="file://"+skill.get("skill_dir","")
    return {
        "record_id":"skill."+stable_id(environment)+"."+stable_id(name),
        "object_type":"skill",
        "name":name,
        "description":skill.get("description"),
        "capabilities":[{"capability_id":"skill.unclassified","relation":"EXPERIMENT"}],
        "admission_state":"DISCOVERED",
        "risk_class":"R1",
        "maturity_min":zero_maturity(),
        "permissions":{"filesystem_scopes":[],"process_execution":None,"shell_access":None,"gpu_access":None,"privilege_level":None},
        "network":{"outbound_required":None,"allowed_destinations":[],"inbound_listeners":[],"localhost_only":None},
        "data_scope":{"personal_data":None,"confidential_data":None,"customer_data":None,"secrets_credentials":None,"persistence_location":None,"retention":None},
        "local_feasibility":{"cpu":None,"ram":None,"gpu":None,"vram":None,"disk":None,"persistent_service":None,"external_api_dependency":None,"subscription_cost":0,"offline_capable":None,"degraded_mode":None},
        "provenance":{
            "source":source,
            "source_repo":None,
            "source_commit":None,
            "version":None,
            "artifact_hash":"sha256:"+digest if digest else None,
            "license":None,
            "verified_at":None
        },
        "evidence":[],
        "skill":{
            "skill_name":name,
            "trigger_description":skill.get("description"),
            "source_type":"local",
            "connectors":[],
            "tools":[],
            "scripts":[f["path"] for f in skill.get("files",[]) if f["path"].startswith("scripts/")],
            "conflicts_with":[],
            "depends_on":[],
            "tests":[],
            "trigger_tests":[],
            "non_regression_tests":[],
            "last_verified_at":None
        },
        "registry_meta":{"inventory_environment":environment,"entrypoint":skill.get("entrypoint"),"file_count":skill.get("file_count")}
    }

def candidate_to_record(item):
    source=item["source_repo"]
    parsed=urlparse(source)
    return {
        "record_id":"skill.candidate."+stable_id(item["id"]),
        "object_type":"skill",
        "name":item["id"],
        "description":None,
        "capabilities":[{"capability_id":"skill."+stable_id(item["capability"]),"relation":item.get("relation","EXPERIMENT")}],
        "admission_state":"DISCOVERED",
        "risk_class":"R2",
        "maturity_min":zero_maturity(),
        "permissions":{"filesystem_scopes":[],"process_execution":None,"shell_access":None,"gpu_access":None,"privilege_level":None},
        "network":{"outbound_required":None,"allowed_destinations":[parsed.hostname] if parsed.hostname else [],"inbound_listeners":[],"localhost_only":None},
        "data_scope":{"personal_data":None,"confidential_data":None,"customer_data":None,"secrets_credentials":None,"persistence_location":None,"retention":None},
        "local_feasibility":{"cpu":None,"ram":None,"gpu":None,"vram":None,"disk":None,"persistent_service":None,"external_api_dependency":None,"subscription_cost":0,"offline_capable":None,"degraded_mode":None},
        "provenance":{"source":source,"source_repo":source,"source_commit":None,"version":None,"artifact_hash":None,"license":None,"verified_at":None},
        "evidence":[],
        "skill":{
            "skill_name":item["id"].split(".")[-1],
            "trigger_description":None,
            "source_type":"upstream",
            "connectors":[],
            "tools":[],
            "scripts":[],
            "conflicts_with":[],
            "depends_on":[],
            "tests":[],
            "trigger_tests":[],
            "non_regression_tests":[],
            "last_verified_at":None
        },
        "registry_meta":{"family":item.get("family"),"candidate_id":item["id"],"source_status":"DISCOVERY_ONLY"}
    }

def convert(payload, source_kind):
    if source_kind=="chatgpt":
        env=payload["observed_environment"]
        observed=payload["observed_at"]
        return [chatgpt_item_to_record(x,env,observed) for x in payload.get("items",[])]
    if source_kind=="local":
        env=payload["environment"]
        out=[]
        for root in payload.get("roots",[]):
            for skill in root.get("skills",[]):
                out.append(local_skill_to_record(skill,env))
        return out
    if source_kind=="candidates":
        return [candidate_to_record(x) for x in payload.get("items",[])]
    raise ValueError("unsupported source kind")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("--kind",choices=["chatgpt","local","candidates"],required=True)
    ap.add_argument("--output",default="-")
    args=ap.parse_args()
    payload=json.loads(Path(args.input).read_text(encoding="utf-8"))
    records=convert(payload,args.kind)
    result={"record_count":len(records),"source_kind":args.kind,"records":records}
    data=json.dumps(result,ensure_ascii=False,indent=2)+"\n"
    if args.output=="-":
        print(data,end="")
    else:
        Path(args.output).write_text(data,encoding="utf-8")

if __name__=="__main__":
    main()
