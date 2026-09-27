#!/usr/bin/env python3
"""Deterministic organisational admission assessment for Resource Radar V5."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

RISK_ORDER = {"R0": 0, "R1": 1, "R2": 2, "R3": 3, "R4": 4}
TERMINAL_BLOCK = {"blocked", "hold", "rejected", "retired"}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def assess_admission(profile: dict, context: dict) -> dict:
    reasons: list[str] = []
    human_gate_reasons: list[str] = []
    unknowns: list[str] = []

    state = profile.get("admission_state", "unknown")
    if state in TERMINAL_BLOCK:
        reasons.append(f"etat d'admission bloquant: {state}")

    maturity = context.get("maturity", {})
    required = profile.get("maturity_min", {})
    maturity_gaps = {}
    for dim, minimum in required.items():
        actual = maturity.get(dim)
        if actual is None:
            unknowns.append(f"maturite non observee: {dim}")
        elif actual < minimum:
            maturity_gaps[dim] = {"actual": actual, "required": minimum}
    if maturity_gaps:
        reasons.append("maturite organisationnelle insuffisante")

    risk = profile.get("risk_class")
    if risk not in RISK_ORDER:
        unknowns.append("classe de risque inconnue")
    elif risk in {"R3", "R4"}:
        human_gate_reasons.append(f"{risk} impose un HumanGate explicite")

    permissions = profile.get("permissions", {})
    network = profile.get("network", {})
    policy = context.get("risk_policy", {})

    if permissions.get("shell_access") is True and policy.get("allow_shell_access") is False:
        reasons.append("shell access interdit par la politique")
    if permissions.get("privilege_level") in {"elevated", "system"} and policy.get("allow_elevated_privileges") is False:
        reasons.append("privileges eleves interdits par la politique")
    if network.get("external_writes") is True and policy.get("allow_external_writes") is False:
        reasons.append("ecritures externes interdites par la politique")

    rollback_defined = profile.get("reversibility", {}).get("rollback_defined")
    if rollback_defined is False and state in {"experiment", "admitted", "pinned", "observed"}:
        reasons.append("rollback requis pour admission/exploitation")
    elif rollback_defined is None:
        unknowns.append("reversibilite non observee")

    if reasons:
        verdict = "blocked"
    elif unknowns:
        verdict = "unknown"
    elif human_gate_reasons:
        verdict = "human_gate"
    else:
        verdict = "eligible"

    return {
        "profile_id": profile.get("id"),
        "resource_id": profile.get("resource_id"),
        "organisation_context_id": context.get("id"),
        "verdict": verdict,
        "risk_class": risk,
        "maturity_gaps": maturity_gaps,
        "blocking_reasons": reasons,
        "human_gate_reasons": human_gate_reasons,
        "unknowns": unknowns,
        "evidence_ids": profile.get("evidence_ids", []),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", type=Path, required=True)
    parser.add_argument("--context", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    result = assess_admission(load_json(args.profile), load_json(args.context))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{result['verdict']}: {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
