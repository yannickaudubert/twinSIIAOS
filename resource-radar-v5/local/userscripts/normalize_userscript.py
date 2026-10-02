#!/usr/bin/env python3
"""Normalize an acquired userscript into Radar V5 objects without executing it."""
from __future__ import annotations
import argparse, hashlib, json, re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

RISK={"unknown":-1,"low":0,"medium":1,"high":2,"critical":3}

def parse_metadata(source):
    inside=False; out={}
    for raw in source.splitlines():
        line=raw.strip()
        if "==UserScript==" in line: inside=True; continue
        if "==/UserScript==" in line: break
        if not inside: continue
        m=re.match(r"^//\s*@([A-Za-z0-9:_-]+)\s*(.*)$",line)
        if m: out.setdefault(m.group(1),[]).append(m.group(2).strip())
    return out

def vals(meta,key): return [v for v in meta.get(key,[]) if v]
def first(meta,*keys):
    for key in keys:
        v=vals(meta,key)
        if v:return v[0]
    return None

def slug(value): return re.sub(r"[^a-z0-9]+","-",value.lower()).strip("-") or "unnamed"
def hosts(meta):
    out=set()
    for pattern in vals(meta,"match")+vals(meta,"include"):
        candidate=pattern.replace("*://","https://",1)
        try: host=urlparse(candidate).hostname
        except ValueError: host=None
        if host: out.add(host.lstrip("*."))
    return sorted(out)
def bump(level,candidate): return candidate if RISK[candidate]>RISK[level] else level

def assess(source,meta):
    level="low"; reasons=[]; grants=set(vals(meta,"grant")); connects=vals(meta,"connect"); requires=vals(meta,"require"); matches=vals(meta,"match")+vals(meta,"include")
    if not grants or grants=={"none"}: reasons.append("no privileged userscript grants declared")
    sensitive=sorted(grants.intersection({"GM_cookie","GM.cookies","GM_webRequest"}))
    if sensitive: level=bump(level,"critical"); reasons.append("sensitive browser/session grant: "+", ".join(sensitive))
    if "unsafeWindow" in grants: level=bump(level,"high"); reasons.append("unsafeWindow crosses userscript isolation")
    if {"GM_xmlhttpRequest","GM.xmlHttpRequest"}.intersection(grants): level=bump(level,"medium"); reasons.append("privileged cross-origin request capability")
    if "*" in connects: level=bump(level,"high"); reasons.append("wildcard @connect")
    elif connects: level=bump(level,"medium"); reasons.append("outbound hosts: "+", ".join(connects[:8]))
    if requires: level=bump(level,"medium"); reasons.append("remote @require dependencies need pinning/audit")
    if any(x in {"*://*/*","http*://*/*"} for x in matches): level=bump(level,"high"); reasons.append("script matches essentially the whole web")
    for pattern,candidate,reason in [(r"\beval\s*\(","critical","dynamic eval() detected"),(r"\bnew\s+Function\s*\(","critical","dynamic Function constructor detected"),(r"access[_-]?token|session[_-]?token|authorization\s*:\s*['\"]?bearer","critical","token/session handling pattern detected"),(r"document\.cookie","high","direct cookie access detected")]:
        if re.search(pattern,source,re.I): level=bump(level,candidate); reasons.append(reason)
    return level,reasons,{"low":"test","medium":"test","high":"rewrite","critical":"block","unknown":"monitor"}[level]

def normalize(source,target_resource,source_catalog,observed_at=None):
    meta=parse_metadata(source); name=first(meta,"name") or "Unnamed userscript"; namespace=first(meta,"namespace") or source_catalog; version=first(meta,"version") or "unknown"; digest=hashlib.sha256(source.encode()).hexdigest(); observed=observed_at or datetime.now(timezone.utc).isoformat().replace("+00:00","Z"); level,reasons,action=assess(source,meta); rid=f"augmentation:userscript:{slug(name)}:{hashlib.sha256((namespace+'|'+name+'|'+version+'|'+digest[:16]).encode()).hexdigest()[:12]}"; source_url=first(meta,"homepageURL","homepage","source","downloadURL","updateURL")
    augmentation={"mechanism":"userscript","source_catalog":source_catalog,"upstream_name":name,"upstream_namespace":namespace,"upstream_version":version,"target_resource":target_resource,"target_hosts":hosts(meta),"metadata":{"match":vals(meta,"match"),"include":vals(meta,"include"),"grant":vals(meta,"grant"),"connect":vals(meta,"connect"),"require":vals(meta,"require"),"resource":vals(meta,"resource"),"run_at":first(meta,"run-at")},"sha256":digest,"risk_level":level,"risk_reasons":reasons,"review_status":"discovered","recommended_action":action}
    resource={"id":rid,"kind":"tool","title":name,"summary":first(meta,"description") or f"Userscript discovered via {source_catalog}.","source_url":source_url,"capabilities":["browser augmentation"],"approaches":["augment without migration","userscript"],"state":"observed","maturity":"community-discovered","last_verified_at":observed,"verified_on":["metadata-static-analysis"],"known_gaps":["not executed by this adapter","runtime behavior requires isolated testing"],"augmentation":augmentation,"publication":{"local":True,"radar_public":False,"consultant_site":False,"visibility":"local_private"},"updated_at":observed}
    eh=hashlib.sha256(f"{rid}|{target_resource}|augments".encode()).hexdigest()[:16]
    edge={"id":f"edge:augmentation:{eh}","from":rid,"to":target_resource,"relation":"augments","provenance":{"source":source_catalog,"source_url":source_url,"observed_at":observed,"method":"scanned","confidence":"medium","evidence_ids":[],"raw_ref":digest},"visibility":"local_private","properties":{"mechanism":"userscript","risk_level":level,"recommended_action":action,"review_status":"discovered"},"created_at":observed,"updated_at":observed}
    oh=hashlib.sha256(f"{rid}|security|{digest}".encode()).hexdigest()[:16]
    observation={"id":f"observation:userscript-security:{oh}","subject_id":rid,"kind":"security","observed_at":observed,"source":{"name":source_catalog,"url":source_url,"method":"scan","adapter":"normalize_userscript","adapter_version":"0.1.0"},"claim":"Static userscript metadata and source-code security screening","value":{"risk_level":level,"risk_reasons":reasons,"recommended_action":action,"target_hosts":augmentation["target_hosts"],"grants":augmentation["metadata"]["grant"],"connect":augmentation["metadata"]["connect"],"requires":augmentation["metadata"]["require"]},"confidence":"medium","evidence_ids":[],"raw_ref":digest,"visibility":"local_private"}
    return {"resource":resource,"edge":edge,"observation":observation}

def main():
    p=argparse.ArgumentParser(); p.add_argument("source"); p.add_argument("--target-resource",required=True); p.add_argument("--source-catalog",required=True); p.add_argument("--out"); a=p.parse_args(); payload=normalize(Path(a.source).read_text(encoding="utf-8"),a.target_resource,a.source_catalog); rendered=json.dumps(payload,ensure_ascii=False,indent=2)+"\n"; Path(a.out).write_text(rendered,encoding="utf-8") if a.out else print(rendered,end=""); return 0
if __name__=="__main__": raise SystemExit(main())
