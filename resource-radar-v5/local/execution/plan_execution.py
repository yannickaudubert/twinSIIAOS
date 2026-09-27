#!/usr/bin/env python3
"""Compose a conservative local execution plan from an Estate, a Workload and execution profiles.

This planner is intentionally deterministic. It does not invent missing hardware,
benchmarks or capabilities and does not call an external provider.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def available_vram_mb(estate: dict) -> int:
    accelerators = estate.get("hardware", {}).get("accelerators", [])
    return max((int(item.get("vram_mb") or 0) for item in accelerators), default=0)


def resource_available(profile: dict, estate: dict) -> tuple[bool, list[str]]:
    req = profile.get("requirements", {})
    reasons: list[str] = []

    ram = int(estate.get("hardware", {}).get("memory", {}).get("ram_mb") or 0)
    min_ram = int(req.get("min_ram_mb") or 0)
    if min_ram and ram < min_ram:
        reasons.append(f"RAM insuffisante: {ram} < {min_ram} MiB")

    vram = available_vram_mb(estate)
    min_vram = int(req.get("min_vram_mb") or 0)
    if min_vram and vram < min_vram:
        reasons.append(f"VRAM insuffisante: {vram} < {min_vram} MiB")

    storage = estate.get("hardware", {}).get("storage", [])
    free_gb = sum(float(item.get("free_gb") or 0) for item in storage)
    need_gb = float(req.get("storage_gb") or 0)
    if need_gb and free_gb < need_gb:
        reasons.append(f"stockage libre insuffisant: {free_gb:g} < {need_gb:g} GiB")

    software = estate.get("software", {})
    runtimes = set(software.get("container_runtimes", []))
    runtimes.update(software.get("language_runtimes", []))
    runtimes.update(software.get("model_servers", []))
    runtimes.update(software.get("tool_ids", []))
    required_runtimes = set(req.get("runtime_ids", []))
    missing_runtimes = required_runtimes - runtimes
    if missing_runtimes:
        reasons.append("runtimes absents: " + ", ".join(sorted(missing_runtimes)))

    services = set(software.get("service_ids", []))
    required_services = set(req.get("service_ids", []))
    missing_services = required_services - services
    if missing_services:
        reasons.append("services absents: " + ", ".join(sorted(missing_services)))

    return not reasons, reasons


def compose_plan(estate: dict, workload: dict, profiles: list[dict]) -> dict:
    required = [
        item for item in workload.get("required_capabilities", [])
        if item.get("priority", "required") == "required"
    ]
    preferred = [
        item for item in workload.get("required_capabilities", [])
        if item.get("priority") == "preferred"
    ]

    steps: list[dict] = []
    uncovered: list[str] = []
    rejected: list[str] = []
    evidence_ids: set[str] = set()

    for cap_spec in required + preferred:
        capability = cap_spec["capability"]
        candidates = [p for p in profiles if capability in p.get("capabilities", [])]
        accepted = None
        for profile in candidates:
            ok, reasons = resource_available(profile, estate)
            if ok:
                accepted = profile
                break
            rejected.append(f"{profile.get('id', 'profile')} pour {capability}: " + "; ".join(reasons))

        if accepted is None:
            if cap_spec in required:
                uncovered.append(capability)
            continue

        req = accepted.get("requirements", {})
        provenance = accepted.get("provenance", {})
        evidence_ids.update(provenance.get("evidence_ids", []))
        resource_id = accepted.get("resource_id")
        steps.append({
            "id": f"step-{len(steps)+1}",
            "capability": capability,
            "execution_mode": "local_service",
            "resource_ids": [resource_id] if resource_id else [],
            "execution_profile_ids": [accepted["id"]],
            "implementation": accepted.get("mode", {}).get("name", accepted["id"]),
            "expected": {
                "ram_mb": int(req.get("recommended_ram_mb") or req.get("min_ram_mb") or 0),
                "vram_mb": int(req.get("recommended_vram_mb") or req.get("min_vram_mb") or 0),
                "storage_gb": float(req.get("storage_gb") or 0),
            },
            "evidence_ids": provenance.get("evidence_ids", []),
        })

    policy = estate.get("policy", {})
    workload_constraints = workload.get("constraints", {})
    budget = min(
        float(policy.get("incremental_budget_eur", 0)),
        float(workload_constraints.get("incremental_budget_eur", 0)),
    )
    external_allowed = bool(policy.get("external_provider_dependency_allowed", False))
    local_only = bool(workload_constraints.get("local_only", False))
    status = "feasible" if not uncovered else "not_feasible"

    basis = [
        "composition deterministe a partir de profils d'execution declares ou observes",
        f"budget incremental autorise: {budget:g} EUR",
        "provider externe interdit" if (local_only or not external_allowed) else "provider externe autorise mais non requis par ce plan",
    ]

    return {
        "id": f"plan:{estate['id']}:{workload['id']}",
        "estate_id": estate["id"],
        "workload_id": workload["id"],
        "state": "candidate",
        "feasibility": {
            "status": status,
            "basis": basis,
            "constraints": uncovered,
            "evidence_ids": sorted(evidence_ids),
        },
        "steps": steps or [{
            "id": "step-none",
            "capability": "uncovered",
            "execution_mode": "deterministic",
            "resource_ids": [],
            "execution_profile_ids": [],
            "implementation": "aucun plan executable sans donnee supplementaire",
            "expected": {"ram_mb": 0, "vram_mb": 0, "storage_gb": 0},
            "evidence_ids": [],
        }],
        "cost": {
            "incremental_eur": 0,
            "external_dependencies": [],
            "external_dependencies_required": False,
        },
        "gap_analysis": {
            "uncovered_capabilities": uncovered,
            "substitutions_considered": [],
            "rejected_options": rejected,
            "residual_gaps": uncovered,
        },
        "benchmark_ids": [],
        "evidence_ids": sorted(evidence_ids),
        "visibility": "local_private",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--estate", type=Path, required=True)
    parser.add_argument("--workload", type=Path, required=True)
    parser.add_argument("--profiles", type=Path, required=True, help="JSON file containing an array, or a directory of JSON profiles")
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    estate = load_json(args.estate)
    workload = load_json(args.workload)
    if args.profiles.is_dir():
        profiles = [load_json(path) for path in sorted(args.profiles.glob("*.json"))]
    else:
        raw = load_json(args.profiles)
        profiles = raw if isinstance(raw, list) else [raw]

    plan = compose_plan(estate, workload, profiles)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{plan['feasibility']['status']}: {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
