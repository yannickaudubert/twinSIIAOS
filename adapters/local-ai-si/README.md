# Local AI / agent / SI adapter pattern

Every local AI component or information-system component integrates through the same protocol envelope.

## Direct process integration

Python:

```python
from capability_core import engine
result = engine.execute(envelope)
```

When the folder name is kept as `capability-core`, import it by path or package it in the host project without changing semantics.

Node:

```javascript
const core = require("./capability-core/engine.js");
const result = core.execute(envelope);
```

## Process boundary

```bash
echo '<json envelope>' | python3 capability-core/engine.py
echo '<json envelope>' | node capability-core/engine.js
```

## Service boundary

Use the local sidecar:

```
POST /v0.1/execute
```

This is the preferred shape for:

- n8n;
- local LLM agents;
- LM Studio-side tools;
- MCP wrappers;
- desktop clients;
- SI applications written in other languages;
- containers that should not embed Python/Node policy code.

## Important distinction

The AI model may propose a candidate record or context. It does **not** decide whether its own proposal is admitted.

The deterministic core evaluates the structured envelope outside model reasoning.

## Required status discipline

Model output = proposed.

Runtime/tool observation = observed.

A successful mutation with evidence = realised.

A separate validation gate = verified.

No adapter may collapse these states.
