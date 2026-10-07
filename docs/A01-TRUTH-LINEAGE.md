# Front A — A01 Truth / Lineage

Status: CODED + TESTED LOCALLY, not promoted.

## Purpose

A01 freezes the canonical vocabulary for truth and provenance without introducing a new runtime service.

Canonical truth statuses:
- PROVEN
- OBSERVED
- DECLARED
- PROPOSED
- FAILED
- UNKNOWN

These statuses are intentionally distinct from:
- derivation method: direct_observation / declaration / inference / calculation / proposal / test_result / unknown;
- validation state: unreviewed / checked / validated / rejected;
- state view: desired / declared / observed / effective.

This separation prevents a recurring ambiguity where “inferred” or “validated” were treated as truth states.

## Contracts

- `contracts/truth.schema.json`
- `contracts/source-lineage.schema.json`

## Invariants

1. UNKNOWN is explicit and does not mean failure.
2. OBSERVED requires an observation timestamp and TTL.
3. PROVEN requires at least one evidence reference and validated validation state.
4. DECLARED must come from a declaration derivation.
5. PROPOSED must come from a proposal derivation.
6. Non-UNKNOWN assertions must cite at least one source.
7. Lineage records retain parent references and transformations.
8. Public fixtures must remain synthetic and contain no machine-local paths, secrets or client data.

## Compatibility rule

Legacy vocabularies such as `declared / observed / inferred / proposed / validated` are normalized as follows:
- declared -> truth_status=DECLARED, derivation=declaration;
- observed -> truth_status=OBSERVED, derivation=direct_observation;
- inferred -> derivation=inference, while truth_status remains one of PROVEN/OBSERVED/DECLARED/PROPOSED/FAILED/UNKNOWN depending on evidence;
- proposed -> truth_status=PROPOSED, derivation=proposal;
- validated -> validation.status=validated; it is not a truth status.

## Gate

A01 is ready for review when schema validation tests pass on positive fixtures and reject negative fixtures for each invariant.
