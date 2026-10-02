#!/usr/bin/env python3
"""Deterministic mobilization router for Resource Radar V5.

This module proposes a mobilization route. It does not activate a mission,
contact people, or share context.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def route_mobilization(response_context: dict) -> dict:
    unknowns = list(response_context.get("unknowns", []))
    execution = response_context.get("execution", {})
    admission = response_context.get("admission", {})
    complexity = response_context.get("complexity", {})
    needs = response_context.get("needs", {})
    evidence_ids = sorted(set(response_context.get("evidence_ids", [])))

    execution_status = execution.get("status", "unknown")
    admission_verdict = admission.get("verdict", "unknown")

    required_domains = list(needs.get("required_domains", []))
    human_judgement = bool(needs.get("human_judgement_required", False))
    structured_delivery = bool(needs.get("structured_delivery_required", False))
    collective_coordination = bool(needs.get("collective_coordination_required", False))
    territorial = int(complexity.get("territorial_ecosystem", 0) or 0)
    organisational = int(complexity.get("organisational", 0) or 0)
    human_change = int(complexity.get("human_change", 0) or 0)

    shareable = list(response_context.get("context_boundary", {}).get("shareable_fields", []))
    local_only = list(response_context.get("context_boundary", {}).get("local_only_fields", []))

    if execution_status == "unknown" or admission_verdict == "unknown":
        route = "no_activation"
        reasons = ["preuve ou contexte insuffisant pour proposer une activation qualifiée"]
        gap = unknowns or ["qualification incomplete"]
        team_shape = "none"
        mandate_required = False
        human_gate = False
    elif admission_verdict == "blocked":
        route = "no_activation"
        reasons = ["admission organisationnelle bloquée"]
        gap = list(admission.get("blocking_reasons", []))
        team_shape = "none"
        mandate_required = False
        human_gate = False
    elif (
        execution_status == "feasible"
        and admission_verdict == "eligible"
        and not human_judgement
        and not structured_delivery
        and not collective_coordination
        and len(required_domains) <= 1
        and max(territorial, organisational, human_change) <= 1
    ):
        route = "siiaos_local"
        reasons = ["la capacité est réalisable et admissible en self-service local"]
        gap = []
        team_shape = "none"
        mandate_required = False
        human_gate = False
    elif collective_coordination or len(required_domains) >= 2 or territorial >= 3:
        route = "agoria_collective"
        reasons = ["plusieurs domaines autonomes ou une coordination collective sont requis"]
        gap = list(needs.get("self_service_gap", []))
        team_shape = "multi_domain" if len(required_domains) >= 2 else "single_specialist"
        mandate_required = True
        human_gate = True
    elif structured_delivery or organisational >= 3 or human_change >= 3:
        route = "cabinet_augmente"
        reasons = ["une mission structurée de transformation ou de delivery est requise"]
        gap = list(needs.get("self_service_gap", []))
        team_shape = "agentic_delivery"
        mandate_required = True
        human_gate = True
    else:
        route = "yannick_consultant"
        reasons = ["un arbitrage, jugement professionnel ou mandat humain ciblé est requis"]
        gap = list(needs.get("self_service_gap", []))
        team_shape = "single_specialist"
        mandate_required = True
        human_gate = True

    if admission_verdict == "human_gate" and route == "siiaos_local":
        route = "yannick_consultant"
        reasons = ["l'admission impose un HumanGate avant toute activation"]
        team_shape = "single_specialist"
        mandate_required = True
        human_gate = True

    return {
        "id": response_context.get("id", "route:generated"),
        "route": route,
        "state": "proposed",
        "reasons": reasons,
        "self_service_gap": gap,
        "required_capabilities": list(needs.get("required_capabilities", [])),
        "required_domains": required_domains,
        "team_shape": team_shape,
        "mandate": {
            "required": mandate_required,
            "human_gate": human_gate,
            "authority_scope": list(needs.get("authority_scope", [])),
            "client_or_user_acceptance_required": mandate_required,
        },
        "context_boundary": {
            "shareable_fields": shareable,
            "local_only_fields": local_only,
            "context_pack_required": route in {"cabinet_augmente", "agoria_collective"},
        },
        "evidence_ids": evidence_ids,
        "visibility": "local_private",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--context", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    result = route_mobilization(load_json(args.context))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{result['route']}: {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
