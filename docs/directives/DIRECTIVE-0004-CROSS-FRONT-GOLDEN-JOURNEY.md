# DIRECTIVE-0004 — Cross-front golden journey

Status: ACTIVE

## Purpose

The unit of progress is no longer one more isolated A/B/C feature. It is a useful mission that crosses the three fronts without creating a second truth.

## Reference journey

1. A human states a need.
2. Front C creates or opens a Mission Workbench.
3. A ContextPack is assembled from permitted sources.
4. Front B performs discovery / pre-audit / analysis and preserves UNKNOWN.
5. Front A receives or validates Evidence and OperationRecord-compatible objects.
6. Front C Research Studio exposes sources, evidence, contradictions and gaps.
7. Front C Decision Room presents alternatives and consequences.
8. Front A enforces mandate/policy/HumanGate and records the decision.
9. Front B produces the governed deliverable or next transformation.
10. Front C Deliverable Studio supports review and capture.
11. Front A records immutable evidence/decision/record links.
12. RETEX updates methods, capabilities or future mission proposals without rewriting history.

## Required acceptance checks

The journey is not accepted unless:

- one tenant/mission scope is explicit throughout;
- no Front B derived object silently becomes canon;
- no Front C UI state silently becomes canon;
- every critical action has an authority path;
- UNKNOWN and contradictions can survive the journey;
- evidence is addressable;
- a decision requiring a human cannot be auto-admitted;
- a failed operation can be represented;
- rollback/stop is available where an action mutates state;
- the final result is useful to a non-technical human;
- the same contracts can support personal, cabinet and client scopes with different policies rather than different cores.

## Proof ladder

Keep separate:

`DESIGNED -> CODED -> TESTED -> DEPLOYED -> OBSERVED`

A mock Golden Journey proves only the layers it actually executes.

The first production-grade proof must be an observed local journey with real authority, evidence and recovery behavior.
