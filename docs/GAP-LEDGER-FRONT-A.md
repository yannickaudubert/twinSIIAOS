# Front A Gap Ledger

Updated: 2026-10-05

## A01 — Truth / Lineage

Status: CODED; invariant tests present; prior local execution claim withdrawn until a fresh reproducible run exists.

Closed:
- canonical truth status vocabulary defined;
- derivation and validation separated from truth status;
- source lineage contract defined;
- synthetic fixtures added;
- deterministic invariant tests added.

Open:
- execute tests in CI or an environment able to materialize the branch;
- integrate A01 contracts into the chosen runtime;
- reconcile historical contracts that still encode inferred/validated as truth states;
- attach evidence IDs from real runtime observations after a read-only truth snapshot;
- replace placeholder schema IDs with a project-controlled URI if retained.

Observed mismatch:
- historical documentation and public alpha branch used `declared / observed / inferred / proposed / validated` as one flat set;
- convergence pack used `PROVEN / OBSERVED / DECLARED / PROPOSED / FAILED / UNKNOWN`.
Resolution: the convergence vocabulary is canonical for truth status; inferred and validated are derivation and validation dimensions.

## A02 — Core ontology

Status: CODED / NOT YET EXECUTION-PROVEN

Contract:
- `contracts/core-ontology.schema.json`

Scope:
- Principal -> Tenant -> Mission -> Resource;
- canonical ownership and tenant binding;
- truth and lineage references on core objects.

## A03 — Identity model

Status: CODED / NOT YET EXECUTION-PROVEN

Contract:
- `contracts/identity.schema.json`

Scope:
- human / organization / agent / service / workload / device identities;
- credential references only;
- identity distinct from authority.

## A04 — Authority / Mandate / Delegation

Status: CODED / NOT YET EXECUTION-PROVEN

Contract:
- `contracts/authority.schema.json`

Scope:
- explicit mandate;
- bounded, expirable and revocable delegation;
- non-delegable delegation by default in this first contract.

## A05 — Policy / ToolGrant / HumanGate

Status: CODED / NOT YET EXECUTION-PROVEN

Contract:
- `contracts/policy-toolgrant-humangate.schema.json`

Scope:
- policy decision;
- mission-bound least-privilege ToolGrant;
- explicit HumanGate decision with digest.

## A06 — Data / Privacy / Tenant boundaries

Status: CODED / NOT YET EXECUTION-PROVEN

Contract:
- `contracts/data-privacy-boundary.schema.json`

Scope:
- PUBLIC / INTERNAL / CONFIDENTIAL / RESTRICTED;
- explicit purpose, retention, remote execution and export policy;
- fail-closed restrictions for confidential/restricted data.

## A07 — Document / Record lifecycle

Status: CODED / NOT YET EXECUTION-PROVEN

Contract:
- `contracts/document-record.schema.json`

Scope:
- mutable Document vs immutable Record;
- explicit capture, digest, evidence, lineage and supersession.

## A08 — Evidence / OperationRecord

Status: CODED / EXECUTION PROOF PENDING CI

Contract:
- `contracts/evidence-operation-record.schema.json`

Scope:
- immutable evidence objects tied to tenant/mission context;
- explicit source and claim references plus digest;
- OperationRecord binds actor identity, mandate, action, status, inputs/outputs and evidence;
- succeeded/failed operations require evidence.

## A09 — Decision / ADR / Case

Status: CODED / EXECUTION PROOF PENDING CI

Contract:
- `contracts/decision-adr-case.schema.json`

Scope:
- governed Decision separated from proposal/recommendation;
- approved/rejected decisions require explicit human gate, mandate and evidence;
- ADR records architectural consequences without replacing the Decision;
- Case groups evidence and decisions while preserving tenant/mission scope.

Verification:
- deterministic A08/A09 tests added in `tests/test_a08_a09_records.py`;
- status remains not execution-proven until the branch CI is green.

## A10-A14

Status: PROPOSED / NOT YET CODED IN THIS BRANCH

Planned sequence:
- A10 Capability / Provider contracts
- A11 Security / Trust / Secrets
- A12 Federation / Organization model
- A13 Regulatory / compliance profiles
- A14 Canon integration + migrations

No later lot is considered implemented by the presence of earlier contracts.
