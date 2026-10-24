# ADR-0001: tmux Control Mode over a PTY

Status: Accepted

## Evidence
- `docs/spike-results/sm-t870-q01.json`
- Result: `PASS / CONTROL_FRAMES_OK`
- tmux 3.8 emitted `%begin`, `%end`, and `%session-changed` frames through the PTY probe on the SM-T870.

## Decision
Use tmux control mode over a PTY as Channel C's notification/hint stream. Treat notifications as hints only: after an event, re-query authoritative tmux state before acting. Keep ordinary tmux commands/polling as a compatibility fallback.

## Fallback
If control mode cannot be established or its parser becomes unhealthy, disable the control stream and poll/query tmux state directly. Do not infer pane/window state solely from missed events.

## Consequences
Control mode is feasible on the tested device and tmux version. The implementation still requires a bounded parser, reconnect handling, and event-then-query semantics.

## M1 Impact
Q01 is resolved for the tested device. This ADR does not approve M1 by itself.
