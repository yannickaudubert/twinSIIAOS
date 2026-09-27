#!/usr/bin/env python3
from pathlib import Path
import hashlib
import sys

ROOT = Path(__file__).resolve().parents[2]

PAIRS = [
    (
        ROOT / "capability-core" / "engine.js",
        ROOT / "public-resource-hub" / "vendor" / "capability-core.js",
        "capability core web vendor"
    ),
    (
        ROOT / "resource-radar-v3" / "registry.bootstrap.json",
        ROOT / "public-resource-hub" / "data" / "registry.bootstrap.json",
        "registry web projection"
    ),
]

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    bad = []
    for canonical, projected, label in PAIRS:
        if not canonical.exists() or not projected.exists():
            bad.append((label, "missing file"))
            continue
        if canonical.read_bytes() != projected.read_bytes():
            bad.append((label, f"{digest(canonical)} != {digest(projected)}"))
    if bad:
        for label, reason in bad:
            print(f"DRIFT: {label}: {reason}", file=sys.stderr)
        return 1
    print("No projection drift detected.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
