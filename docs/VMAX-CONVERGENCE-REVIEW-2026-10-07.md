# SIIAOS Vmax — convergence review and finalisation method

Status: ACTIVE CONVERGENCE PLAN / NOT RUNTIME PROOF  
Date: 2026-10-07

## 0. Position

Vmax is not "all features enabled at once".

Vmax means:
- the widest coherent architecture reached by the historical work;
- stable constitutional contracts and authority boundaries;
- replaceable providers/runtimes/harnesses;
- one operational spine from need to governed result;
- local-first operation on SandY;
- multiple UI projections without a second canon;
- evidence, recovery and exit paths proven end to end.

The implementation method is therefore:

`HERITAGE -> INVARIANTS -> CROSS-FRONT CONTRACTS -> VERTICAL SLICE -> ADVERSARIAL TESTS -> OBSERVED SANDY -> PROMOTION`

No front is considered "finished" merely because its isolated schemas, read models or package tests are green.

---

## 1. What the historical work shows we underestimated

### U1 — Integration debt is larger than contract debt

A01-A09, B01-B13, Front C module contracts, Mission Factory and Cognitive Fabric already cover a large part of the conceptual space.

The main remaining risk is not missing one more type. It is failure to connect:
- NeedSpec;
- ContextPack;
- Mission;
- Team;
- workgraph/Spider;
- Capability/Resource planning;
- cognitive strategy;
- tool/agent execution;
- OperationRecord/Evidence;
- HumanGate/Decision;
- Deliverable;
- KnowledgeAdmission/RETEX;
- UI projections.

Rule: prefer integration and migration adapters over another parallel model.

### U2 — Spider is not one router

The Spider concept must compose several independent decisions:

1. semantic/work decomposition;
2. policy/authority;
3. data class and privacy;
4. effect/reversibility;
5. capability availability;
6. resource/host fit;
7. cognitive strategy;
8. verifier requirement;
9. execution route;
10. human gate / abstention.

A single probability threshold cannot represent these dimensions.

### U3 — Team semantics are richer than the current Front B model

Persona, Seat, Role, Team, Council, Agent identity, Capability and Authority are not synonyms.

The historical work requires:
- behavioral/expertise Persona;
- organizational Seat/Role;
- mission-bounded Team;
- deliberative Council/Debate;
- concrete AgentInstance/runtime;
- mandate and ToolGrant from Front A.

The current simple `GovernanceActor { seat, team, councils }` is useful but insufficient as Vmax runtime semantics.

### U4 — Memory promotion is a control-plane problem

Canvas, KnowledgeGraph, RAG, ContextPack and shared team memory must not collapse into one "memory".

Vmax needs explicit layers:

`working/session -> task/team -> mission ContextPack -> project knowledge -> reviewed shared knowledge -> canon`

with:
- source/provenance;
- data class;
- tenant/project/mission scope;
- contradiction state;
- retention;
- admission/rejection;
- reversible derived indexes.

### U5 — Durable execution is not equivalent to database persistence

PostgreSQL, SQLite, Redis and object storage are providers.

The invariant is:
- durable state;
- replay/checkpoint;
- idempotency;
- cancellation;
- compensation;
- restart recovery;
- evidence linkage.

Vmax must define the durable workflow contract first, then bind a provider.

### U6 — Local multi-agent scheduling is a first-class problem

SandY is finite.

A Vmax local runtime must manage:
- model residency/loading;
- VRAM/RAM budgets;
- context budgets;
- parallelism;
- queueing/backpressure;
- tool concurrency;
- cancellation;
- deadlines;
- priority;
- resource evidence.

Multiple named agents do not imply multiple simultaneously loaded models.

### U7 — Client isolation extends beyond `org_id`

Tenant isolation must cover:
- API scope;
- filesystem/artifacts;
- embeddings/indexes;
- model context assembly;
- caches;
- logs/traces;
- exports;
- temporary files;
- agent/tool grants.

A shared Postgres row key alone is not sufficient proof of non-leakage.

### U8 — Recovery/STOP/replay is part of the product, not only engineering

The user must be able to see:
- stopped;
- blocked;
- failed;
- compensating;
- waiting for gate;
- resumable;
- superseded.

Front C must project these states rather than hiding them behind a generic "busy/completed" UI.

### U9 — Golden Mission must become a regression family

One synthetic Golden Mission is useful but insufficient.

Vmax requires at least:
- a local confidential client journey;
- a research/analysis journey with disagreement and evidence;
- an operational production/deliverable journey with HumanGate and recovery.

The same core contracts must survive all three.

### U10 — Transferability was underweighted

SIIAOS is also a consulting/industrialisation system.

Capabilities need:
- deployment profile;
- prerequisites;
- security evidence;
- runbook;
- backup/restore;
- rollback;
- exit/export;
- licence/SBOM;
- training/operator/user guidance;
- SLO/cost model where relevant.

A capability that only works on SandY is not yet a transferable Vmax capability.

---

## 2. What the historical work shows we overinterpreted

### O1 — "Building / floors" is a projection, not core ontology

Keep the spatial metaphor for orientation/pilotage/inspection.

Do not encode every floor/room as canonical domain truth unless a real domain object exists underneath.

### O2 — Prompt Spider is not "every word = one fork"

Fork semantic work objects, constraints, effects and decisions, not tokens.

The useful inheritance is structured branching + explainability + abstention.

### O3 — Confidence is not authority

Confidence may inform routing or verification.

It never overrides:
- Policy;
- Mandate;
- ToolGrant;
- HumanGate;
- sensitive data boundary;
- irreversible effect policy.

### O4 — Provider names are not architecture

LM Studio, Ollama, Hermes, Open WebUI, vLLM, Codex, Claude Code, Qwen Code, Kimi Code, Temporal, Redis, PostgreSQL, etc. remain providers/adapters unless explicitly admitted as a durable dependency.

Freeze contracts; benchmark providers.

### O5 — Fixed team counts are not a constitutional requirement

Historical "18 teams" / "6 agents" ideas are useful target configurations and UX tests, not hard-coded architecture.

TeamCompiler should create the minimum governed team needed for the mission.

### O6 — KnowledgeGraph is not the execution graph

Keep:
- durable semantic KnowledgeGraph;
- live Spider/Execution WorkGraph;
- lineage links between them.

Promote selected outcomes/evidence/decisions, not every retry and transient task.

### O7 — CI green is not machine truth

CI proves code/contracts/tests.

It does not prove:
- SandY current state;
- local runtime binding;
- non-egress;
- recovery after host restart;
- hardware performance;
- actual UI usability.

---

## 3. Front A — next convergence sequence

Front A must now prioritize the contracts required by the other two fronts, not expand horizontally without consumers.

### A10 — Capability / Provider / Execution ABI

Add or reconcile:
- Capability;
- Provider/Engine;
- NativePrimitive;
- CapabilityBinding;
- ExecutionEnvelope;
- CapabilityAvailability/Maturity;
- host/resource evidence refs;
- provider replacement/exit strategy.

Reuse the V100 CapabilityCard/EngineRecord ideas without making `plateforme` canonical.

### A11 — Security / Trust / Secrets / Effect policy

Unify:
- data classes;
- external-effect classes;
- network/egress policy;
- credential refs only;
- sandbox/trust boundary;
- idempotency/compensation requirements;
- HumanGate rules for irreversible effects.

### A12 — Federation / Organization / Team authority boundary

Clarify:
- organization/tenant;
- project/mission;
- Persona/Seat/Role/Team/Council;
- AgentIdentity/AgentInstance;
- mandate/delegation;
- cross-tenant/federated relationships.

### A13 — Compliance profile

Do not hard-code regulations into every runtime object.

Define profiles that can bind:
- retention;
- export;
- data residency;
- required review;
- audit evidence;
- deletion/archival policy.

### A14 — Canon integration + migration

Produce:
- versioned ABI manifest;
- adapters from historical YanIA Mission Factory / Cognitive Fabric;
- migration rules for old OperationRecord/HumanGate types;
- compatibility tests preventing B/C from drifting into local substitute canons.

Front A closure condition:
the Golden Journeys can consume its ABI without importing Front A implementation internals.

---

## 4. Front B — next convergence sequence

Front B should stop adding isolated domain breadth temporarily and turn existing B01-B13 into an executable governed mission brain.

### B-CVG1 — Mission/Spider convergence

Bind WorkGraph nodes to:
- NeedSpec;
- Mission;
- Team;
- task/subtask;
- ContextPack;
- output/artifact;
- canonical evidence/decision refs.

No second mission/task store.

### B-CVG2 — TeamCompiler Vmax

Input:
- mission objective;
- risk/data class;
- required capabilities;
- cognitive strategies;
- human roles;
- resource plan.

Output:
- minimum viable Team;
- roles/seats;
- agent instances/providers;
- verifier/contradictor requirement;
- ToolGrant request;
- resource budget;
- stop conditions.

### B-CVG3 — Composite Spider router

Compose:
`policy -> effect -> resource -> capability -> cognition -> verifier -> execution/human/abstain`

The route result must include reason codes and evidence refs.

### B-CVG4 — Memory / ContextPack discipline

Implement:
- scoped ContextPack builder;
- context budget;
- exact refs;
- spill-to-artifact;
- checkpoint before destructive compaction;
- candidate knowledge admission;
- contradiction preservation;
- no cross-client recall.

### B-CVG5 — durable pipeline engine contract

Support at least:
- serial;
- parallel;
- join;
- loop with bounds;
- gate;
- retry policy;
- checkpoint;
- idempotency key;
- cancellation;
- compensation;
- resume.

Do not choose a heavyweight workflow provider before the contract and tests require it.

### B-CVG6 — Experiment / capability admission loop

Upgrade simplistic Radar evidence-count logic into:

`Radar -> ExperimentContract -> measured result -> evidence -> human/governed admission -> Capability maturity change`

### B-CVG7 — Impact / RETEX

Separate:
- observed metric;
- attribution hypothesis;
- cost;
- time saved;
- risk reduction;
- quality;
- user/adoption/wellbeing;
- confidence/limits.

RETEX creates candidates/changesets; it never rewrites historical truth.

---

## 5. Front C — next convergence sequence

Front C should now become the visual proof that the architecture is understandable and controllable.

### C-CVG1 — Hall attention model

Hall is not a dashboard dump.

Show only:
- what changed;
- what is blocked;
- what needs human attention;
- what is risky;
- what completed;
- where evidence is missing;
- where a mission can resume.

### C-CVG2 — Mission Workbench as the primary operational surface

Must show:
- Need;
- objective/success criteria;
- ContextPack;
- Team;
- Spider graph;
- current lifecycle state;
- resource/local-only state;
- evidence coverage;
- gates;
- artifacts;
- STOP/resume/retry;
- WHY.

### C-CVG3 — Spider Canvas projections

Project the same graph into:
- project view;
- team view;
- task view;
- debate/council view;
- decision view.

Portal nodes represent cross-scope dependencies.

No copied task identity.

### C-CVG4 — WHY / Evidence / Disagreement interaction

For a node/edge:
- observation;
- applied rule/policy;
- evidence;
- uncertainty;
- disagreement;
- selected strategy;
- route;
- effect class;
- authority/gate;
- result.

No raw hidden chain-of-thought required.

### C-CVG5 — Decision Room

Show:
- alternatives;
- consequences/blast radius;
- evidence for/against;
- UNKNOWN;
- reversible/irreversible boundary;
- mandate;
- HumanGate;
- amendment/reject/defer.

### C-CVG6 — Recovery UX

A failed/stopped mission must remain operable:
- inspect last checkpoint;
- see failed operation/evidence;
- retry safe stage;
- compensate;
- amend plan;
- resume;
- close with RETEX.

### C-CVG7 — density and audience

Preserve:
- simple;
- standard;
- expert;

and historical:
- Orientation;
- Pilotage;
- Inspection.

Different density, same truth.

---

## 6. Cross-front integration spine

The Vmax reference journey is:

`NeedSpec`
-> `ContextPack`
-> `Mission`
-> `Capability/Resource Plan`
-> `TeamCompiler`
-> `Spider WorkGraph`
-> `Cognitive/Execution Routes`
-> `Agent/Tool/Human operations`
-> `OperationRecord + Evidence`
-> `Verification/Disagreement`
-> `HumanGate when required`
-> `Decision/Record`
-> `Deliverable`
-> `KnowledgeAdmission`
-> `Impact/RETEX`
-> `Capability/Method changeset candidate`

Front ownership:

- **A**: authority, canon, evidence contracts, policy, security, decision/admission.
- **B**: derived reasoning, mission decomposition, team/work planning, methods, production, RETEX.
- **C**: projection, interaction, explanation, review, control.

---

## 7. Test strategy — Vmax

### Level T0 — schema/invariant

Pure deterministic contracts.

### T1 — package/unit

Front-local functions and state machines.

### T2 — cross-front contract tests

ABI compatibility, migration fixtures, authority boundaries.

### T3 — adversarial/FakeWorld

At minimum:
- false consensus;
- memory poisoning;
- bad simulator;
- irreversible action;
- prompt/tool injection;
- stale host truth;
- cross-tenant reference;
- missing evidence;
- forged HumanGate ref;
- hidden remote fallback;
- duplicate/idempotent action;
- retry after partial failure;
- cyclic Spider dependency.

### T4 — persistence/recovery

Restart process/container and prove:
- mission recovery;
- workgraph identity;
- checkpoints;
- gates;
- operation history;
- no duplicated effect.

### T5 — local integration

Real local providers, model endpoints, tools and stores.

### T6 — UI E2E

Playwright/visual/user journeys:
- orientation;
- pilotage;
- inspection;
- STOP/resume;
- WHY;
- cross-team portal;
- Decision Room;
- client projection.

### T7 — SandY observed

Date-stamped:
- hardware/resources;
- Windows/WSL/Docker;
- local models/runtimes;
- ports/binds;
- non-egress;
- restart/recovery;
- resource pressure;
- multi-agent scheduling;
- backup/restore.

### T8 — three Golden Journeys

1. **Confidential local client dossier**
   - no egress;
   - tenant isolation;
   - research/docs;
   - multi-step mission;
   - evidence;
   - deliverable;
   - restart/resume.

2. **Contested research/innovation decision**
   - competing hypotheses;
   - adversarial verification;
   - UNKNOWN/disagreement;
   - experiment/simulation fidelity;
   - HumanGate decision.

3. **Production/transfer journey**
   - governed artifact production;
   - approval/publication/export boundary;
   - ClientTransferPack;
   - rollback/exit;
   - RETEX.

---

## 8. Vmax closure gates

Vmax-at-date is accepted only if:

- Front A ABI required by B/C is versioned and migration-tested;
- one Mission/Spider runtime exists, not parallel mission systems;
- TeamCompiler is provider-neutral and authority-bounded;
- memory/context promotion boundaries are tested;
- local-only sensitive route is fail-closed;
- durable restart/resume and idempotency are proven;
- UI exposes STOP, WHY, evidence, unknowns and HumanGate;
- three Golden Journeys pass;
- one Golden Journey is observed on SandY with no-egress evidence;
- capability/provider replacement is demonstrated at least once;
- backup/restore and export/exit are tested;
- no Vercel/cloud service is required for nominal local operation;
- no UI/provider/runtime is treated as canonical authority;
- the remaining gaps are explicitly classified rather than hidden.

---

## 9. Immediate implementation order

1. **Front A:** implement/reconcile A10-A11 first because B/C now need capability/effect/security ABI.
2. **Cross-front:** adapt Mission Factory + Cognitive Fabric into the current PR lineage instead of reimplementing them.
3. **Front B:** bind Spider to Mission/ContextPack/Team and compose Resource Steward + Cognitive Router + Execution Policy + Verification.
4. **Front C:** render the real unified workgraph in Mission Workbench before adding decorative Building complexity.
5. **Runtime:** add durable checkpoint/replay/idempotency around that vertical slice.
6. **Testing:** expand FakeWorld and cross-tenant/non-egress suites before adding autonomy.
7. **SandY:** run the resulting vertical slice as drift/conformance proof against the known baseline.
8. **Only then:** widen to more teams, floors, providers, advanced serving and self-improvement loops.

This order maximizes architectural learning per change and minimizes duplicate cores/models.
