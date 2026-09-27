# SIIAOS Skill Registry

The skill registry is a governed projection of capabilities, not a folder-counting exercise.

## Three distinct layers

1. **Inventory** — a skill is observable in one environment.
2. **Candidate** — a skill or upstream source is worth evaluating.
3. **Admitted capability** — the candidate passed the shared Capability Core lifecycle with evidence.

Never collapse these layers.

## Target coverage

`families.json` defines an initial target of 96 capability slots across 12 families. This is a planning target, not a requirement to install 96 packages.

A single high-quality skill may satisfy several slots. Several environment-specific skills may implement the same capability.

## Environment truth

`current-chatgpt.inventory.json` records skills observed in the current ChatGPT environment only.

It does **not** prove presence on:

- SandY;
- ARAGORN;
- Hermes;
- n8n;
- local model runtimes;
- a client SI.

Those environments need their own observed inventories.

## Community candidates

`community-candidates.seed.json` is discovery input only. Candidates enter the same lifecycle as any other resource:

```
DISCOVERED -> CANDIDATE -> SCANNED -> REVIEWED -> EXPERIMENT -> ADMITTED -> PINNED -> OBSERVED
```

No upstream README, popularity metric or previous assistant recommendation skips this lifecycle.

## Next implementation

1. Add an environment inventory collector.
2. Convert selected inventory/candidate entries into canonical capability records.
3. Add trigger tests and non-regression tests per skill.
4. Add conflict/dependency detection.
5. Add security/provenance scanning.
6. Build maturity-aware routing over admitted skills.
