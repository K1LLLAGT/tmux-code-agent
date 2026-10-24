# M1 Kickoff Checklist

## M0 Exit Gate

| Verification | Status |
|---|:---:|
| Q01 through Q14 evidence present | Complete |
| Evidence records | 14 |
| PASS results | 10 |
| FAIL results | 0 |
| SKIP results | 4 |
| Missing results | 0 |
| Evidence validator | PASS |
| Evidence review | PASS |
| M0 doctor gate | PASS |
| Remaining blockers | None |
| Physical-device coverage | 1/1 |
| Approved to begin M1 | YES |

## Accepted Deferrals

| Question | Evidence Code | ADR |
|---|---|:---:|
| Q09 | `NO_MODEL_ENDPOINT` | Accepted |
| Q11 | `MANUAL_CHECK_REQUIRED` | Accepted |
| Q12 | `DEVICE_COMPARISON_REQUIRED` | Accepted |
| Q14 | `SCREEN_OFF_NOT_TESTED` | Accepted |

Accepted deferrals remain visible as follow-up items. They do not block M1 while the authoritative M0 doctor reports no blockers.

## Repository and Release Integrity

| Verification | Status |
|---|:---:|
| RC2 HEAD verified | Complete |
| RC1 source commit verified | Complete |
| RC1 annotated tag object verified | Complete |
| RC1 archive checksum verified | Complete |
| Git object integrity verified | Complete |
| Shell syntax audit passed | Complete |
| Python syntax audit passed | Complete |
| Broken symbolic links | 0 |
| CRLF text files | 0 |

## Tooling Readiness

| Verification | Status |
|---|:---:|
| Outer tooling requires explicit `TCA_ROOT` | Complete |
| Root and non-root fallback available | Complete |
| M0 summary helper root resolution fixed | Complete |
| M0 summary helper creates its output directory | Complete |
| M0 summary output validated as JSON | Complete |
| ADR rewriting removed from summary helper | Complete |
| Accepted ADRs preserved during sandbox testing | Complete |

## M1 Actions

- [x] Confirm the M0 doctor reports `Approved to begin M1: YES`.
- [x] Preserve accepted ADRs as authoritative.
- [x] Preserve RC1 as an immutable release boundary.
- [x] Retain accepted deferrals as documented follow-up items.
- [ ] Record the M1 kickoff commit.
- [ ] Confirm the active M1 implementation scope.
- [ ] Run the targeted M1 tests after the first implementation change.
- [ ] Run the complete regression suite before closing M1.
- [ ] Preserve a verified checkpoint before beginning M2.

## Release Boundary

RC1 remains frozen and immutable.

Do not rebuild or replace the verified RC1 artifacts. New source, application, packaging, and archive changes belong to RC2 or a later release.
