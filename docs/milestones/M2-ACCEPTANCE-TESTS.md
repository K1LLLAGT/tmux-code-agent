# M2 Acceptance Tests

## Targeted Automated Tests

```bash
PY="$PWD/.m0-venv/bin/python"

"$PY" -m pytest -q \
  tests/unit/test_lifecycle.py \
  tests/unit/test_daemon_lock.py \
  tests/unit/test_ports.py \
  tests/integration/test_stale_pid.py \
  tests/integration/test_port_conflict.py \
  tests/integration/test_dry_run.py
```

## Device Gate

```bash
bash tests/device/test_m2_lifecycle.sh
```

Required result:

```text
M2 health: READY
M2 DEVICE LIFECYCLE: PASS
```

## Dependent Gates

Run these when shared tmux or launch behavior changes:

```bash
bash tests/device/test_m1_dry_run.sh
bash tests/device/test_m3_tmux.sh
```

## Full Regression Gate

```bash
PY="$PWD/.m0-venv/bin/python"
"$PY" -m pytest -q tests/unit tests/integration tests/fault

for test_script in tests/device/test_*.sh; do
  bash "$test_script"
done
```

## Acceptance Criteria

- Targeted tests pass.
- M2 lifecycle device gate passes.
- Full regression suite passes without reducing the verified test count.
- All device gates pass.
- No accepted ADR is contradicted.
- No RC1 artifact changes.
- `git diff --check` passes.
- `git fsck --no-progress` exits zero.
- Repository is clean after the completion commit.
