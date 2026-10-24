# ADR-0012: CI and Physical-Device Test Authority

Status: Accepted

## §44 Question

Q12: Can a Termux-oriented CI environment reproduce real Android/Termux behavior well enough to replace physical-device testing?

## Evidence

Canonical evidence remains:

- `docs/spike-results/sm-t870-q12.json`
- Result: `SKIP / DEVICE_COMPARISON_REQUIRED`

This M0 run has already produced physical-device evidence for Android/Termux-specific behavior including private sshd operation, tmux behavior, browser launch, filesystem primitives, ControlMaster behavior, and live web-stack resource measurement. No paired CI-versus-device comparison artifact currently demonstrates equivalent behavior for Q12, so canonical Q12 remains SKIP.

## Decision

CI and physical-device testing have different authority.

CI is the primary gate for portable and deterministic project logic, including unit tests, schema/protocol validation, parsers, pure application logic, static checks, and integration tests that do not claim Android-specific semantics.

Physical Android/Termux devices remain authoritative for behaviors that depend on the Android runtime, Termux packaging/process environment, platform services, device power policy, browser/IME behavior, or other device-specific operating-system semantics.

A CI PASS must never overwrite or substitute for a required physical-device FAIL/SKIP merely because the same high-level test name exists in both environments.

## Fallback

If CI cannot faithfully reproduce an Android/Termux subsystem:

1. keep its portable/unit coverage in CI where useful;
2. classify the Android-specific portion as device-required;
3. run that portion in the physical-device suite;
4. make the device result authoritative for release gating;
5. document any known CI/device divergence instead of hiding it.

CI remains valuable even when it is not a complete Android emulator.

## Deferred Comparison

A later comparison should run equivalent portable/device probes in the selected CI environment and on supported physical devices, then record concrete similarities and differences. Until that comparison exists, TCA must not claim that CI reproduces Android/Termux completely.

## Consequences

### Positive

- Fast deterministic validation stays in CI.
- Android-specific claims remain grounded in real-device evidence.
- CI environment limitations cannot silently weaken the release gate.

### Negative

- Maintaining a physical-device suite remains mandatory for Android-specific functionality.
- Some failures may only reproduce on particular Android/Termux/browser/device combinations.

## M1 Impact

ADR-0012 resolves the authority boundary for Q12. Canonical Q12 correctly remains `SKIP / DEVICE_COMPARISON_REQUIRED` until a paired comparison is recorded.

The physical-device suite remains a required gate for Android-specific behavior. This ADR does not approve M1 by itself.
