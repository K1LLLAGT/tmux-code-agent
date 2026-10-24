# ADR-0009: Model Endpoint Discovery and Degraded Mode

Status: Accepted

## §44 Question

Q09: What model/tool-protocol capability is available on the target device, and what happens when no usable model endpoint exists?

## Evidence

Canonical evidence remains:

- `docs/spike-results/sm-t870-q09.json`
- Result: `SKIP / NO_MODEL_ENDPOINT`

Additional device inspection found:

- `llama-server`: not installed
- `ollama`: not installed
- no listener on the checked common model ports 8080, 11434, or 1234
- no obvious llama/Ollama/model-server process

No model was installed solely to force this M0 question to PASS. No claim is made about native tool calling, JSON-action reliability, minimum model size, or benchmark quality on this device.

## Decision

A reachable model endpoint is optional for TCA startup.

At runtime TCA must discover/probe the configured provider and classify the resulting capability. If there is no usable endpoint, TCA enters an explicit DEGRADED state:

- terminal remains available
- files/editor remain available
- Git/manual project functionality remains available
- model-backed autonomous agent execution remains unavailable
- the UI explains that a model must be connected before agent tasks can run

TCA must not silently download, install, start, or expose a model server merely because discovery fails.

A later model-capability probe must record the actual endpoint/server/model and classify tool behavior from observed responses rather than assumptions.

## Fallback

If a discovered model cannot reliably use the required tool protocol, degrade its capability instead of executing ambiguous model output.

Fallback order:

1. native tool mode when positively probed
2. strict structured JSON-action mode when positively probed
3. `chat_only` when tool behavior is not safe/reliable enough
4. no-model DEGRADED mode when no usable endpoint exists

A model below the eventual measured capability/quality threshold must not be presented as a fully autonomous coding agent merely to satisfy a benchmark gate.

## Deferred Measurement

Q09's performance/quality portion remains deferred until an actual local or explicitly configured endpoint is available. Later measurement must record at least:

- provider and endpoint type
- server version where available
- model identifier
- available context/capability information
- observed tool mode
- failing-test benchmark result
- failure/degradation behavior

## Consequences

### Positive

- Core TCA functionality does not depend on a particular local-model package being installed.
- No paid or automatically downloaded model is required merely to launch TCA.
- Capability is measured from the real configured endpoint rather than hard-coded by model name.
- Unsafe or incapable models degrade instead of being granted agent execution implicitly.

### Negative

- This SM-T870 M0 run does not establish a minimum useful model size or successful tool protocol.
- Real-model smoke and benchmark testing remains necessary in the later model/agent milestones.

## M1 Impact

ADR-0009 resolves the startup and fallback architecture when no model endpoint exists. Canonical Q09 correctly remains `SKIP / NO_MODEL_ENDPOINT` because no real model protocol was exercised.

This ADR does not approve Milestone 1 by itself. Remaining M0 gates still apply.
