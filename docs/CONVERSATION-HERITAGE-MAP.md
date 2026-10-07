# Conversation Heritage Map — SIIAOS

Status: ACTIVE HERITAGE REFERENCE  
Updated: 2026-10-07

## Purpose

This document preserves architectural intent recovered from the historical SIIAOS conversations so that Front A, B and C do not rediscover or contradict prior work.

It is a **heritage reference**, not runtime proof. Conversation history can establish prior intent, constraints, rejected paths and design lineage. It cannot by itself establish current machine state, deployed state or observed runtime behavior.

When this document conflicts with a newer canonical directive, ADR, schema or observed machine truth, the newer authoritative artifact wins and the conflict must remain explicit.

## 1. Stable invariants recovered across the historical work

1. **One canon, many projections.** Interfaces, canvases, graphs, twins, dashboards, agent rooms and client views project state; they do not become a second authority.
2. **Human authority is distinct from technical capability.** Identity, expertise, role, model confidence and tool access do not imply authority.
3. **Unknown remains unknown.** Absence of evidence is never silently converted into false, success or confidence.
4. **Consensus is not proof.** Multi-agent agreement may be useful, but evidence and authority remain separate.
5. **Simulation is not reality.** Dry-run, FakeWorld, mocks, CI and synthetic tests never become observed runtime state.
6. **Local-first is nominal, not degraded mode.** SandY must be capable of running the useful core without a mandatory remote provider.
7. **No implicit cloud fallback.** Confidential/restricted or local-only work fails closed unless an explicit governed external capability exists.
8. **Providers are replaceable operators.** Hermes, Open WebUI, OpenHands, Codex, Claude Code, Qwen Code, Kimi Code, LM Studio, Ollama and similar systems are providers/operators, never the canon.
9. **REUSE -> COMPOSE -> ADAPT -> BUILD.** Existing working assets and upstream components are audited before new custom code is introduced.
10. **Every sensitive action has an authority path.** Policy, mandate, ToolGrant, HumanGate, STOP/resume and rollback/recovery remain visible.
11. **Evidence is addressable.** Critical outputs and decisions must preserve source, provenance, evidence and operation lineage.
12. **Memory is layered.** Working/session memory, mission memory, derived indexes/graphs and durable admitted knowledge are distinct.
13. **Agent output is a proposal until admitted.** Derived knowledge, recommendations, twins, plans and RETEX do not silently mutate durable knowledge.
14. **Clients/tenants remain isolated.** Shared methods can converge; private client data and context do not leak into common memory.
15. **The same core supports personal, cabinet and client scopes through policies, not separate cores.**
16. **The UI must expose disagreement and causality.** Users can inspect why a route, task, team, tool or decision exists.
17. **No fake activity.** Building/City/agent-office views must reflect real state, not decorative autonomous behavior.
18. **GitHub is the engineering integration authority.** Code, branches, PRs, lint, tests, CI and integration proof live there; Vercel is not a default proof path.
19. **Maturity and truth are separate.** DESIGNED/CODED/TESTED/DEPLOYED/OBSERVED/PROVEN must not be collapsed.
20. **A failed operation is first-class state.** Failure, cancellation, retry, compensation, rollback and incomplete work must remain representable.

## 2. Design lineage recovered from prior conversations

### 2.1 Early local sovereign workspace

The early architecture combined local LLM runtimes with Open WebUI, Obsidian/Markdown, AppFlowy, AnythingLLM/RAG, n8n, Grist/NocoDB, Docker and Git/GitOps.

Useful pattern retained:
- LLM/runtime separated from memory and workspace;
- RAG/indexes are derived;
- workflows orchestrate capabilities;
- human workspace and machine execution remain separable.

Rejected evolution:
- no external UI or RAG product is allowed to become the SIIAOS authority.

### 2.2 Vault / memory / agent separation

Historical work repeatedly converged on:
- Obsidian/Markdown/Vault as durable human-readable knowledge;
- Git as version/provenance memory;
- RAG/vector/graph as rebuildable derived access layers;
- agents as operators above the memory layer;
- review queues and staging before promotion;
- ContextPack as a bounded mission projection.

Memory boundary:
`session/cache -> mission memory -> reviewed/admitted knowledge -> derived RAG/graph projections`

The old rule remains valid: a full Vault, secret set or unrelated client corpus is never injected into an agent by default.

### 2.3 Hermes and harness lineage

Hermes was repeatedly positioned as an agent runtime/provider with sessions, skills, MCP/tool access, teams/rooms and local execution. Similar harnesses studied later include OpenHands, OpenClaw, Goose, Agent Zero, Codex, Kimi Code, Qwen Code, Claude Code, PydanticAI and Microsoft Agent Framework.

Retained:
- provider-neutral agent contract;
- bounded tools;
- observable sessions/runs;
- role/team composition;
- replayable evidence.

Rejected:
- provider-specific identity or memory as canonical identity/memory;
- harness consensus as proof;
- harness autonomy bypassing SIIAOS policy.

### 2.4 Building / City / Hall lineage

The building metaphor predates the current Front C work and is not decorative.

Recovered navigation and control expectations include:
- Hall as attention/entry surface;
- Building/City/Floors for scoped operational navigation;
- Mission Workbench;
- Team/employee workspaces;
- Decision Room;
- Research Studio;
- Deliverable Studio;
- Knowledge;
- Radar;
- Infrastructure / Platform / Fleet;
- Admin / Archive;
- global STOP and clear identity/context selector.

The UI must support observing, questioning, orienting, debating, interrupting, reassigning, annotating, reviewing, arbitrating, validating, rejecting and promoting work.

The historical UX depth model remains:
`Orientation -> Pilotage -> Inspection`

### 2.5 Mission Factory lineage

The most stable operational spine recovered from the prior prototypes is:

`NeedSpec -> ContextPack -> Mission -> Team -> operation/tool/agent work -> Evidence/OperationRecord -> HumanGate when required -> Deliverable/Decision -> RETEX`

Retained assets include:
- mission lifecycle/state machine;
- durable checkpoints;
- dry-run;
- STOP/resume;
- explicit failure;
- bounded team compilation;
- knowledge admission;
- Golden Mission / Golden Journey regression use.

### 2.6 Cognitive Fabric / Capability Fabric lineage

Recovered reusable concepts:
- Capability Registry;
- Capability Router;
- Resource Steward;
- ExecutionEnvelope;
- StrategySpec;
- model/provider separation;
- local resource fit;
- deterministic-first routing;
- adversarial verification;
- simulation with fidelity evidence;
- fail-closed external routing;
- capability/provider/runtime/host as distinct objects.

Rejected shortcuts:
- choosing a provider before a capability;
- treating model confidence as authority;
- pretending an unavailable local resource exists;
- treating simulated success as deployed success.

### 2.7 Evidence / replay / truth lineage

Historical work on Truth Gates, Evidence Ledger, MachineTruth/RepoTruth, OperationRecord, replay/Rewind and immutable snapshots converged on:
- source/lineage separate from validation;
- observed state separate from desired state;
- immutable evidence or digests for critical operations;
- snapshots compared over time;
- replayable execution history;
- failure and rollback represented explicitly.

This lineage is now carried by Front A contracts and must not be recreated independently in B or C.

### 2.8 Resource Radar / open-source admission lineage

The Radar work established a broader architectural method:

`discover -> qualify -> compare -> test -> experiment -> admit/reject -> monitor -> RETEX`

Resources are classified by capability, evidence, license, deployability, local fit, security, maintenance and exit strategy.

Historical rule retained:
- no upstream repository becomes SIIAOS merely because it is technically interesting;
- useful patterns are pinned and mapped to existing SIIAOS surfaces before adoption.

### 2.9 Territorial / citizen governance lineage

Prior territorial and citizen-governance work contributes non-technical invariants that must constrain SIIAOS:

- legitimacy != technical authority;
- participation != co-decision;
- contribution != ownership;
- expertise != democratic legitimacy;
- public authority != omniscience;
- subsidiarity and polycentric governance;
- durable disagreement must remain representable;
- accountability must expose status, reason, responsible actor and evidence;
- contribution and common assets require traceability and fair governance;
- interfaces must make complexity understandable without erasing it.

HumanGate therefore supports more than one pattern:
- prior approval;
- co-planning;
- active monitoring;
- posterior review;
- STOP/resume;
- ratification/rejection/defer/out-of-scope states.

### 2.10 SandY / ARAGORN lineage and supersession

Historical machine roles changed during exploration and must not be flattened into one timeless statement.

Current retained direction from the latest conversations:
- **SandY** is the primary local-first compute/IA/SI node for the SIIAOS;
- **ARAGORN** is a physical ASUS TUF machine and remains secondary/canary/rollback/experimentation, not a software abstraction and not a required runtime dependency;
- machine truth is always date-stamped;
- a previous observed or declared state is a baseline, not proof of current state;
- a fresh probe measures drift rather than rediscovering the architecture.

## 3. Agent / Team / memory requirements to preserve

Teams are not only collections of prompts.

A team may include roles such as:
- coordinator/lead;
- researcher;
- analyst;
- producer/operator;
- contradictor/adversarial reviewer;
- evidence reviewer/guardian.

Earlier Persona/Seat/Team/Council work established that:
- persona describes behavioral/expertise configuration;
- seat/role describes organizational function;
- team describes mission composition;
- council/debate describes a governed deliberative surface;
- identity and authority remain distinct from all four.

Shared-memory rule:
- mission/team agents receive a bounded ContextPack;
- work products stay in mission/work memory until reviewed;
- accepted knowledge is promoted explicitly;
- disagreements and rejected proposals remain traceable;
- RETEX proposes future changes but does not rewrite history.

## 4. Spider/Canvas implications

The 2026-10-07 Spider work is a continuation of the older Building, Mission Factory, Cognitive Fabric, Team and graph work.

It must therefore preserve:
- one operational graph, many board projections;
- stable object identity across project/team/task/floor views;
- typed edges and explicit dependency;
- recursive decomposition without authority escalation;
- structured WHY traces;
- visible UNKNOWN, blocked, contested and abstained states;
- cross-team portals rather than duplicated task copies;
- HumanGate precedence over confidence;
- promotion from execution graph into durable knowledge only through governed admission.

Canvas = representation.  
Spider = decomposition/routing/orchestration.  
Agents = execution.  
Front A = authority/evidence/canon.  
Front B = derived analysis/work planning/production.  
Front C = interaction/projection.

## 5. Reuse / adapt / reject map

### KEEP / COMPOSE
- Mission Factory spine and state machine;
- ContextPack;
- Capability Registry;
- Evidence/OperationRecord lineage;
- HumanGate/STOP/resume;
- Golden Mission / Golden Journey;
- Vault/Markdown/Git durable knowledge pattern;
- Building/Hall/Mission/Decision/Research/Deliverable UX surfaces;
- Resource Radar qualification method;
- Team/Seat/Persona/Council model;
- deterministic workflows for bounded operations;
- local runtimes and provider-neutral interfaces.

### ADAPT
- Hermes teams/rooms/skills into governed provider contracts;
- Open WebUI as transitional or optional surface only;
- AppFlowy/Obsidian/Grist/Paperless/office tools as capability providers/projections;
- n8n/Windmill/Temporal according to workload durability rather than as a second control plane;
- Graphiti/Cognee/Mem0/vector stores as derived memory providers;
- older cockpits/Building prototypes as UX heritage, not runtime authority;
- historical YanIA contracts to the Front A ABI.

### REJECT AS CORE
- any provider as source of canonical truth;
- consensus = proof;
- confidence = authorization;
- simulation = observed reality;
- UI state = canonical state;
- memory inside one harness as shared organizational truth;
- silent cloud fallback;
- autonomous external communications without explicit authority;
- duplicate control planes and duplicate canons;
- decorative agent activity not backed by runtime state.

## 6. Regression obligations for the three fronts

### Front A
Must test:
- identity != authority;
- policy/HumanGate precedence;
- evidence and lineage;
- unknown/failed states;
- data boundaries;
- immutable record/decision linkage;
- admission and supersession rather than history rewrite.

### Front B
Must test:
- derived twin/plan/recommendation remains derived;
- team/role composition is mission-bounded;
- Spider recursion does not expand authority;
- deterministic/local-agent/abstain routing;
- contradiction preservation;
- ContextPack and memory boundaries;
- RETEX is proposal until admission.

### Front C
Must test:
- every board is a projection;
- the same object keeps one identity across views;
- moving/editing a visual node cannot mint canon;
- WHY exposes evidence/rules/reason codes without requiring hidden chain-of-thought;
- HumanGate and STOP are visible and actionable;
- unknown/blocked/contested states are not visually normalized away;
- simple/standard/expert depth preserves the same underlying truth.

## 7. Engineering doctrine

The historical work should now be treated as a regression corpus.

Every significant new Front A/B/C capability should answer four questions:

1. Which prior lineage does this reuse?
2. Which invariant does it preserve?
3. Which rejected path could it accidentally reintroduce?
4. What test proves the invariant without overstating runtime truth?

This is the default rule for continuing SIIAOS convergence.
