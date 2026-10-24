# tmux-code-agent

A Termux-first, tmux-backed coding-agent runtime for Android with private session isolation, loopback web access, lifecycle supervision, filesystem policy controls, model-provider support, auditability, upgrade safety, and an Android companion launcher.

This README consolidates the verified project path from **M00 through M14**, including the accepted architecture decisions, milestone outcomes, current hardening work, release boundaries, tests, and operational controls.

## Project Status

| Item | Current verified state |
|---|---|
| Active branch | `m2` |
| Validated M2 baseline commit | `65524e9e1ed46b4059d45b1470acb1c60d8ccf67` |
| Current hardening commit | `fix(m2): harden lifecycle and daemon locking` |
| Python regression suite | 124 passed |
| Device gates | M1 through M14 passed |
| RC2 live-start test | Passed |
| M2 baseline gate | Matches validated M2 baseline commit |
| Repository state | Clean |
| Git integrity | Passed |
| RC1 archive checksum | Passed |
| Accepted ADRs | Preserved |
| RC1 boundary | Frozen and immutable |

## Current Validation Summary

The current M2 baseline was validated with:

```text
Branch:                 m2
HEAD:                   65524e9e1ed46b4059d45b1470acb1c60d8ccf67
Pytest regression:      124 passed
Device suite:           M1 through M14 passed
RC2 live start:         passed
Baseline gate:          matches HEAD
Baseline script syntax: passed
Working tree:           clean
Staged changes:         none
Git fsck exit:          0
RC1 archive checksum:   OK
Overall result:         M2 FULL VALIDATION PASS
```

Validation evidence:

```text
~/tmux-code-agent/m2-full-suite-20261024T163342Z.log
```

## Core Goals

`tmux-code-agent` is designed to provide:

- Private tmux servers per managed session
- Deterministic lifecycle state and recovery behavior
- Loopback-only web and control services
- Safe Termux path and workspace handling
- Non-root operation by default
- Per-command privilege escalation only when required
- Filesystem containment and safe-write primitives
- Explicit user approvals and hard-deny policy enforcement
- Model-provider abstraction and fallback handling
- Audit trails, bundles, recovery, and upgrade support
- Android companion launching without weakening runtime boundaries
- Reproducible milestone and release validation

## Repository Layout

```text
agent/          Agent planning, prompts, compaction, ownership, and execution
android/        Android companion application
audit/          Audit writing, verification, and bundle creation
cli/            User-facing commands and rendering
core/           IDs, paths, context, manifests, state, configuration, releases
docs/           ADRs, milestone records, evidence, reviews, and upgrade notes
frontend/       Browser interface components
fsguard/        Canonicalization, safe I/O, atomic writes, backups, and trash
gitsafe/        Git baselines, diffs, snapshots, and worktrees
models/         Model providers, capabilities, fallbacks, and tool protocol
policy/         Approvals, profiles, capabilities, classification, and hard denies
scripts/        Milestone, test, release, soak, and spike tooling
store/          Persistent database and migrations
supervisor/     Lifecycle, locking, ports, heartbeat, control, daemon, recovery
termbridge/     Terminal frames, replay, PTY bridge, and viewer support
tests/          Unit, integration, fault, fixture, and device tests
tmuxctl/        Private tmux configuration and control
transport/      Local and SSH execution transports
tools/          Tool schemas, registry, filesystem, execution, Git, and metadata
web/            Loopback web application, authentication, routes, and WebSockets
```

## Milestone Map

| Milestone | Area | Verified outcome |
|---|---|---|
| M00 | Feasibility, evidence, and architecture | Accepted ADR set, physical-device evidence, no blockers |
| M1 | Safe dry-run foundation | IDs, paths, context, manifest, state, configuration |
| M2 | Runtime lifecycle | Supervisor lifecycle, locks, ports, readiness, recovery |
| M3 | Private tmux | Private server, adoption, control mode, resize, process exit |
| M4 | SSH runner | Restricted SSH execution and connection reuse |
| M5 | Terminal channel | Terminal framing, replay, PTY, viewer, backpressure |
| M6 | Filesystem and policy | Safe paths, atomic writes, approvals, hard denies |
| M7 | Model and agent | Provider protocol, fallback, planning, completion, tool use |
| M8 | MVP core | Integrated runtime and installer safety |
| M9 | UI areas | Browser panels and operational UI structure |
| M10 | Control mode | YOLO and control workflows with policy boundaries |
| M11 | Worktree and bundle | Git-safe worktrees, snapshots, and evidence bundles |
| M12 | Providers and context | Provider fallback and context handling |
| M13 | Upgrade and rollback | Release flip, migration, marker, and rollback behavior |
| M14 | Readiness | Final budgets, readiness gate, and v1 validation |

# M00: Feasibility, Evidence, and Architecture

M00 established whether the proposed runtime could operate safely and predictably in Termux on Android.

## M00 Questions

The feasibility program covered Q01 through Q14:

| Question | Area | Result |
|---|---|---|
| Q01 | tmux control-mode PTY | PASS |
| Q02 | tmux feature baseline | PASS |
| Q03 | Private SSH restrictions | PASS |
| Q04 | SSH ControlMaster | PASS |
| Q05 | Android process budget | PASS |
| Q06 | Browser launch | PASS |
| Q07 | Python web stack | PASS |
| Q08 | Termux dependencies | PASS |
| Q09 | Model tool protocol | Accepted deferral |
| Q10 | Filesystem primitives | PASS |
| Q11 | Android IME and browser behavior | Accepted deferral |
| Q12 | CI device fidelity | Accepted deferral |
| Q13 | Dependency licenses | PASS |
| Q14 | Wake-lock behavior | Accepted deferral |

M00 evidence summary:

```text
Records:                 14
PASS:                    10
FAIL:                    0
SKIP:                    4
Missing:                 0
Physical-device coverage: 1/1
Blockers:                none
Approved to begin M1:    YES
```

## Accepted M00 Deferrals

| Question | Evidence code | Treatment |
|---|---|---|
| Q09 | `NO_MODEL_ENDPOINT` | Covered by the accepted degraded model-endpoint policy |
| Q11 | `MANUAL_CHECK_REQUIRED` | Retained as a physical compatibility follow-up |
| Q12 | `DEVICE_COMPARISON_REQUIRED` | CI remains supplemental to accepted device evidence |
| Q14 | `SCREEN_OFF_NOT_TESTED` | Wake-lock support remains optional and screen-off comparison remains deferred |

The authoritative M0 doctor determines milestone approval. Accepted ADR fallbacks and recorded deferrals are warnings and follow-up items, not blockers, when the doctor reports no blockers.

## Accepted Architecture Decisions

The files under `docs/decisions/` remain authoritative.

| ADR | Decision area | Accepted direction |
|---|---|---|
| ADR-0001 | tmux control-mode PTY | Use private tmux control mode for managed terminal sessions |
| ADR-0002 | tmux baseline | Use the verified Termux tmux feature baseline |
| ADR-0003 | Private SSH | Use a private, restricted SSH service and constrained execution model |
| ADR-0004 | ControlMaster | Support verified SSH connection reuse with explicit lifecycle handling |
| ADR-0005 | Process budget | Keep process fan-out bounded for Android constraints |
| ADR-0006 | Browser launch | Use the verified Android and Termux browser-launch path with fallback behavior |
| ADR-0007 | Python web stack | Use an isolated loopback Python web stack |
| ADR-0008 | Dependencies | Install and validate dependencies through the accepted Termux workflow |
| ADR-0009 | Endpoint degradation | Operate without a configured model endpoint and clearly report degradation |
| ADR-0010 | Filesystem primitives | Use validated private-storage and safe-path primitives |
| ADR-0011 | IME and browser | Retain manual compatibility validation and documented fallbacks |
| ADR-0012 | CI fidelity | Treat CI evidence as supplemental to physical-device evidence |
| ADR-0013 | Licenses | Preserve dependency-license metadata in validation and release review |
| ADR-0014 | Wake lock | Keep wake-lock support optional, explicit, visible, and non-blocking |

# M1: Safe Dry-Run Foundation

M1 created the safe, non-destructive foundation for session creation.

## M1 Scope

- Session ID generation and validation
- Termux-aware state and runtime paths
- Workspace validation
- Environment capture with secret redaction
- Session manifest creation
- Atomic state writing
- Configuration loading
- Dry-run command behavior

## M1 Key Files

```text
core/ids.py
core/paths.py
core/context.py
core/manifest.py
core/state.py
core/config.py
cli/launch.py
tests/unit/test_ids.py
tests/unit/test_paths.py
tests/unit/test_context.py
tests/unit/test_manifest_state_config.py
tests/integration/test_dry_run.py
tests/device/test_m1_dry_run.sh
```

## M1 Validation

```text
Targeted tests:      25 passed
Device dry run:      PASS
Full M1 regression:  117 passed
M1 kickoff commit:   5a4b61a502f05425ffcaf39a3f51db57db202ad7
```

An external M1 checkpoint was created under:

```text
~/tmux-code-agent/checkpoints/m1-20261024T155447Z/
```

It contains a source archive, complete Git bundle, manifest, branch relationship record, full-suite log hash, and aggregate checksums.

# M2: Runtime Lifecycle Hardening

M2 makes runtime startup, readiness, locking, recovery, and shutdown deterministic and testable.

## M2 Declared Scope

- Supervisor lifecycle transitions and persisted state
- Single-instance locking and stale-lock recovery
- PID validation and stale-PID cleanup
- Port reservation and conflict handling
- Readiness and heartbeat reporting
- Partial-start rollback
- Idempotent stop and destroy
- CLI lifecycle integration
- Non-root-first operation
- Per-command escalation only when required
- Structured and redacted lifecycle failures

## Current M2 Hardening

Current commit:

```text
65524e9e1ed46b4059d45b1470acb1c60d8ccf67
fix(m2): harden lifecycle and daemon locking
```

Implemented behavior:

- Same-state lifecycle transitions are idempotent
- Illegal transitions remain rejected
- Lock creation is exclusive and atomic
- Lock records include PID and Linux process start time
- PID reuse is detected through process identity
- Stale locks can be reclaimed
- Live locks cannot be stolen
- Legacy PID-only locks are conservatively protected
- Lock release requires matching ownership

## M2 Affected Subsystems

```text
supervisor/lifecycle.py
supervisor/lock.py
supervisor/ports.py
supervisor/heartbeat.py
supervisor/control.py
supervisor/daemon.py
supervisor/recovery.py
core/state.py
core/config.py
core/paths.py
cli/launch.py
cli/status.py
cli/stop.py
```

## M2 Acceptance Tests

```bash
PY="$PWD/.m0-venv/bin/python"

"$PY" -m pytest -q \
  tests/unit/test_lifecycle.py \
  tests/unit/test_daemon_lock.py \
  tests/unit/test_ports.py \
  tests/integration/test_stale_pid.py \
  tests/integration/test_port_conflict.py \
  tests/integration/test_dry_run.py

bash tests/device/test_m2_lifecycle.sh
```

Current results:

```text
First lifecycle slice:  11 passed
Targeted M2 set:        14 passed
Full regression:        124 passed
M2 lifecycle gate:      PASS
M1 dependent gate:      PASS
M3 dependent gate:      PASS
Complete device suite:  PASS
```

# M3: Private tmux Runtime

M3 established isolated tmux operation for managed sessions.

Verified behaviors:

- Private tmux server startup
- Dedicated socket use
- Session adoption
- Control-mode operation
- Window and pane discovery
- PTY resize reporting
- Pane process-exit reporting
- Isolation from unrelated user tmux servers

Current device result:

```text
M3 windows:                     PASS
M3 adopt:                       PASS
M3 control mode:                PASS
M3 resize reporting:            PASS
M3 pane process-exit reporting: PASS
M3 PRIVATE TMUX:                PASS
```

# M4: SSH Runner

M4 added the restricted SSH execution path used for controlled local or remote command transport.

Verified behaviors include:

- Private SSH service restrictions
- Authentication handling
- Explicit control-socket behavior
- Connection reuse
- Controlled command execution
- Result handling

Current device result:

```text
M4 SSH RUNNER: PASS
```

# M5: Terminal Channel

M5 implemented terminal transport and replay behavior.

Primary components:

```text
termbridge/frames.py
termbridge/replay.py
termbridge/pty_bridge.py
termbridge/viewer.py
web/ws_term.py
```

Verified behaviors include:

- Terminal frame schema
- Replay behavior
- PTY bridging
- Resize handling
- Viewer sessions
- WebSocket backpressure
- Event replay

Current device result:

```text
M5 TERMINAL CHANNEL: PASS
```

# M6: Filesystem and Policy

M6 established safe filesystem operations and execution policy.

Primary components:

```text
fsguard/canon.py
fsguard/safeio.py
fsguard/atomic.py
fsguard/backups.py
fsguard/trash.py
policy/capabilities.py
policy/profiles.py
policy/classify.py
policy/approvals.py
policy/hard_deny.py
policy/v1.py
```

Verified behaviors include:

- Canonical path handling
- Symlink-escape prevention
- Safe reads and writes
- Atomic replacement
- Backups and trash behavior
- Capability classification
- Approval handling
- Hard-deny enforcement
- Prompt-injection resistance in tested policy paths

Current device result:

```text
M6 FILESYSTEM/POLICY: PASS
```

# M7: Model and Agent Runtime

M7 connected model providers to the agent execution loop.

Primary components:

```text
models/base.py
models/caps.py
models/openai_compat.py
models/llamacpp.py
models/ollama.py
models/fallback.py
models/tooljson.py
agent/tasks.py
agent/prompt.py
agent/plan.py
agent/engine.py
agent/completion.py
agent/compaction.py
agent/compaction_v2.py
agent/ownership.py
```

Verified behaviors include:

- Provider abstraction
- Capability reporting
- Tool JSON handling
- Provider fallback
- Prompt zoning
- Planning and completion
- Context compaction
- Tool approval and denial
- Scripted model tests
- Invalid model-tool fault handling

Current device result:

```text
M7 MODEL/AGENT: PASS
```

# M8: Integrated MVP Core

M8 combined the earlier milestones into an installable MVP runtime.

Verified areas include:

- Core startup path
- Session state and manifests
- Runtime directory creation
- Private tmux integration
- Loopback web service
- Installer safety
- Uninstall behavior
- SM-T870 physical-device execution

Current device result:

```text
M8 SM-T870 MVP CORE: PASS
M8 INSTALLER SAFETY: PASS
```

# M9: UI Areas

M9 established the browser UI structure and panel ownership.

Primary frontend and web components:

```text
frontend/src/main.js
frontend/src/components/models.js
frontend/src/components/v1_panels.js
web/static/index.html
web/static/main.js
web/static/agent.js
web/static/diff.js
web/static/styles.css
web/routes_state.py
web/routes_approvals.py
web/ws_events.py
web/ws_term.py
```

Verified areas include:

- Operational panels
- Model-related UI areas
- State rendering
- Approval routes
- Event and terminal WebSockets
- M9 section ownership

Current device result:

```text
M9 UI AREAS: PASS
```

# M10: Control and YOLO Mode

M10 implemented controlled execution modes while preserving policy boundaries.

Verified behavior includes:

- Control markers
- Ownership rules
- Explicit high-autonomy mode selection
- Approval integration
- Hard-deny preservation
- UI and state representation

Current device result:

```text
M10 YOLO/CONTROL: PASS
```

# M11: Worktrees and Audit Bundles

M11 added Git-safe worktree operations and portable evidence bundles.

Primary components:

```text
gitsafe/baseline.py
gitsafe/diff.py
gitsafe/run.py
gitsafe/snapshot.py
gitsafe/worktree.py
audit/writer.py
audit/verify.py
audit/bundle.py
```

Verified behavior includes:

- Clean baseline capture
- Dirty-tree preservation
- Malicious Git configuration handling
- Worktree creation
- Snapshot creation
- Audit chaining
- Bundle creation and verification

Current device result:

```text
M11 WORKTREE/BUNDLE: PASS
```

# M12: Providers and Context

M12 expanded provider selection and context behavior.

Verified behavior includes:

- Provider capability handling
- Fallback selection
- Missing-endpoint degradation
- Context and profile matrices
- Continued operation with accepted provider deferrals

Current device result:

```text
M12 PROVIDERS: PASS
```

# M13: Upgrade and Rollback

M13 implemented upgrade and rollback safety.

Primary components:

```text
core/releases.py
store/db.py
store/migrations/
docs/upgrade.md
```

Verified behavior includes:

- Release markers
- Store migration
- Live marker handling
- Release flip
- Upgrade validation
- Rollback behavior
- Preservation of user and Git state

Current device result:

```text
M13 UPGRADE/ROLLBACK: PASS
```

# M14: Readiness and v1 Gate

M14 established final readiness controls and the v1 gate.

Verified behavior includes:

- Runtime resource budgets
- Final readiness checks
- Audit integrity
- Recovery behavior
- v1 gate enforcement
- RC2 live-start compatibility

Current device results:

```text
M14 READINESS: PASS
RC2 LIVE START: PASS
```

# Android Companion

The Android companion is located under `android/`.

Primary components:

```text
MainActivity.kt
TermuxContract.kt
TermuxLauncher.kt
TermuxResultReceiver.kt
```

The companion launches the Termux-side runtime while preserving the Termux process and filesystem boundaries. Android work remains separate from core lifecycle hardening unless explicitly declared in milestone scope.

# Runtime Lifecycle

The runtime uses explicit session states:

```text
CREATED
STARTING
READY
STOPPING
STOPPED
ORPHANED
FAILED
```

Current lifecycle invariants include:

- Same-state transitions are no-ops
- Illegal transitions fail
- `STOPPED` remains terminal except for repeated `STOPPED`
- `FAILED` and `ORPHANED` have explicit recovery paths
- State writes use atomic replacement
- Lock ownership uses PID plus Linux process-start identity

# Security Model

## Default Execution

The default runtime is non-root.

Privilege escalation is limited to the individual operation that requires it. The intended order is:

```text
normal Termux execution
sudo -n
tsu
su -c
explicit failure when root is unavailable
```

The application must not run globally as root merely because root access is available.

## Network Boundary

- Web services bind to loopback
- Control sockets are private Unix sockets
- Runtime directories use private permissions
- Authentication and CSP controls are applied in the web subsystem

## Filesystem Boundary

- Workspace paths are validated
- Unix socket path lengths are checked
- Symlink escapes are rejected
- State writes are atomic
- Sensitive context is redacted
- Backups and trash operations are explicit

## Policy Boundary

- Capabilities are classified
- Profiles determine allowed operations
- High-impact operations require approval
- Hard-denied operations remain denied in high-autonomy modes
- Tool envelopes and schemas are validated

# Testing

## Full Python Regression

```bash
PY="$PWD/.m0-venv/bin/python"

"$PY" -m pytest -q \
  tests/unit \
  tests/integration \
  tests/fault
```

Current result:

```text
124 passed
```

## Full Device Suite

```bash
for test_script in tests/device/test_*.sh; do
  bash "$test_script"
done
```

Current result:

```text
M1 through M14: PASS
RC2 live start: PASS
```

## M2 Targeted Tests

```bash
"$PY" -m pytest -q \
  tests/unit/test_lifecycle.py \
  tests/unit/test_daemon_lock.py \
  tests/unit/test_ports.py \
  tests/integration/test_stale_pid.py \
  tests/integration/test_port_conflict.py \
  tests/integration/test_dry_run.py
```

Current result:

```text
14 passed
```

# Evidence and Documentation

Key documentation:

```text
docs/decisions/                         Accepted ADRs
docs/milestones/M1-KICKOFF-CHECKLIST.md M1 entry gate
docs/milestones/ACCEPTED-ADR-SUMMARY.md Accepted ADR summary
docs/milestones/M1-M2-HANDOFF.md        Verified handoff record
docs/milestones/M2-IMPLEMENTATION-SCOPE.md
docs/milestones/M2-ACCEPTANCE-TESTS.md
docs/spike-results/                     M00 evidence and device results
docs/review/threat-model-checklist.md   Security review support
```

Historical milestone and checkpoint files are evidence records. Do not rewrite or delete them during unrelated implementation work.

# Checkpoints

## M1 External Checkpoint

```text
~/tmux-code-agent/checkpoints/m1-20261024T155447Z/
```

Contents:

```text
BRANCH-RELATIONSHIP.txt
M1-CHECKPOINT-MANIFEST.txt
M1-FULL-SUITE-LOG.sha256
SHA256SUMS
tmux-code-agent-m1-source.tar.gz
tmux-code-agent-m1.bundle
```

## Historical Internal Checkpoints

Historical archives are retained under:

```text
docs/milestones/checkpoints/
```

These are milestone evidence, not working directories.

# Release Boundaries

## RC1

RC1 is frozen and immutable.

```text
RC1 source commit:
87eb3f1a297715e400b9dbd16f97feccce12f5f9

RC1 annotated tag object:
749f15cf096f892c500bf75ae45ac3ed106994ee
```

Verify the archive:

```bash
sha256sum -c \
  dist/tmux-code-agent-v1.0.0-rc1.tar.gz.sha256
```

Do not rebuild, replace, or edit RC1 artifacts. Any archive-content change requires a new release identity.

## RC2

RC2 includes the Android companion and live-start work.

Artifacts are stored under:

```text
dist/
dist/github-rc2/
```

## Validated M2 Baseline

```text
Branch:
m2

HEAD:
65524e9e1ed46b4059d45b1470acb1c60d8ccf67

Outer baseline gate:
65524e9e1ed46b4059d45b1470acb1c60d8ccf67
```

# Operational Notes

Files under `~/tmux-code-agent/archive/` belong to the outer maintenance workspace and are not part of this Git repository.

## Python Caches

`__pycache__`, `.pyc`, and `.pyo` files are ignored generated content. They may be removed outside `.m0-venv` without changing repository state, but Python and pytest will recreate them.

## Git Integrity

A dangling blob may be reported:

```text
97595cba85b0bd7a49408fe5891924e2b5114bb6
```

It is unreachable historical content from a discarded Markdown revision. Repository integrity remains valid when `git fsck` exits with `0`.

## Storage

Checkpoint archives are intentionally retained and may consume significant storage. Do not delete them as part of normal implementation cleanup.

# Quick Validation

Run from the repository root:

```bash
PY="$PWD/.m0-venv/bin/python"

"$PY" -m pytest -q tests/unit tests/integration tests/fault

for test_script in tests/device/test_*.sh; do
  bash "$test_script"
done

git diff --check
git fsck --no-progress

sha256sum -c \
  dist/tmux-code-agent-v1.0.0-rc1.tar.gz.sha256
```

Expected current result:

```text
124 Python tests passed
All device gates passed
RC2 live start passed
Repository clean
Git integrity passed
RC1 archive verified
```

# Development Controls

- Work only within the declared milestone scope
- Add tests before or with behavior changes
- Run targeted tests after each bounded change
- Run dependent device gates when shared behavior changes
- Run the complete regression suite before a milestone completion commit
- Preserve accepted ADRs
- Preserve historical evidence
- Keep non-root execution as the default
- Escalate only the individual command requiring privileges
- Keep release packaging separate from implementation commits
- Never modify RC1 artifacts

# Current Next Work

The next bounded M2 slice is expected to address:

- Atomic heartbeat writing
- Heartbeat parsing and freshness classification
- Control-socket cleanup
- Daemon cleanup when startup partially fails
- Lock release during all shutdown paths
- Device validation that shutdown removes live runtime ownership artifacts

This work should remain separate from CLI lifecycle expansion, Android companion changes, release packaging, and historical evidence cleanup.
