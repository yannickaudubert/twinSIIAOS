# Front A — A06 and A07

Status: CODED; deterministic execution proof still pending.

## A06 — Data / Privacy / Tenant boundaries

A governed data reference never becomes tenant-neutral by accident.

Invariants:
- every governed data reference has exactly one tenant;
- classification is explicit: PUBLIC / INTERNAL / CONFIDENTIAL / RESTRICTED;
- purpose and retention are explicit;
- CONFIDENTIAL is local-by-default or local-only and export requires a gate;
- RESTRICTED is local-only and export is double-approval-or-forbidden;
- locator references identify data without embedding content or secret material in the contract.

## A07 — Document / Record lifecycle

A Document is mutable editorial state. A Record is an immutable capture of one document version with digest, actor, evidence and lineage.

Invariants:
- no document silently becomes a record;
- record capture is explicit and timestamped;
- records carry content digest and evidence;
- supersession creates a new record; it does not rewrite the old one;
- tenant/classification remain explicit through the lifecycle.
