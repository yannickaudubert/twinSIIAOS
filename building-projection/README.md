# SIIAOS Building Projection v1

This package defines the human/spatial projection of SIIAOS as Hall -> Buildings -> Floors -> Service Cells.

## Non-negotiable architectural rule

Buildings are **not** a second control plane and are **not** proof of runtime state.

Canonical runtime truth remains in the underlying SIIAOS objects and evidence chain. A building only projects stable references to capabilities, missions, teams, services, providers, policies and evidence.

The projection must preserve the distinction:

DESIGNED -> CODED -> TESTED -> DEPLOYED -> OBSERVED

and keep `desired_state` separate from `observed_state`.

Unknown runtime state stays `UNKNOWN`; Git or configuration state never promotes it automatically.

## Spatial semantics

The interface borrows the strongest semantics from spatial agent harnesses such as StarNet:

- room / service cell = capability-scoped work area;
- hallway / handoff lane = explicit authorised transfer path;
- placed object = visible capability/tool grant;
- agent presence = a projection of a real bounded run or assignment;
- deliverable object = a real artifact reference;
- alert = a real event/evidence condition.

SIIAOS deliberately differs on one point: **layout is not the source of truth**. Editing a room, route or object creates a desired-state proposal. It does not mutate runtime authority until Capability Core / policy / HumanGate allow the transition.

## Initial city

Universal entry:

- `HALL`

Six canonical first buildings:

- `BLD-CONSULT` — Cabinet augmente / missions clients
- `BLD-DSI` — DSI / infrastructure / GitOps / data / IA / security / operations
- `BLD-RADAR` — Hyperveille / recherche / qualification / experimentation
- `BLD-KNOW` — Connaissance / Vault / graph / methods / skills / learning
- `BLD-COM` — Communication / editorial / web / diffusion / media
- `BLD-REVENUE` — Opportunities / offers / procurement / customer success / economics

Admin/Delivery remains a cross-cutting backstage/control surface, not a seventh business building.

## Runtime mapping

Preferred providers are replaceable:

- agent runtime: Hermes Agent first, other harnesses through adapters;
- deterministic automation: n8n;
- local model gateway: LM Studio / llama.cpp-compatible endpoints;
- knowledge projection: Graphiti-compatible temporal graph plus canonical Vault;
- browser action: BrowserOS-compatible adapter;
- skill lifecycle: SIIAOS Skill Registry, with collective-learning patterns inspired by Ultron;
- spatial clients: web/2D first and optional Godot 3D client using the same JSON/event contracts.

No provider name is encoded as a permanent architectural dependency in the building schema.

## Files

- `building.schema.json` — descriptor contract
- `event.schema.json` — live projection event envelope
- `catalog.json` — city index
- `buildings/*.json` — Hall and the six first buildings
- `tests/test_catalog.py` — dependency-free structural smoke tests
