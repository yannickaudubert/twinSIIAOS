#!/usr/bin/env python3
import argparse
import hashlib
import json
import re
from pathlib import Path

PATTERNS={
  "network_download": re.compile(r"\b(curl|wget|Invoke-WebRequest|requests\.(get|post)|urllib\.request|fetch\()\b",re.I),
  "shell_execution": re.compile(r"\b(subprocess\.|os\.system|child_process|exec\(|spawn\(|powershell|cmd\.exe|bash\s+-c)\b",re.I),
  "dynamic_eval": re.compile(r"\b(eval\(|exec\(|new\s+Function\b)",re.I),
  "secret_terms": re.compile(r"\b(API[_-]?KEY|TOKEN|PASSWORD|SECRET|PRIVATE[_-]?KEY)\b",re.I),
  "filesystem_delete": re.compile(r"\b(rm\s+-rf|Remove-Item\s+.*-Recurse|shutil\.rmtree|os\.remove|unlink\()\b",re.I)
}

TEXT_SUFFIXES={".md",".py",".js",".ts",".tsx",".sh",".ps1",".json",".yaml",".yml",".toml",".txt"}

def sha256(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""):
            h.update(chunk)
    return h.hexdigest()

def scan_skill(root):
    root=Path(root).resolve()
    findings=[]
    files=[]
    for p in sorted(x for x in root.rglob("*") if x.is_file()):
        rel=p.relative_to(root).as_posix()
        item={"path":rel,"bytes":p.stat().st_size,"sha256":sha256(p),"findings":[]}
        if p.suffix.lower() in TEXT_SUFFIXES and p.stat().st_size<=2_000_000:
            text=p.read_text(encoding="utf-8",errors="replace")
            for kind,rx in PATTERNS.items():
                matches=rx.findall(text)
                if matches:
                    item["findings"].append({"kind":kind,"count":len(matches)})
                    findings.append({"path":rel,"kind":kind,"count":len(matches)})
        files.append(item)
    score=0
    weights={"network_download":2,"shell_execution":3,"dynamic_eval":4,"secret_terms":1,"filesystem_delete":4}
    for f in findings:
        score+=weights.get(f["kind"],1)*f["count"]
    risk="LOW" if score==0 else "MEDIUM" if score<8 else "HIGH"
    return {
      "scanner_version":"0.1",
      "root":str(root),
      "file_count":len(files),
      "files":files,
      "findings":findings,
      "heuristic_score":score,
      "heuristic_risk":risk,
      "rule":"Static heuristics are an admission signal only; they are not a security verdict."
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("skill_dir")
    ap.add_argument("--output",default="-")
    args=ap.parse_args()
    result=scan_skill(args.skill_dir)
    data=json.dumps(result,ensure_ascii=False,indent=2)+"\n"
    if args.output=="-":
        print(data,end="")
    else:
        Path(args.output).write_text(data,encoding="utf-8")

if __name__=="__main__":
    main()
