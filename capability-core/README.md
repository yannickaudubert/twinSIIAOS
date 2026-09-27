# SIIAOS Capability Core

Portable decision core for capability admission, maturity routing and local-first policy.

## Architectural rule

The core is **not** a feature of the Resource Radar, n8n, ChatGPT, SandY, Vercel, a model runtime, an MCP server or any other surface.

The canonical contract is:

1. JSON data structures;
2. deterministic decision semantics;
3. shared conformance fixtures;
4. versioned protocol envelopes.

Language implementations are replaceable reference engines. Adapters may transport data, but they must not silently change decisions.

## Supported execution shapes

The same contract can be used through:

- Python import;
- Python CLI over stdin/stdout JSON;
- Node/CommonJS import;
- Node CLI over stdin/stdout JSON;
- browser global (`SIIAOSCapabilityCore`);
- n8n Code/Execute Command or later HTTP adapter;
- local AI agents and model runtimes through a tool/MCP wrapper;
- ChatGPT through a skill/connector adapter using the same fields and verdicts;
- arbitrary SI through a future HTTP, message-bus or database adapter.

The default interoperability boundary is **JSON in / JSON out**. This keeps the core usable even where no shared runtime or SDK exists.

## Operations

Protocol version `0.1` supports:

- `assess`: evaluate one candidate against an organisation/profile context;
- `route`: evaluate and order several candidates;
- `transition`: validate an evidence-gated lifecycle transition without performing external mutation.

Example:

```json
{
  "protocol_version": "0.1",
  "operation": "assess",
  "record": {
    "record_id": "project.example",
    "name": "Example",
    "admission_state": "CANDIDATE",
    "risk_class": "R1",
    "maturity_min": {"governance": 1},
    "capabilities": [{"capability_id": "automation.workflow", "relation": "NEW"}],
    "local_feasibility": {"offline_capable": true, "external_api_dependency": false}
  },
  "context": {
    "profile": {"governance": 2},
    "preferences": {"avoidExternalApi": true}
  }
}
```

CLI:

```bash
cat request.json | python3 capability-core/engine.py
cat request.json | node capability-core/engine.js
```

Both engines must return semantically equivalent output.

## Deterministic gates

The reference engine currently implements:

1. terminal lifecycle state gate;
2. multidimensional maturity fit;
3. risk/HumanGate policy;
4. admitted-capability overlap detection;
5. local-first/offline/external-API/cost preferences;
6. deterministic routing score;
7. evidence-gated lifecycle transitions;
8. immutable pinning requirements;
9. runtime-evidence requirements before OBSERVED.

No engine may infer missing proof. Unknown data remains unknown.

## Portability requirements

The core must remain:

- dependency-free in its reference Python and JavaScript forms;
- offline-capable;
- deterministic for identical input;
- side-effect free;
- free of credentials and secrets;
- independent of UI and transport;
- testable from shared fixtures;
- versioned before breaking semantic changes.

A wrapper may add authentication, persistence, HTTP, MCP, queues, telemetry or UI. It must not redefine the core states or silently promote a claim from proposed to realised/verified.

## Conformance

`conformance/cases.json` is shared by all implementations.

Current reference checks cover:

- maturity gap;
- eligible candidate;
- R3 HumanGate;
- local-first rejection of required external API;
- HOLD state;
- duplicate admitted capability.

Every new runtime or language adapter must run the same conformance cases before being called compatible.

## Integration direction

```text
                         +--> Resource Radar / Vercel UI
                         +--> n8n workflows
                         +--> ChatGPT skill / connectors
JSON contract <-> CORE  +--> MCP tool wrapper
                         +--> local AI agents/runtimes
                         +--> CLI / scripts / services
                         +--> enterprise SI adapters
```

The Resource Radar is a discovery and interaction surface. The capability core is shared infrastructure.

## Next adapters

Planned adapters, in this order:

1. Resource Radar compatibility adapter;
2. n8n subworkflow contract;
3. MCP tool wrapper;
4. ChatGPT skill adapter;
5. minimal localhost HTTP sidecar;
6. event/message-bus adapter if an organisation needs it.

Adapters are added only when a real integration needs them; they are not prerequisites for the core.
