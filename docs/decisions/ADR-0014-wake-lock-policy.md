# ADR-0014: Optional Android Wake-Lock Policy

Status: Accepted

## §44 Question

Q14: Is a wake lock required for TCA sessions that run long agent
tasks while the Android device screen is off?

## Evidence

Primary device evidence:

- `docs/spike-results/sm-t870-q14.json`
- `docs/spike-results/sm-t870-q14-screen-on-timing.log`

Historical evidence:

- `docs/spike-results/sm-t870-q14.original-skip.json`

Tested environment:

- Samsung SM-T870
- Android 13 / API 33
- aarch64
- Termux

Observed behavior:

- `termux-wake-lock` is installed.
- `termux-wake-unlock` is installed.
- Clean wake-lock acquisition returned exit 0.
- Clean wake-lock release returned exit 0.
- A 36-iteration timing run completed without a gap exceeding
  15 seconds.
- The screen remained on throughout that timing run.

An earlier wake-lock invocation exited 139 after its shell current
working directory had been deleted during Q06 cleanup. That attempt
produced `getcwd()` failures and is excluded from the wake-lock
feasibility result.

Screen-off execution was not tested. The evidence therefore does not
establish whether a wake lock is required or sufficient for long TCA
tasks while the screen is off.

## Decision

Wake-lock support is optional.

TCA must:

- default to wake lock OFF
- expose an explicit `--wake-lock` option
- make wake-lock state visible to the user
- acquire the lock only after an explicit request or configuration
- release it during normal stop/destroy
- attempt release during abnormal cleanup where possible
- never silently enable a permanent wake lock
- continue to function without wake-lock support

Wake lock is a power-management aid, not a correctness, persistence,
security, or transport boundary.

The supervisor must continue to recover and re-verify component state
after device sleep regardless of wake-lock configuration.

## Fallback

If wake-lock commands are unavailable, fail, or are ineffective on a
device:

1. Continue without a wake lock.
2. Surface a warning for long background tasks.
3. Preserve normal state, recovery, timeout, and resume semantics.
4. Do not automatically modify Android battery-optimization settings.
5. Document device-specific guidance when later physical testing
   demonstrates a need.

## Deferred Device Validation

A later physical-device test should explicitly:

1. Acquire the wake lock.
2. Start a timestamped long-running task.
3. Turn the screen off.
4. Leave the device idle for a measured interval.
5. Turn the screen back on.
6. Verify execution continuity.
7. Repeat without the wake lock.
8. Compare results.

Until that comparison exists, TCA must not claim that wake lock is
required or sufficient for screen-off execution.

## Consequences

### Positive

- Wake-lock integration is available on the tested Termux device.
- Normal users do not incur unnecessary wake-lock power consumption.
- Long-running users may explicitly opt in.
- TCA remains functional when wake-lock support is absent.

### Negative

- Screen-off behavior remains device and power-policy dependent.
- The current M0 evidence does not measure the benefit of holding the
  wake lock.
- Later physical-device testing is still required before publishing
  strong screen-off reliability claims.

## M1 Impact

ADR-0014 resolves the architectural question by making wake-lock
support optional and non-blocking.

Q14 device evidence remains `SKIP / SCREEN_OFF_NOT_TESTED`, accurately
representing the test that was actually performed.

This ADR does not by itself approve Milestone 1. The remaining M0 gates
must still be completed.
