# SIIAOS canonical directives

These directives are the short, stable rules that constrain implementation across Front A, Front B and Front C.

They do not replace detailed schemas, ADRs, runbooks or project plans. They exist to stop historical drift from silently re-entering the system.

## Active directives

1. [DIRECTIVE-0001 — Operating doctrine](./DIRECTIVE-0001-OPERATING-DOCTRINE.md)
2. [DIRECTIVE-0002 — Cabinet personae and interface contract](./DIRECTIVE-0002-CABINET-PERSONAE-INTERFACES.md)
3. [DIRECTIVE-0003 — Tenant membranes and projections](./DIRECTIVE-0003-TENANT-MEMBRANES.md)
4. [DIRECTIVE-0004 — Cross-front golden journey](./DIRECTIVE-0004-CROSS-FRONT-GOLDEN-JOURNEY.md)

## Precedence

When an older document conflicts with these directives, the conflict must be made explicit and resolved through a new ADR or migration record. Historical documents are not deleted merely because they are superseded.

## Evidence rule

A document, branch, mock, simulation, UI or successful CI run is not by itself proof of runtime state. Implementation maturity and truth status remain separate dimensions.
