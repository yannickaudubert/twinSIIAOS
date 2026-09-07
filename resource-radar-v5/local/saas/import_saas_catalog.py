#!/usr/bin/env python3
"""Import an assessed SaaS catalog as local canonical Resource Records."""
from __future__ import annotations
import argparse, json
from pathlib import Path

def load_catalog(path):
    data=json.loads(Path(path).read_text(encoding='utf-8'))
    if data.get('schema')!='siiaos.saas-augmentation-catalog.v0.2': raise ValueError('unsupported SaaS catalog schema')
    if not isinstance(data.get('items'),list): raise ValueError('catalog items must be a list')
    return data

def validate(record):
    required=['id','kind','title','capabilities','state','publication','control_profile']
    missing=[k for k in required if k not in record]
    if missing: raise ValueError(f"missing keys for {record.get('id','<unknown>')}: {missing}")
    scores=(record['control_profile'].get('scores') or {})
    for key in ('augmentability','reversibility','governance','siiaos_control','lock_in'):
        value=scores.get(key)
        if not isinstance(value,(int,float)) or not 0<=value<=100: raise ValueError(f"invalid score {key}={value!r} for {record['id']}")
    publication=record.get('publication') or {}
    if publication.get('radar_public') or publication.get('consultant_site'):
        raise ValueError('seed import must stay local until explicit publication decision')

def import_catalog(path):
    records=[]; seen=set()
    for record in load_catalog(path)['items']:
        if not isinstance(record,dict): raise ValueError('catalog item must be an object')
        validate(record)
        if record['id'] in seen: raise ValueError(f"duplicate resource id: {record['id']}")
        seen.add(record['id']); records.append(record)
    return records

def write_records(records,out_dir):
    out=Path(out_dir); out.mkdir(parents=True,exist_ok=True)
    for record in records:
        name=record['id'].replace(':','__').replace('/','_')+'.json'
        (out/name).write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def main():
    p=argparse.ArgumentParser(); p.add_argument('catalog'); p.add_argument('--out',required=True); a=p.parse_args(); records=import_catalog(a.catalog); write_records(records,a.out); print(f"imported {len(records)} SaaS records into {a.out}"); return 0
if __name__=='__main__': raise SystemExit(main())
