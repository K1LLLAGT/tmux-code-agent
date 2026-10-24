# Accepted Architecture Decision Summary

This document summarizes the accepted M0 architecture decisions. The individual files under `docs/decisions/` remain authoritative.

## Accepted Decisions

| ADR | Decision Area | Accepted Direction |
|---|---|---|
| ADR-0001 | tmux control-mode PTY | Use private tmux control-mode operation for managed terminal sessions. |
| ADR-0002 | tmux feature baseline | Use the verified Termux tmux feature set as the supported baseline. |
| ADR-0003 | Private SSH restrictions | Use a private, restricted SSH service and constrained execution model. |
| ADR-0004 | SSH ControlMaster | Support verified connection reuse with explicit socket and lifecycle handling. |
| ADR-0005 | Android process budget | Keep process fan-out bounded and account for Android resource constraints. |
| ADR-0006 | Browser launch | Use the verified Android and Termux browser-launch path with documented fallback behavior. |
| ADR-0007 | Python web stack | Use the validated isolated Python web stack for loopback application services. |
| ADR-0008 | Termux dependencies | Install and validate required dependencies through the accepted Termux workflow. |
| ADR-0009 | Model endpoint degradation | Allow operation without a configured model endpoint and surface the degraded state clearly. |
| ADR-0010 | Filesystem primitives | Restrict filesystem operations to validated private-storage and safe-path primitives. |
| ADR-0011 | Android IME and browser compatibility | Retain manual compatibility validation and documented fallback behavior. |
| ADR-0012 | CI device fidelity | Treat CI evidence as supplemental to accepted physical-device evidence. |
| ADR-0013 | Dependency licenses | Preserve dependency-license metadata and include licensing in validation and release review. |
| ADR-0014 | Wake-lock policy | Keep wake-lock support optional, explicit, visible, and non-blocking. |

## Accepted Deferrals

| Question | Evidence Code | Accepted Treatment |
|---|---|---|
| Q09 | `NO_MODEL_ENDPOINT` | Model endpoint absence is covered by the accepted degradation policy. |
| Q11 | `MANUAL_CHECK_REQUIRED` | IME and browser behavior remains a documented manual-validation item. |
| Q12 | `DEVICE_COMPARISON_REQUIRED` | CI evidence remains supplemental to accepted physical-device coverage. |
| Q14 | `SCREEN_OFF_NOT_TESTED` | Wake-lock support remains optional while screen-off comparison remains deferred. |

## M0 Gate Interpretation

The authoritative M0 doctor determines approval to begin M1.

The final verified result is:

```text
Evidence records:       14
PASS:                   10
FAIL:                   0
SKIP:                   4
Missing:                0
Physical coverage:      1/1
Blockers:               None
Approved to begin M1:   YES
```

Accepted ADR fallbacks and documented deferrals remain warnings and follow-up items rather than active blockers.

## Release Boundary

RC1 remains frozen and immutable. Future implementation and packaging changes belong to RC2 or a later release.
