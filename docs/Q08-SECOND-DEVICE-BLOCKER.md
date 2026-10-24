# Q08 Second-Physical-Device M0 Blocker

Status: BLOCKING M0

## Requirement

The pinned runtime dependency set must be successfully installed and
validated on a second physical Android/Termux device.

Device A is the Samsung SM-T870.

Testing a second virtual environment on the SM-T870 does not satisfy
this requirement because it is still the same physical device.

## Device A Status

Device:

- Model: SM-T870
- Android: 13
- API: 33
- Architecture: aarch64
- Python: 3.14.8

Dependency result:

- `requirements.lock`: available
- clean virtual environment creation: PASS
- `pip install -r requirements.lock`: PASS
- `pip check`: PASS
- required runtime packages: PASS
- canonical Q08: `PASS / INSTALL_OK`

The same-device Device-B procedure was also rehearsed successfully
after the lock file was copied into place.

That rehearsal does not count as second-device evidence.

## Lock File

Required input:

`requirements.lock`

Expected SHA-256:

`b2d728c191093dcd5bc43f535d67831569cf00a1d2185a2484d8ad10802850b5`

Device B must calculate its local hash and verify that it matches this
value before dependency installation.

## Device B Requirements

Device B must be a second physical Android device running Termux.

Record:

- device model
- Android release
- API level
- architecture
- Python version
- Termux environment
- requirements.lock SHA-256

Then create a fresh virtual environment and verify:

- venv creation succeeds
- pip installation succeeds
- pip check succeeds
- required runtime distributions are installed
- no required distribution is missing

Required distributions:

- starlette
- uvicorn
- websockets
- h11
- anyio

## Required Device B Evidence

Copy these files back to Device A:

- `q08-device-b.json`
- `q08-device-b-freeze.txt`
- `q08-device-b.sha256`

The JSON may report PASS only when the actual second physical device
produced all required successful results.

Required successful values include:

- `question = Q08`
- `status = PASS`
- `code = SECOND_DEVICE_INSTALL_OK`
- `physical_device = true`
- `device_role = device-b`
- `install_returncode = 0`
- `pip_check_returncode = 0`
- `missing_packages = []`

## Failed/Rehearsal Evidence

The initial same-device Device-B attempt failed because
`requirements.lock` had not been copied into the rehearsal directory.

A later SM-T870 rehearsal successfully installed the lock and passed
`pip check`.

Neither same-device attempt satisfies the second-physical-device gate.

Do not copy same-device PASS evidence into a filename matching the
doctor's Device-B evidence pattern.

## Completion

After genuine Device-B evidence is copied into:

`docs/spike-results/`

run:

    python scripts/m0-doctor.py fix

    python scripts/m0-doctor.py gate

The Device-B requirement is complete only when the doctor no longer
reports:

`Q08: second physical-device dependency PASS evidence missing`

Do not manually override the M0 gate to compensate for missing
Device-B evidence.
