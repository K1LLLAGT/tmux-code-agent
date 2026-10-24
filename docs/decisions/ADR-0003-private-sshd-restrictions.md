# ADR-0003: Private Termux SSHD Restrictions

Status: Accepted

## §44 Question

Q03: Can non-root Termux `sshd` run with a private configuration and enforce the required authentication and key restrictions?

## Evidence

Primary device evidence:

- `docs/spike-results/sm-t870-q03.json`
- `docs/spike-results/sm-t870-q03-auth-matrix.json`
- `docs/spike-results/sm-t870-q03-basic-auth.json`

Historical diagnostic evidence:

- `docs/spike-results/sm-t870-q03.first-failure.json`
- `docs/spike-results/sm-t870-q03-auth-success-assertion-failure.json`

Tested environment:

- Android 13 / API 33
- aarch64
- Python 3.14.8
- OpenSSH 10.6p1
- Non-root Termux user

Verified checks:

- Correct session key authenticates.
- The exec key runs only its forced command.
- An unrelated key is rejected.
- A no-key request is rejected.
- Password authentication is rejected.
- Keyboard-interactive authentication is disabled.
- The exec key cannot allocate a PTY.
- TCP forwarding is refused.
- Agent forwarding is disabled in effective configuration.
- The daemon listens on `127.0.0.1`.
- The generated private configuration passes `sshd -t`.

## Decision

Use a dedicated, per-session, loopback-only Termux OpenSSH daemon.

Generate per-session Ed25519 host and client keys. Store the authorized-key file and daemon configuration in the private short runtime directory.

The exec identity uses an authorized-key entry with:

- `restrict`
- a forced command
- no PTY
- no forwarding

The daemon explicitly disables:

- password authentication
- keyboard-interactive authentication
- TCP forwarding
- stream-local forwarding
- agent forwarding
- X11 forwarding
- tunnels
- user-provided environment
- user RC processing

On the tested Termux OpenSSH build:

- `UsePAM` is unsupported and must be omitted.
- `PrintLastLog` is unsupported and must be omitted.
- `StrictModes no` is required for the dedicated temporary authorized-key path because Android/Termux ancestor-directory ownership and modes do not satisfy OpenSSH's standard home-directory checks.

`StrictModes no` is limited to this private loopback daemon. It does not modify the user's normal Termux SSH server configuration. TCA creates the runtime directory with mode `0700`, the authorized-key file with mode `0600`, and controls every file in that directory.

## Fallback

If the private OpenSSH daemon fails its startup or authentication self-test, do not silently weaken authentication further.

Offer the documented `LocalTransport` degraded fallback and clearly report that SSH transport is unavailable.

## Consequences

### Positive

- The required private SSH transport is feasible on the tested Termux device.
- Wrong-key, no-key, password, PTY, and forwarding restrictions are confirmed with active tests.
- The user's regular Termux SSH configuration is untouched.
- Authentication and restriction behavior is reproducible through an automated matrix.

### Negative

- Termux OpenSSH compatibility must be feature-detected rather than assuming desktop-Linux directives.
- `StrictModes no` weakens OpenSSH's normal path-mode checking for this daemon, so TCA must enforce private runtime ownership and permissions itself.
- A second target device must repeat this matrix before final M0 approval.

## M1 Impact

Non-blocking for M1 after the clean Q03 matrix is retained and the private-runtime permission invariants are implemented and tested.

This ADR does not approve Milestone 1 by itself. The overall M0 gate remains closed.
