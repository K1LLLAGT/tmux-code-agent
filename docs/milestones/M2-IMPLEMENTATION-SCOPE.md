# M2 Implementation Scope

## Objective

M2 hardens the runtime lifecycle so start, readiness, health, stop, destroy, stale-state recovery, and port-conflict behavior are deterministic and testable on Termux.

## In Scope

- Supervisor lifecycle transitions and persisted state
- Single-instance locking and stale-lock recovery
- PID validation and stale-PID cleanup
- Port reservation, conflict detection, and release
- Readiness and heartbeat reporting
- Partial-start rollback and idempotent stop/destroy
- CLI lifecycle integration for start, status, and stop
- Non-root-first execution with per-command escalation only when required
- Structured, redacted lifecycle errors and diagnostics

## Expected Subsystems and Files

- `supervisor/lifecycle.py`
- `supervisor/lock.py`
- `supervisor/ports.py`
- `supervisor/heartbeat.py`
- `supervisor/control.py`
- `supervisor/daemon.py`
- `supervisor/recovery.py`
- `core/state.py`
- `core/config.py`
- `core/paths.py`
- `cli/launch.py`
- `cli/status.py`
- `cli/stop.py`
- `tests/unit/test_lifecycle.py`
- `tests/unit/test_daemon_lock.py`
- `tests/unit/test_ports.py`
- `tests/integration/test_stale_pid.py`
- `tests/integration/test_port_conflict.py`
- `tests/device/test_m2_lifecycle.sh`

Additional files may change only when directly required by the declared lifecycle behavior and covered by tests.

## Out of Scope

- Rebuilding or modifying RC1 artifacts
- Rewriting accepted ADRs or historical milestone evidence
- Android companion feature expansion
- Model-provider feature work
- UI redesign
- Release publication or packaging changes

## Implementation Controls

- Keep changes within the declared M2 scope.
- Preserve accepted ADR decisions.
- Add tests before or with new behavior.
- Run targeted tests after each bounded change.
- Run dependent device gates when shared lifecycle behavior changes.
- Keep non-root execution as the default.
- Escalate only the individual operation that requires root.
- Do not modify RC1 artifacts.
- Do not rewrite historical evidence.
- Keep release packaging separate from implementation commits.
