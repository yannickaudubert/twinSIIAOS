#!/usr/bin/env python3
"""Conservative execution planner for Resource Radar V5.

The planner is deterministic: it composes only what is described by the
Execution Estate and execution profiles. It never invents hardware, silently
adds a cloud provider, or turns missing observations into certainty.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


MODE_ORDER = {
    "deterministic": 0,
    "local_service": 1,
    "local_model": 2,
    "local_agent": 3,
    "human": 4,
    "external_optional": 5,
    "external_required": 6,
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _known_ram_mb(estate: dict) -> int | None:
    memory = estate.get("hardware", {}).get("memory", {})
    return int(memory["ram_mb"]) if memory.get("ram_mb") is not None else None


def _known_vram_mb(estate: dict) -> int | None:
    accelerators = estate.get("hardware", {}).get("accelerators")
    if accelerators is None:
        return None
    values = [item.get("vram_mb") for item in accelerators if item.get("vram_mb") is not None]
    if not values:
        return None
    return max(int(value) for value in values)


def _known_free_storage_gb(estate: dict) -> float | None:
    storage = estate.get("hardware", {}).get("storage")
    if storage is None:
        return None
    values = [item.get("free_gb") for item in storage if item.get("free_gb") is not None]
    if not values:
        return None
    return sum(float(value) for value in values)


def execution_mode(profile: dict) -> str:
    return profile.get("mode", {}).get("execution_mode", "local_service")


def incremental_cost(profile: dict) -> float:
    return float(profile.get("cost", {}).get("incremental_eur", 0) or 0)


def profile_availability(profile: dict, estate: dict, workload: dict) -> tuple[str, list[str]]:
    """Return available, unavailable, or unknown with explicit reasons."""
    req = profile.get("requirements", {})
    reasons: list[str] = []
    unknown: list[str] = []

    ram = _known_ram_mb(estate)
    min_ram = int(req.get("min_ram_mb") or 0)
    if min_ram:
        if ram is None:
            unknown.append("RAM non observee")
        elif ram < min_ram:
            reasons.append(f"RAM insuffisante: {ram} < {min_ram} MiB")

    vram = _known_vram_mb(estate)
    min_vram = int(req.get("min_vram_mb") or 0)
    if min_vram:
        if vram is None:
            unknown.append("VRAM non observee")
        elif vram < min_vram:
            reasons.append(f"VRAM insuffisante: {vram} < {min_vram} MiB")

    free_gb = _known_free_storage_gb(estate)
    need_gb = float(req.get("storage_gb") or 0)
    if need_gb:
        if free_gb is None:
            unknown.append("stockage libre non observe")
        elif free_gb < need_gb:
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

    mode = execution_mode(profile)
    estate_policy = estate.get("policy", {})
    constraints = workload.get("constraints", {})
    privacy_class = constraints.get("privacy_class")
    local_only_classes = set(estate_policy.get("data_classes_local_only", []))
    external_forbidden = (
        bool(constraints.get("local_only", False))
        or bool(constraints.get("offline_required", False))
        or (privacy_class in local_only_classes if privacy_class else False)
        or not bool(estate_policy.get("external_provider_dependency_allowed", False))
    )
    if mode in {"external_optional", "external_required"}:
        dependency = profile.get("cost", {}).get("external_dependency")
        allowed = set(constraints.get("allowed_external_providers", []))
        if external_forbidden:
            reasons.append("provider externe interdit par la politique")
        elif dependency and allowed and dependency not in allowed:
            reasons.append(f"provider externe non autorise pour ce workload: {dependency}")
        elif dependency and not allowed:
            reasons.append(f"aucun provider externe explicitement autorise pour ce workload: {dependency}")

    estate_budget = float(estate_policy.get("incremental_budget_eur", 0) or 0)
    workload_budget = float(constraints.get("incremental_budget_eur", 0) or 0)
    budget = min(estate_budget, workload_budget)
    cost = incremental_cost(profile)
    if cost > budget:
        reasons.append(f"cout incremental hors budget: {cost:g} > {budget:g} EUR")

    if reasons:
        return "unavailable", reasons
    if unknown:
        return "unknown", unknown
    return "available", []


def candidate_sort_key(profile: dict) -> tuple[int, float, str]:
    return (
        MODE_ORDER.get(execution_mode(profile), 99),
        incremental_cost(profile),
        profile.get("id", ""),
    )


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
    unknown_caps: list[str] = []
    rejected: list[str] = []
    substitutions: list[str] = []
    evidence_ids: set[str] = set()
    total_cost = 0.0
    external_dependencies: list[str] = []
    external_required = False

    for cap_spec in required + preferred:
        capability = cap_spec["capability"]
        candidates = sorted(
            [p for p in profiles if capability in p.get("capabilities", [])],
            key=candidate_sort_key,
        )
        accepted = None
        saw_unknown = False
        considered: list[str] = []

        for profile in candidates:
            considered.append(profile.get("id", "profile"))
            availability, reasons = profile_availability(profile, estate, workload)
            if availability == "available":
                accepted = profile
                break
            if availability == "unknown":
                saw_unknown = True
            rejected.append(
                f"{profile.get('id', 'profile')} pour {capability}: " + "; ".join(reasons)
            )

        if accepted is None:
            if cap_spec in required:
                if saw_unknown:
                    unknown_caps.append(capability)
                else:
                    uncovered.append(capability)
            continue

        if len(considered) > 1:
            substitutions.append(
                f"{capability}: " + " -> ".join(considered)
            )

        req = accepted.get("requirements", {})
        provenance = accepted.get("provenance", {})
        evidence_ids.update(provenance.get("evidence_ids", []))
        resource_id = accepted.get("resource_id")
        mode = execution_mode(accepted)
        total_cost += incremental_cost(accepted)
        dep = accepted.get("cost", {}).get("external_dependency")
        if dep:
            external_dependencies.append(dep)
        external_required = external_required or mode == "external_required" or bool(
            accepted.get("cost", {}).get("external_required", False)
        )
        steps.append({
            "id": f"step-{len(steps)+1}",
            "capability": capability,
            "execution_mode": mode,
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

    estate_policy = estate.get("policy", {})
    constraints = workload.get("constraints", {})
    budget = min(
        float(estate_policy.get("incremental_budget_eur", 0) or 0),
        float(constraints.get("incremental_budget_eur", 0) or 0),
    )

    if uncovered:
        status = "not_feasible"
    elif unknown_caps:
        status = "unknown"
    else:
        status = "feasible"

    basis = [
        "composition deterministe a partir de profils d'execution declares ou observes",
        f"budget incremental autorise: {budget:g} EUR",
        "configuration inconnue conservee comme inconnue" if unknown_caps else "configuration suffisante pour les profils retenus",
        "provider externe interdit"
        if (
            constraints.get("local_only", False)
            or constraints.get("offline_required", False)
            or (
                constraints.get("privacy_class") in set(estate_policy.get("data_classes_local_only", []))
                if constraints.get("privacy_class") else False
            )
            or not estate_policy.get("external_provider_dependency_allowed", False)
        )
        else "provider externe autorise mais non privilegie",
    ]

    residual = uncovered + unknown_caps
    return {
        "id": f"plan:{estate['id']}:{workload['id']}",
        "estate_id": estate["id"],
        "workload_id": workload["id"],
        "state": "candidate",
        "feasibility": {
            "status": status,
            "basis": basis,
            "constraints": residual,
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
            "incremental_eur": total_cost,
            "external_dependencies": sorted(set(external_dependencies)),
            "external_dependencies_required": external_required,
        },
        "gap_analysis": {
            "uncovered_capabilities": uncovered,
            "unknown_capabilities": unknown_caps,
            "substitutions_considered": substitutions,
            "rejected_options": rejected,
            "residual_gaps": residual,
        },
        "benchmark_ids": [],
        "evidence_ids": sorted(evidence_ids),
        "visibility": "local_private",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--estate", type=Path, required=True)
    parser.add_argument("--workload", type=Path, required=True)
    parser.add_argument("--profiles", type=Path, required=True)
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
