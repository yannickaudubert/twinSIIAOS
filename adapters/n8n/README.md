# n8n adapter — SIIAOS Capability Core

The n8n integration must **call** the portable Capability Core. It must not copy its decision logic into n8n expressions or Code nodes.

## Preferred topology

```
n8n workflow
   |
   | HTTP JSON
   v
capability-core sidecar
   |
   v
same Python core / same protocol / same conformance cases
```

This keeps n8n an orchestrator rather than a second implementation of policy.

## Sidecar

Start locally:

```bash
python3 capability-core/sidecar.py
```

Default endpoint:

```
GET  http://127.0.0.1:8765/health
POST http://127.0.0.1:8765/v0.1/execute
```

For Docker Compose, put n8n and the sidecar on the same internal network. If the sidecar binds beyond loopback, set `SIIAOS_CORE_TOKEN`. The sidecar refuses a non-loopback bind without a token.

## n8n subworkflow contract

Input item:

```json
{
  "protocol_version": "0.1",
  "operation": "assess",
  "record": {},
  "context": {}
}
```

HTTP Request node:

- Method: `POST`
- URL: configured internal sidecar URL, e.g. `http://capability-core:8765/v0.1/execute`
- Send Body: JSON
- Body: current item
- Authentication: Bearer token when configured
- Timeout: bounded
- Retry: bounded; do not convert transport failure into an admission decision

Output:

```json
{
  "protocol_version": "0.1",
  "result": {
    "verdict": "ELIGIBLE"
  }
}
```

## Workflow rule

A transport error is `UNKNOWN / BLOCKED`, never `ELIGIBLE`.

A downstream n8n branch may route by `result.verdict`:

- `ELIGIBLE` -> prepare experiment
- `HUMAN_GATE` -> request explicit review
- `DUPLICATE` -> compare with admitted capability
- `MATURITY_GAP` -> adapt the transformation path
- `LOCAL_POLICY_GAP` -> seek a local/cheaper alternative
- `BLOCKED/HOLD/REJECTED/RETIRED` -> stop mutation

## Container principle

Mount or package the canonical `capability-core/` into the sidecar container. Do not maintain a fork under the n8n project.

The same conformance fixtures must run against the deployed sidecar before production use.
