# Front A — A02 to A05

Status: CODED; schema-level review pending CI/runtime execution.

## A02 — Core ontology

Canonical scope chain:

`Principal -> Tenant -> Mission -> Resource`

The ontology is deliberately small. Authority, identity, policy, grants and evidence are references or later contracts, not extra ownership hierarchies.

Key invariants:
- every Tenant belongs to exactly one Principal;
- every Mission belongs to exactly one Tenant;
- every Resource belongs to exactly one Tenant and may optionally be mission-bound;
- truth and lineage references remain attached to canonical objects;
- interfaces and projections never become owners of canonical objects.

## A03 — Identity model

Identity answers “who/what is this subject?” It does not answer “what may it do?”.

Key invariants:
- subject types are human, organization, agent, service, workload or device;
- credentials are references only; secret values are forbidden;
- verified/strong assurance requires truth references;
- suspension/revocation changes usability but does not erase lineage.

## A04 — Authority / Mandate / Delegation

Authority comes from an explicit Mandate. Delegation is derived from an existing mandate and is never implicitly recursive.

Key invariants:
- authority is tenant-scoped and action-scoped;
- delegation identifies from/to identities;
- delegation is non-delegable by default and in this contract fixed to `non_delegable=true`;
- revocation/expiry must be representable explicitly;
- identity alone never grants authority.

## A05 — Policy / ToolGrant / HumanGate

A policy decision constrains action; a ToolGrant is the concrete least-privilege capability to use a tool in one mission; a HumanGate records a non-delegable human decision.

Key invariants:
- ToolGrant always binds Identity + Mandate + Tenant + Mission + Tool + Actions;
- policy decision is explicit: allow / deny / require_human_gate;
- HumanGate stores a decision digest, not an informal “approved” flag;
- grants are revocable and expirable;
- no grant exists outside a mission.

## Verification state

A01 remains the only lot with previously added invariant tests in the branch. A02-A05 schemas are coded; deterministic tests must be executed in CI or an environment able to materialize the branch. No claim of TESTED/PROVEN is made yet.
