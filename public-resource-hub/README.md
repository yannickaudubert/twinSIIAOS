# AgorIA · SIIAOS Resource Radar

Public demo of a local-first resource aggregator for the AgorIA / SIIAOS digital commons.

## What the demo shows

- Curated catalog of AI hubs, datasets, scientific repositories, creative model markets, launchers, runtimes and orchestration tools.
- Authority / volume / ownership / dependency / local-readiness classification.
- Hyperveille pipeline from external signal to governed local resource.
- Agent roles: Scout, Classifier, License, Security, Benchmark, Architect, Integrator, Archivist.
- Dependency map showing that upstream websites are treated as replaceable sources, not as the local system of record.

## Run locally

No build step and no dependencies are required.

```bash
python -m http.server 8080
```

Then open `http://localhost:8080`.

## Deploy on Vercel

Import the GitHub repository and set the project Root Directory to `public-resource-hub`.
Framework preset: `Other`.
Build command: none.
Output directory: `.`.

## Demo boundary

The current catalog is curated static demo data. Production ingestion should use source adapters, provenance, license/security checks, deduplication, benchmarking and a governed local registry before any resource is admitted into a user's SIIAOS.
