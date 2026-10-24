# ADR-0009: Model Tool Protocol
Status: Proposed

## §44 Question
Q09 — model tool protocol.

## Evidence
- Device result: `docs/spike-results/sm-t870-q09.json`
- Status: `SKIP`
- Code: `NO_MODEL_ENDPOINT`
- Probe exit: `2`
- Summary: Set TCA_MODEL_BASE_URL; quality benchmarking remains M7/M12

```json
{}
```

## Draft Decision
Review required. A probe PASS is evidence, not automatic architectural approval. A FAIL or SKIP must be resolved or covered by an explicitly accepted fallback.

## Fallback
Use the fallback stated in §44 of the master design until this ADR is changed from `Proposed` after review.

## Consequences
Document compatibility, security, performance, maintenance, and test effects during review.

## M1 Impact
Keep `Approved to begin M1: NO` until all blocking evidence and the two-device dependency requirement are resolved.
