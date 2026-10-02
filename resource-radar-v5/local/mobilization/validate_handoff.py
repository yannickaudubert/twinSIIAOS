#!/usr/bin/env python3
"""Validate governed handoff from Radar response to human/cabinet/AgorIA mission."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


HUMAN_ROUTES = {"yannick_consultant", "cabinet_augmente", "agoria_collective"}


def validate_handoff(route: dict, context_pack: dict | None = None, mission_brief: dict | None = None) -> dict:
    errors: list[str] = []
    warnings: list[str] = []

    route_name = route.get("route")
    mandate = route.get("mandate", {})
    boundary = route.get("context_boundary", {})
    shareable = set(boundary.get("shareable_fields", []))
    local_only = set(boundary.get("local_only_fields", []))
    overlap = shareable & local_only
    if overlap:
        errors.append("champs simultanement partageables et local-only: " + ", ".join(sorted(overlap)))

    if route_name in HUMAN_ROUTES:
        if not mandate.get("required"):
            errors.append("une route humaine exige un mandat")
        if not mandate.get("human_gate"):
            errors.append("une route humaine exige un HumanGate")
        if context_pack is None:
            errors.append("ContextPack requis pour une route humaine")
        if mission_brief is None:
            warnings.append("MissionBrief non encore cree: la route reste une proposition")
    else:
        if mission_brief is not None:
            errors.append("aucun MissionBrief ne doit etre cree pour siiaos_local/no_activation")

    if context_pack is not None:
        policy = context_pack.get("share_policy", {})
        cp_share = set(policy.get("shareable_fields", []))
        cp_excluded = set(policy.get("excluded_fields", []))
        if cp_share & cp_excluded:
            errors.append("ContextPack contient un champ partageable et exclu")
        if route_name in HUMAN_ROUTES and not policy.get("human_approval_required", False):
            errors.append("partage du ContextPack humain sans approbation")
        decision = context_pack.get("decision_state", {})
        if decision.get("execution") == "unknown" or decision.get("admission") == "unknown":
            errors.append("un contexte inconnu ne peut pas etre passe en mission qualifiee")

    if mission_brief is not None:
        if mission_brief.get("route") not in HUMAN_ROUTES:
            errors.append("route de MissionBrief invalide")
        if mission_brief.get("human_gate") is not True:
            errors.append("MissionBrief sans HumanGate")
        if mission_brief.get("state") in {"active", "completed"}:
            errors.append("le validateur ne peut pas promouvoir automatiquement une mission active/completed")

    return {
        "valid": not errors,
        "errors": errors,
        "warnings": warnings,
        "route": route_name,
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--route", type=Path, required=True)
    p.add_argument("--context-pack", type=Path)
    p.add_argument("--mission-brief", type=Path)
    args = p.parse_args()

    route = json.loads(args.route.read_text(encoding="utf-8"))
    context_pack = json.loads(args.context_pack.read_text(encoding="utf-8")) if args.context_pack else None
    mission = json.loads(args.mission_brief.read_text(encoding="utf-8")) if args.mission_brief else None
    result = validate_handoff(route, context_pack, mission)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
