# ADR-0004: SSH ControlMaster and ControlPersist

Status: Accepted

## §44 Question

Q04: Is OpenSSH connection multiplexing reliable enough on Termux
to reuse the private loopback SSH connection for structured
execution?

## Evidence

Primary reviewed evidence:

- `docs/spike-results/sm-t870-q04.json`
- `docs/spike-results/sm-t870-q04-explicit-socket-retry-v2.json`
- `docs/spike-results/sm-t870-q04-reuse-success-stop-terminal.json`

Historical diagnostic evidence:

- `docs/spike-results/sm-t870-q04-controlmaster.multiplex-failure.json`
- `docs/spike-results/sm-t870-q04-explicit-socket-refused.json`
- `docs/q04-first-finding.20261024T023124Z.tar.gz`

Q03 prerequisite:

- `docs/spike-results/sm-t870-q03.json`
- `docs/decisions/ADR-0003-private-sshd-restrictions.md`

Tested environment:

- Android 13 / API 33
- aarch64
- OpenSSH 10.6p1
- Non-root Termux user
- Private loopback-only SSH daemon
- Restricted forced-command exec key

## Findings

The initial probe created a master but ordinary calls did not reuse
it because they did not explicitly select the control socket.

The first explicit-socket retry reached the master, but its
`-N` bootstrap caused the master to refuse subordinate session
requests.

The successful retry:

- bootstrapped the master using the restricted forced-command key
- enabled bounded `ControlPersist`
- used an explicit session-private `ControlPath`
- explicitly selected that socket for subordinate calls
- retained the correct private port, identity, and host-key options

Verified behavior:

- The master started successfully.
- `ssh -O check` reported it as running.
- The ControlPath length was within the measured AF_UNIX budget.
- Three subordinate calls reused the master.
- Each reused call returned exactly `forced`.
- Server logs showed one public-key authentication before shutdown.
- The master remained healthy after the reused calls.
- `ssh -O stop` returned success.
- The control socket disappeared after `stop`.
- A post-stop control check failed as expected.
- A fresh independent SSH connection succeeded afterward.
- Final cleanup left no private SSH processes, sockets, or runtime
  directories.

An `ssh -O exit` operation issued after successful `-O stop` returned
a missing-control-socket error. This is expected because `stop` had
already removed the control listener. The two shutdown operations
must be tested in separate master lifecycles if both behaviors need
independent coverage.

## Decision

Use one OpenSSH ControlMaster per TCA session for Channel-B structured
execution when the device self-test succeeds.

Use:

- a private short `ControlPath`
- a runtime directory with mode `0700`
- `ControlMaster=auto` for subordinate calls
- a bounded `ControlPersist`
- explicit `-S <ControlPath>` selection
- the exact private SSH port
- the exact session identity
- the private host-key policy
- `ssh -O check` for health
- `ssh -O stop` for normal listener shutdown
- supervisor-owned process termination as the final cleanup authority

The master must be bootstrapped through a valid forced-command
connection. Do not create the production master using the unsuccessful
`-N` pattern observed in the first retry.

ControlMaster is an optimization and connection-management mechanism.
It is not persistent application state and it is not a security
boundary.

The session manifest, mutable state, command records, audit log, tmux,
and supervisor remain authoritative.

## Fallback

If master creation, reuse, health checking, or cleanup fails:

1. Mark ControlMaster unavailable for that TCA session.
2. Remove a stale control socket only after validating that no healthy
   master owns it.
3. Use independent key-authenticated loopback SSH connections.
4. Preserve the same Q03 forced-command and authentication restrictions.
5. Do not weaken SSH restrictions merely to keep multiplexing enabled.

If private SSH itself fails its Q03 self-test, use the separately tested
`LocalTransport` degraded fallback.

## Consequences

### Positive

- Three structured calls reused one authenticated connection.
- Reused calls avoided repeated public-key authentication.
- Explicit socket health checks are available.
- Normal shutdown removes the socket cleanly.
- Independent SSH remains available after master shutdown.

### Negative

- Every subordinate call must use an exact matching connection tuple.
- ControlPath length must remain bounded.
- Stale-socket handling requires health validation.
- The supervisor must remain responsible for final process cleanup.
- Startup patterns that authenticate without opening the permitted
  forced-command session may create a master that refuses later sessions.

## M1 Impact

The Q04 design decision is resolved for the tested SM-T870.

This ADR does not approve Milestone 1 by itself. The complete M0 gate,
including remaining Q findings and the second-device dependency
requirement, remains open.
