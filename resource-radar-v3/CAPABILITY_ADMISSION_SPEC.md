# SIIAOS — Capability Admission & Maturity Routing

Status: WORKING SPEC  
Repository: `yannickaudubert/twinSIIAOS`  
Base commit: `72df658435dff1585279dca419f5fc094dc307a3`  
Scope: extension of `public-resource-hub` and `resource-radar-v3`.

## 1. Purpose

Evolve the Resource Radar from a catalog/discovery surface into a governed capability admission layer.

The target chain is:

```
signal
  -> canonical resource
  -> provenance / licence / security qualification
  -> capability mapping
  -> organisation maturity fit
  -> local feasibility
  -> sandbox experiment
  -> evidence
  -> human review when required
  -> admission / pinning
  -> observation / RETEX
  -> hold / retirement
```

The radar must answer not only "what exists?" but also:

- Which SIIAOS capability does this resource provide?
- Is that capability already available locally?
- For which organisational maturity profile is it suitable?
- What permissions, data access, network egress and compute does it require?
- What evidence is required before use?
- Is it reversible and replaceable?
- Is it a source, a candidate, an admitted dependency, or an observed runtime component?

## 2. Canonical invariants

1. A source is not a system of record.
2. Downloaded does not mean installed.
3. Installed does not mean activated.
4. Activated does not mean tested.
5. Tested does not mean deployed.
6. Deployed does not mean observed healthy.
7. A proposal is never promoted to realised or verified without evidence.
8. Git state does not prove machine/runtime state.
9. Missing evidence is recorded as `UNKNOWN / TO_VERIFY`, never inferred.
10. Corrections and explicit decisions must remain traceable and must not be silently overwritten by newer summaries.
11. External services and vendors are replaceable accelerators; local operation must remain possible for SIIAOS core capabilities.
12. Admission is reversible: every admitted component needs an exit/rollback path.
13. Sensitive mutation requires an explicit HumanGate according to risk and organisational maturity.
14. Resource discovery, download, installation and activation remain distinct operations.

## 3. Objects

The registry uses one common envelope for:

- `source` — external discovery source/hub.
- `project` — open-source or open-weight project.
- `model` — model/checkpoint/runtime-loadable artefact.
- `dataset` — dataset/corpus.
- `skill` — reusable ChatGPT/Codex/Hermes capability package.
- `mcp` — MCP server/client capability.
- `workflow` — n8n or other executable workflow.
- `runtime` — local execution environment/component.
- `service` — deployable service.
- `method` — practice/framework/reference method.

Every object gets a stable `record_id`.

## 4. Capability mapping

A resource is never admitted only because it is popular or technically attractive.

It must map to one or more capability identifiers:

```
resource
 -> capability
 -> treatment / workflow / mission
 -> required organisation context
 -> evidence
```

A candidate should also state whether the capability is:

- `NEW`: no current equivalent known.
- `REPLACE`: proposed replacement.
- `AUGMENT`: complements an existing capability.
- `DUPLICATE`: materially overlaps an admitted capability.
- `EXPERIMENT`: exploration without production commitment.

Before creating or installing a new component, the resolver must search the admitted registry for equivalent capability.

## 5. Organisational maturity vector

Do not collapse maturity into one score. Store dimensions separately.

Initial dimensions:

- `governance`
- `delivery`
- `operations`
- `observability`
- `security`
- `data`
- `ai_usage`
- `automation`
- `open_source`
- `human_control`

Each dimension uses levels 0–4:

- `0 OPPORTUNISTIC`: ad hoc, manual, weak inventory/evidence.
- `1 CONTROLLED`: basic Git, ownership, backups, review, bounded experiments.
- `2 REPEATABLE`: reusable workflows, tests, telemetry, standardised gates.
- `3 PLATFORM`: governed self-service, policy, provenance, shared capability catalog.
- `4 ADAPTIVE`: continuous sensing, measured experiments, automatic reconciliation, upstream/common contribution.

A resource declares `maturity_min` per required dimension rather than one global minimum.

The router must prefer the simplest viable capability for the actual maturity vector.

## 6. Project maturity

Track upstream maturity independently from organisation maturity.

Fields:

- `upstream_stage`: experimental | sandbox | incubating | stable | graduated | archived | unknown
- `upstream_stage_source`
- `release_cadence`
- `last_release_at`
- `last_commit_at`
- `maintainer_diversity`
- `bus_factor_signal`
- `adoption_signal`
- `security_policy_present`
- `responsible_disclosure_present`

No upstream maturity label alone is sufficient for admission.

## 7. Admission lifecycle

Canonical lifecycle:

```
DISCOVERED
 -> CANDIDATE
 -> SCANNED
 -> REVIEWED
 -> EXPERIMENT
 -> ADMITTED
 -> PINNED
 -> OBSERVED
```

Side states:

- `BLOCKED`
- `HOLD`
- `REJECTED`
- `RETIRED`
- `UNKNOWN`

Rules:

- `SCANNED` requires provenance, licence and security checks.
- `EXPERIMENT` requires an explicit experiment contract.
- `ADMITTED` requires evidence from the experiment or an explicitly documented exception.
- `PINNED` requires immutable version/commit/hash.
- `OBSERVED` requires runtime evidence, not repository evidence.
- `HOLD` prevents new activation while retaining provenance/history.
- `RETIRED` must preserve replacement and rollback history.

## 8. Risk and permissions

Each record declares:

### Execution

- scripts executed
- package managers
- container requirements
- privilege level
- filesystem scopes
- process execution
- shell access
- GPU/device access

### Network

- outbound network required
- allowed destinations
- inbound listeners
- localhost-only capability
- telemetry/update checks

### Data

- personal data
- confidential data
- customer data
- model prompts/completions
- secrets/credentials
- persistence location
- retention

### Supply chain

- source repository
- release artefacts
- signatures/attestations
- hashes
- dependency lock state
- extension/plugin ecosystem
- dynamic remote code loading

Risk classes:

- `R0`: read-only/reference.
- `R1`: local bounded execution, no sensitive mutation.
- `R2`: filesystem/network mutation with bounded permissions.
- `R3`: credentials, external writes, sensitive data or infrastructure mutation.
- `R4`: privileged/system-wide or high-impact autonomous mutation.

R3/R4 always require explicit HumanGate for first admission and policy-defined review for subsequent use.

## 9. Local feasibility and frugality

The record must capture:

- CPU requirement
- RAM requirement
- GPU/VRAM requirement
- disk footprint
- expected persistent services
- idle cost
- external API dependency
- licence/subscription cost
- local-only capability
- degraded-mode capability
- offline capability

The resolver should prefer existing local capacity and already-admitted components before paid or structurally external dependencies.

## 10. Experiment contract

Every non-trivial candidate admitted through experimentation gets:

- `hypothesis`
- `baseline`
- `success_metrics`
- `failure_conditions`
- `resource_budget`
- `data_scope`
- `allowed_permissions`
- `test_environment`
- `rollback`
- `evidence_outputs`
- `review_required`

The experiment must be small enough to reverse cleanly.

## 11. Evidence

Evidence records are append-only references.

Minimum fields:

- `evidence_id`
- `kind`
- `source`
- `timestamp`
- `subject`
- `claim`
- `status`: observed | realised | verified | blocked | unknown
- `artifact_hash` when applicable
- `environment`
- `notes`

Claims must never be promoted only from assistant summaries.

## 12. Skill registry overlay

Skills use the same admission model and add:

- `skill_name`
- `trigger_description`
- `source_type`: local | upstream | adapted
- `source_repo`
- `source_commit`
- `package_hash`
- `connectors`
- `tools`
- `scripts`
- `permissions`
- `network`
- `data_scope`
- `conflicts_with`
- `depends_on`
- `tests`
- `last_verified_at`
- `trigger_tests`
- `non_regression_tests`

The target library may contain 75–120+ skills, but routing should normally select one primary skill and only the minimum auxiliary set.

The number of installed skills is not a maturity metric. Coverage, reliability, routing accuracy, proof and non-regression are.

## 13. Initial skill families

The registry must support at least these families:

1. Context archaeology / chantier recovery
2. Authority, correction and anti-regression
3. Truth-state / evidence / verification-before-completion
4. Convergence and knowledge capitalisation
5. Research and source qualification
6. Open-source radar and technology qualification
7. Git/GitHub and repository archaeology
8. Software architecture and dependency mapping
9. Systematic debugging
10. Testing / TDD / non-regression
11. Code and differential review
12. Supply-chain / CI/CD / DevSecOps
13. Docker / local runtime / GitOps
14. Observability / OpenTelemetry
15. Local models / model routing / benchmarking
16. MCP admission and permissions
17. n8n design / modularisation / error handling
18. Knowledge graph / Graphiti / Neo4j projections
19. Web / Next.js / Vercel / accessibility / SEO
20. Editorial factory / publishing / social derivation
21. Client SI/AI/data mapping
22. Organisational maturity assessment
23. Transformation roadmap
24. Documentation / DOCX / PDF / slides / spreadsheets
25. Project-specific capability packs

## 14. Resource Radar integration

Current `public-resource-hub/sources.js` is curated static demo data. Preserve it as demonstration input until migration is tested.

Target evolution:

```
sources.js (current demo)
        |
        v
normaliser
        |
        v
registry records
        |
        +--> public catalog projection
        +--> maturity view
        +--> capability graph
        +--> risk/admission view
        +--> local feasibility view
        +--> skill registry view
        +--> experiment queue
```

Do not make the UI data structure the canonical registry schema.

## 15. Minimal implementation sequence

### Gate 0 — preserve current V3
- Snapshot current files and SHA.
- Add validation fixtures before schema migration.
- Keep current Vercel demo operational.

### Gate 1 — schema
- Validate records against `capability-record.schema.json`.
- Introduce a generated registry dataset without removing `sources.js`.

### Gate 2 — compatibility adapter
- Map the existing 41 curated sources to registry records.
- Preserve existing UI fields.
- Flag missing fields as `unknown`, not guessed.

### Gate 3 — maturity routing
- Add maturity-vector input/profile.
- Filter/rank candidates by minimum maturity, risk and local feasibility.
- Never hide rejected/blocked reasoning.

### Gate 4 — admission
- Add lifecycle state and evidence.
- Separate discovery, download, installation and activation.
- Add HumanGate for high-risk transition.

### Gate 5 — skills
- Import/adapt skills only through the same lifecycle.
- Run trigger/non-regression/security tests.
- Pin admitted versions and hashes.

### Gate 6 — continuous innovation
- Periodically re-check upstream freshness and security.
- Compare new candidates to current capabilities.
- Generate experiments instead of automatic replacement.
- Feed RETEX back into capability and maturity records.

## 16. Definition of done for the first implementation

The first implementation is complete only when:

- existing V3 behavior still works;
- all 41 demo sources can be represented without loss;
- unknown values remain explicit;
- one maturity profile changes recommendations deterministically;
- one duplicate capability is detected;
- one R3/R4 candidate is blocked behind a HumanGate;
- one candidate can move CANDIDATE -> EXPERIMENT -> ADMITTED using evidence;
- one admitted record can be put on HOLD and rolled back;
- tests prove the transitions above;
- no claim of deployment is made from Git state alone.
