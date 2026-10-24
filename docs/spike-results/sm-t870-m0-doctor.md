# M0 Doctor Report

- Primary device: `sm-t870`
- Virtual environment: **PASS**
- Gate: **GO**
- Physical-device coverage: **1/1**

## Q/ADR Matrix

| Q | Result | Code | ADR |
|---|---|---|---|
| Q01 | PASS | `CONTROL_FRAMES_OK` | Accepted |
| Q02 | PASS | `FEATURES_RECORDED` | Accepted |
| Q03 | PASS | `AUTH_MATRIX_OK` | Accepted |
| Q04 | PASS | `CONTROLMASTER_OK` | Accepted |
| Q05 | PASS | `BOUNDED_FANOUT_OK` | Accepted |
| Q06 | PASS | `BROWSER_LAUNCH_OK` | Accepted |
| Q07 | PASS | `LIVE_WEB_STACK_OK` | Accepted |
| Q08 | PASS | `INSTALL_OK` | Accepted |
| Q09 | SKIP | `NO_MODEL_ENDPOINT` | Accepted |
| Q10 | PASS | `PRIVATE_STORAGE_OK` | Accepted |
| Q11 | SKIP | `MANUAL_CHECK_REQUIRED` | Accepted |
| Q12 | SKIP | `DEVICE_COMPARISON_REQUIRED` | Accepted |
| Q13 | PASS | `LICENSE_METADATA_OK` | Accepted |
| Q14 | SKIP | `SCREEN_OFF_NOT_TESTED` | Accepted |

## Validated Physical Devices

- `23cdc706bc4c83d4`: samsung SM-T870, Android 13 API 33, aarch64

## Blockers

- None

## Warnings / Accepted Deferrals

- Q09: accepted deferral NO_MODEL_ENDPOINT
- Q11: accepted deferral MANUAL_CHECK_REQUIRED
- Q12: accepted deferral DEVICE_COMPARISON_REQUIRED
- Q14: accepted deferral SCREEN_OFF_NOT_TESTED
