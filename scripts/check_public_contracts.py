#!/usr/bin/env python3
"""Checks public contracts and fixtures without third-party dependencies."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [ROOT / "contracts", ROOT / "examples"]

# Construct instance-specific tokens so this checker does not flag itself.
FORBIDDEN_INSTANCE_TOKENS = ["ARA" + "GORN", "Corpus_" + "Audubert"]
ABSOLUTE_PATH_PATTERNS = [
    re.compile(r"\b[A-Za-z]:[/\\]"),
    re.compile(r"/home/[A-Za-z0-9_.-]+/"),
    re.compile(r"/Users/[A-Za-z0-9_.-]+/"),
]
SECRET_PATTERNS = [
    re.compile(r"(?i)(api[_-]?key|access[_-]?token|secret|password)\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{12,}"),
    re.compile(r"ghp_[A-Za-z0-9]{20,}"),
]


def iter_files():
    for root in TARGETS:
        if not root.exists():
            continue
        yield from (p for p in root.rglob("*") if p.is_file())


def main() -> int:
    errors: list[str] = []
    json_count = 0

    for path in iter_files():
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(ROOT)

        for token in FORBIDDEN_INSTANCE_TOKENS:
            if token.lower() in text.lower():
                errors.append(f"{rel}: instance-specific token detected")

        for pattern in ABSOLUTE_PATH_PATTERNS:
            if pattern.search(text):
                errors.append(f"{rel}: absolute local path detected")

        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                errors.append(f"{rel}: possible secret detected")

        if path.suffix == ".json":
            json_count += 1
            try:
                json.loads(text)
            except json.JSONDecodeError as exc:
                errors.append(f"{rel}: invalid JSON: {exc}")

    if json_count == 0:
        errors.append("no JSON contracts or fixtures found")

    schema = ROOT / "contracts" / "core.schema.json"
    if not schema.exists():
        errors.append("contracts/core.schema.json missing")
    else:
        data = json.loads(schema.read_text(encoding="utf-8"))
        required_defs = {
            "context",
            "need",
            "fact",
            "evidence",
            "responsibility_profile",
            "capability_passport",
            "observation_request",
            "summit",
            "path_candidate",
            "action_plan",
        }
        missing = sorted(required_defs - set(data.get("$defs", {})))
        if missing:
            errors.append("core schema missing definitions: " + ", ".join(missing))

    if errors:
        print("Public contract checks FAILED")
        for error in errors:
            print("-", error)
        return 1

    print(f"Public contract checks OK: {json_count} JSON files inspected")
    return 0


if __name__ == "__main__":
    sys.exit(main())
