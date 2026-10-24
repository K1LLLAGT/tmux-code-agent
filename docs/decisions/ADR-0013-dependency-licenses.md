# ADR-0013: Dependency License Metadata

Status: Accepted

## §44 Question

Q13: Can the candidate pure-Python dependency set be identified with exact versions and machine-readable license metadata without guessing?

## Evidence

- `docs/spike-results/sm-t870-q13.json`
- `docs/spike-results/sm-t870-q13-license-metadata.txt`
- `docs/spike-results/sm-t870-m0-venv-freeze.txt`
- `docs/spike-results/sm-t870-q13.global-python-failure.json`
- `docs/spike-results/sm-t870-q13.legacy-license-field-failure.json`

Tested in the isolated `.m0-venv` on Android 13 / API 33, aarch64, Python 3.14.8.

Recorded distributions:

- Starlette 1.9.0: `BSD-3-Clause` via `License-Expression`
- Uvicorn 0.54.0: `BSD-3-Clause` via `License-Expression`
- WebSockets 17.3: `BSD-3-Clause` via `License-Expression`
- h11 0.16.0: `MIT` via legacy `License`
- AnyIO 4.15.1: `MIT` via `License-Expression`

The final audit reported `LICENSE_METADATA_OK` with no blocking distributions.

## Decision

Use the exact distributions resolved from `requirements.lock` inside the project-owned virtual environment.

License auditing must inspect installed distribution metadata in this order:

1. `License-Expression`
2. nonempty legacy `License`
3. license classifiers
4. otherwise `UNKNOWN`, which blocks release review

Never infer or guess a license from a package name, repository reputation, or previous version.

Record the exact version, selected license value, and metadata source in machine-readable evidence. Re-run the audit whenever the lock file changes.

## Fallback

If any required distribution is absent or has no usable installed license metadata, keep Q13 blocking. Review that distribution's included license files and authoritative project metadata manually before accepting a replacement or an explicit documented exception.

## Consequences

### Positive

- Current candidate dependencies have machine-readable permissive-license evidence.
- Modern SPDX `License-Expression` metadata is handled correctly.
- Lock-file changes trigger a repeatable audit rather than relying on memory.

### Negative

- Installed metadata can change between releases and must be re-audited.
- A machine-readable expression does not replace distribution and notice-file obligations in release packaging.

## M1 Impact

Q13 is resolved for the tested dependency lock and device environment. This ADR does not approve Milestone 1 by itself. The complete M0 gate remains open.
