#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
CORE = ROOT / "capability-core"
sys.path.insert(0, str(CORE))

import engine
from mcp.server import MCPServer

mcp = MCPServer("SIIAOS Capability Core")

@mcp.tool()
def assess_capability(record: dict[str, Any], context: dict[str, Any] | None = None) -> dict[str, Any]:
    """Assess one capability candidate using the canonical SIIAOS protocol semantics."""
    return {
        "protocol_version": "0.1",
        "result": engine.assess(record, context or {})
    }

@mcp.tool()
def route_capabilities(records: list[dict[str, Any]], context: dict[str, Any] | None = None) -> dict[str, Any]:
    """Route and rank capability candidates without changing canonical registry state."""
    return {
        "protocol_version": "0.1",
        "result": engine.route(records, context or {})
    }

@mcp.tool()
def transition_capability(record: dict[str, Any], target_state: str, transition_request: dict[str, Any] | None = None) -> dict[str, Any]:
    """Validate and propose one lifecycle transition without performing external mutation."""
    return {
        "protocol_version": "0.1",
        "result": engine.transition(record, target_state, transition_request or {})
    }

@mcp.resource("siiaos://capability-core/protocol")
def protocol() -> dict[str, Any]:
    """Describe the stable SIIAOS capability-core contract."""
    return {
        "protocol_version": "0.1",
        "operations": ["assess", "route", "transition"],
        "status_discipline": {
            "model_output": "proposed",
            "runtime_observation": "observed",
            "successful_mutation_with_evidence": "realised",
            "independent_validation": "verified"
        },
        "rule": "MCP is an adapter. It must not redefine decision semantics."
    }
