# ADR-0002: tmux Feature Baseline and Detection

Status: Accepted

## Evidence
- `docs/spike-results/sm-t870-q02.json`
- Result: `PASS / FEATURES_RECORDED`
- tmux 3.8 accepted `new-session -e` and `pause-after` in the device probe.
- `refresh-client -f no-output` returned `no current client`, so the option was reached but was not validated against an attached client by Q02.

## Decision
Require the baseline tmux functionality demonstrated by Q01/Q02, but feature-detect optional/newer controls at runtime. Use `new-session -e` where supported. Do not make `refresh-client -f no-output` a hard prerequisite until exercised against an attached client.

## Fallback
For an unavailable optional tmux feature, use the documented polling/query or output-handling fallback rather than aborting the session. A missing required baseline feature fails Doctor with a clear compatibility result.

## Consequences
The tested tmux 3.8 build is suitable for the planned private tmux server. Optional behavior remains guarded by feature detection rather than version-string assumptions alone.

## M1 Impact
Q02 is resolved for the tested device. The overall M0 gate remains open.
