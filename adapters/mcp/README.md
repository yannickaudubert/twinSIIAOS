# MCP adapter — SIIAOS Capability Core

This adapter exposes the **existing deterministic core** as MCP tools. MCP is not a second policy engine.

The official MCP Python SDK v2 is the current stable line and supports the 2026-07-28 specification. The v2 high-level server class is `MCPServer`.

## Install

```bash
python -m venv .venv
. .venv/bin/activate
pip install "mcp>=2,<3"
```

## Development / inspector

```bash
uv run --with "mcp[cli]>=2,<3" mcp dev adapters/mcp/server.py
```

## Streamable HTTP

```bash
uv run --with "mcp[cli]>=2,<3" mcp run adapters/mcp/server.py --transport streamable-http
```

## Exposed tools

- `assess_capability(record, context)`
- `route_capabilities(records, context)`
- `transition_capability(record, target_state, transition_request)`

Resource:

- `siiaos://capability-core/protocol`

## Security boundary

The MCP server exposes **read/decision tools only**. It does not install, deploy, delete, publish or mutate registry state.

A later mutation server must be a separate capability with explicit authorization and HumanGate semantics.

## Compatibility rule

Any MCP client or plugin consuming these tools must preserve:

- protocol version;
- verdict;
- reasons;
- maturity gaps;
- risk/HumanGate;
- duplicate-capability detection;
- local-first policy outcome.

The model may prepare `record` and `context`, but the deterministic core returns the verdict.
