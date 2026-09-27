#!/usr/bin/env python3
import argparse
import hashlib
import json
from pathlib import Path

def sha256(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""):
            h.update(chunk)
    return h.hexdigest()

def parse_frontmatter(text):
    if not text.startswith("---"):
        return {}
    parts=text.split("---",2)
    if len(parts)<3:
        return {}
    data={}
    for raw in parts[1].splitlines():
        line=raw.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key,value=line.split(":",1)
        key=key.strip()
        value=value.strip().strip('"').strip("'")
        if key in {"name","description"}:
            data[key]=value
    return data

def inspect_skill(entrypoint, root):
    text=entrypoint.read_text(encoding="utf-8",errors="replace")
    meta=parse_frontmatter(text)
    folder=entrypoint.parent
    files=[]
    for path in sorted(p for p in folder.rglob("*") if p.is_file()):
        rel=path.relative_to(folder).as_posix()
        files.append({
            "path":rel,
            "bytes":path.stat().st_size,
            "sha256":sha256(path)
        })
    return {
        "name":meta.get("name") or folder.name,
        "description":meta.get("description"),
        "entrypoint":entrypoint.relative_to(root).as_posix(),
        "skill_dir":folder.relative_to(root).as_posix(),
        "entrypoint_sha256":sha256(entrypoint),
        "file_count":len(files),
        "files":files
    }

def scan_root(root):
    root=root.expanduser().resolve()
    entrypoints=sorted(set(root.rglob("SKILL.md"))|set(root.rglob("skill.md")))
    return {
        "root":str(root),
        "exists":root.exists(),
        "skill_count":len(entrypoints),
        "skills":[inspect_skill(p,root) for p in entrypoints]
    }

def main():
    ap=argparse.ArgumentParser(description="Inventory local skill folders without installing or executing them.")
    ap.add_argument("roots",nargs="+",help="One or more directories to scan")
    ap.add_argument("--environment",default="unspecified-local-environment")
    ap.add_argument("--output",default="-")
    args=ap.parse_args()

    payload={
        "inventory_version":"0.1",
        "environment":args.environment,
        "roots":[scan_root(Path(p)) for p in args.roots],
        "rule":"Inventory proves filesystem presence only; it does not prove admission, compatibility, activation or successful execution."
    }
    data=json.dumps(payload,ensure_ascii=False,indent=2)+"\n"
    if args.output=="-":
        print(data,end="")
    else:
        Path(args.output).write_text(data,encoding="utf-8")

if __name__=="__main__":
    main()
