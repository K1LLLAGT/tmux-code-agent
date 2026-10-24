# ADR-0005: Android Process Budget

Status: Accepted

## Evidence
- `docs/spike-results/sm-t870-q05.json`
- Result: `PASS / BOUNDED_FANOUT_OK`

## Decision
Keep TCA's per-session child-process fanout bounded. Default structured execution remains serialized unless a later measured device budget explicitly permits parallelism. The supervisor must account for its long-lived children and expose abnormal process growth through Doctor/health reporting.

## Fallback
If later device or soak testing shows Android process pressure, reduce concurrency first: cap runner/session fanout, keep `max_parallel_exec=1`, and surface a device-specific warning rather than applying system-level mitigations automatically.

## Consequences
The bounded-fanout strategy represented by Q05 is feasible on the tested device. This is not a claim that Android provides a fixed universal child-process limit; later soak/device tests remain required.

## M1 Impact
Q05 is resolved for the tested device. This ADR does not close the complete M0 gate.
