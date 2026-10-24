# ADR-0008: Termux Dependency Installation and Device Coverage

Status: Accepted

## Evidence

Primary M0 evidence:

- `docs/spike-results/sm-t870-q08.json`
- `docs/spike-results/devices/samsung-sm-t870/device.json`
- `docs/spike-results/devices/samsung-sm-t870/q08.json`
- `docs/spike-results/devices/samsung-sm-t870/q08-freeze.txt`

The standardized physical-device bundle records a successful clean virtual-environment install on the Samsung SM-T870 with the current `requirements.lock`, followed by a successful `pip check` and no missing required runtime distributions.

## Decision

Use a project-owned isolated Python virtual environment and install the pinned runtime dependency set from `requirements.lock`. Do not depend on packages installed in the user's global Termux Python environment.

Device compatibility is validated through the common `scripts/m0-device-test.sh` evidence format. Device evidence is keyed and deduplicated by `physical_device_id`; it is not modeled as hard-coded Device A / Device B roles.

For the gate to begin Milestone 1, require at least one successful physical Android/Termux device bundle. This proves the M0 architecture and dependency set on real target hardware without claiming broad multi-device qualification.

Multi-device coverage remains required for later MVP/release qualification. The registry and doctor retain support for stricter coverage by setting `TCA_REQUIRED_PHYSICAL_DEVICES` to 2 or higher.

## Fallback

If a pinned runtime dependency cannot install cleanly on a target device or architecture, prefer, in order:

1. standard-library functionality;
2. a compatible pure-Python dependency;
3. explicitly vendored permissive pure-Python code after license review;
4. a documented device/architecture compatibility restriction if no safe portable replacement exists.

Do not silently weaken dependency validation to make an unsupported environment appear compatible.

## Validation Policy

### Milestone 1 entry

Minimum physical-device coverage: 1 successful distinct physical device.

### MVP / release qualification

Target physical-device coverage: at least 2 distinct physical Android/Termux devices, including the project's intended primary aarch64 environment and additional practical coverage as devices are available.

A release may adopt a stricter configured threshold without changing the evidence format:

`TCA_REQUIRED_PHYSICAL_DEVICES=<N>`

## Consequences

### Positive

- M1 can begin after a substantial real-device M0 validation instead of waiting on access to arbitrary additional hardware.
- The software remains device-independent by design and evidence format.
- Additional devices can be added without changing test scripts or naming them A/B.
- Release qualification can enforce stronger coverage than the M1 entry gate.

### Negative

- One-device M0 evidence does not establish broad Android/Termux portability.
- Multi-device problems may be discovered in later qualification and must remain visible rather than being inferred away.

## M1 Impact

Q08 is resolved for M1 entry when the device registry contains at least one valid PASS bundle matching the current `requirements.lock`.

This policy change does not itself mark the review approved. `scripts/m0-doctor.py gate` remains authoritative for the computed M0 blocker state.
