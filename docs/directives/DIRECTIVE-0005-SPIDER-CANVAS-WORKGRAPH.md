# DIRECTIVE-0005 — Spider workgraph and canvas projections

Status: ACTIVE

## Purpose

Project, team and task whiteboards may expose a living work graph ("Spider"), but the graph is an operational projection, not a second source of canonical truth.

The objective is to let local agent teams decompose work, route bounded decisions, expose dependencies and explain why a branch exists while preserving Front A authority, evidence and HumanGate invariants.

## Canonical boundary

- Front A remains authoritative for truth, lineage, evidence, mandate, policy, HumanGate, Decision, ADR, Case and immutable records.
- Spider nodes and canvas layout are derived/runtime objects unless an existing Front A contract explicitly admits them.
- A canvas position, colour, edge, agent opinion, confidence score or runtime state never becomes canon by itself.
- Front B may derive plans, tasks, team assignments, debates and candidate routes.
- Front C may project those objects into project/team/task boards.
- Promotion into canon only occurs through the governed cross-front path and existing Front A gates.

## One graph, many boards

The same work object must not be copied into separate team/project/floor boards.

Boards are scoped projections of one work graph:

`mission -> project -> team -> role/agent -> task -> decision/gate -> evidence/artifact`

A board may show a partial view and portal nodes for relations that cross its scope.

## Typed workgraph

The runtime graph should use typed nodes such as:

- objective;
- project;
- team;
- role;
- agent;
- task/subtask;
- decision candidate;
- debate;
- tool;
- evidence;
- artifact;
- gate/approval.

Edges must be typed, for example:

- `decomposes_into`;
- `assigned_to`;
- `requires`;
- `blocks`;
- `produces`;
- `uses`;
- `references`;
- `supports`;
- `contradicts`;
- `escalates_to`;
- `requires_approval`;
- `derived_from`.

## Routing precedence

A confidence score never grants authority.

Routing order is:

1. explicit policy / non-delegable HumanGate;
2. fail-closed blocked or unknown condition;
3. deterministic local capability when a bounded rule is satisfied;
4. local agent/reasoner for remaining ambiguity;
5. abstention/escalation when the required capability or evidence is unavailable.

No remote provider is an implicit fallback for local-only work.

Thresholds are policy inputs, not universal truth values.

## Explainability contract

The Spider must expose a structured decision trace:

`observation -> rule/policy -> evidence refs -> route -> outcome`

The system must not require storage or display of private chain-of-thought. Human-readable reason codes, evidence links, applied rules, disagreement state and resulting actions are sufficient and auditable.

UNKNOWN, contradiction, abstention and unresolved debate must remain visible rather than being collapsed into a confident answer.

## Recursive decomposition

A mission may fork into teams; a team may fork into tasks; a task may fork into subtasks or a debate. Recursion is allowed only while:

- tenant/mission scope remains explicit;
- parentage is preserved;
- cycles are detectable;
- authority does not expand through recursion;
- child work cannot silently mint canonical records;
- stop/cancel/rollback remains representable.

## Local-first requirement

The Spider runtime, its boards, its event stream and its durable execution trace must support local-first operation.

Network/cloud capabilities, if any, are explicit governed capabilities. They are never required to explain or render a local mission.

## Acceptance checks

A Spider/Canvas slice is not accepted unless:

- one work object has one stable identity across all boards;
- project/team/task views are projections, not copies;
- cross-team dependencies remain navigable;
- HumanGate wins over any model confidence;
- confidence is not presented as authority or proof;
- deterministic routes and agent routes are distinguishable;
- a WHY view can show rule/evidence/route without raw hidden reasoning;
- UNKNOWN/blocked/contested states survive the UI;
- Front C cannot mint Decision/Record objects by moving or editing a node;
- Front B cannot silently promote a derived plan to Front A canon;
- the same graph can be rendered without a remote provider.
