# Front A Gap Ledger

Updated: 2026-10-04

## A01 — Truth / Lineage

Status: CODED + TESTED LOCALLY

Closed:
- canonical truth status vocabulary defined;
- derivation and validation separated from truth status;
- source lineage contract defined;
- synthetic fixtures added;
- deterministic invariant tests added.

Open:
- integrate A01 contracts into the chosen runtime;
- reconcile any historical contracts that still encode inferred/validated as truth states;
- attach evidence IDs from real runtime observations after a read-only truth snapshot;
- decide whether schema IDs move from placeholder domain to a project-controlled URI;
- add CI execution once CI baseline is admitted.

Observed mismatch:
- historical documentation and public alpha branch used `declared / observed / inferred / proposed / validated` as one flat set;
- convergence pack used `PROVEN / OBSERVED / DECLARED / PROPOSED / FAILED / UNKNOWN`.
Resolution: the convergence vocabulary is canonical for truth status; inferred and validated are moved to derivation and validation dimensions.

## A02-A14

Status: PROPOSED / NOT YET CODED IN THIS BRANCH

No later lot is considered implemented by the presence of A01.
