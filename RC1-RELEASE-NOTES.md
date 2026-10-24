# tmux-code-agent v1.0.0-rc1 Release Notes

## Release candidate

`v1.0.0-rc1` is the first curated distribution candidate built from the verified V1 development baseline.

### Artifact

- Archive: `tmux-code-agent-v1.0.0-rc1.tar.gz`
- SHA-256: `2c8bfdac4fa9ab001aca67551c7410f3cfdcf90f196d18b2bc78db99d04da44c`
- Curated inventory: 151 entries

## Highlights

- Private tmux session infrastructure and terminal channel.
- Loopback SSH transport with restricted keys and structured command execution.
- Policy, capability and approval plumbing.
- Workspace filesystem guards, atomic writes and stale-write protection.
- Model-provider and agent-loop plumbing.
- Git safety, audit, persistence and recovery components.
- Mobile-oriented frontend shell with Agent, Terminal, Files, Editor, Git, Activity and Settings areas.
- Worktree, diagnostic-bundle, native-provider and release/rollback components added across the V1 milestones.

## RC1 packaging cleanup

RC1 is intentionally separate from the larger V1 development checkpoint. The release candidate:

- restores cumulative application files that were absent from the earlier V1 checkpoint package;
- excludes Python cache and bytecode artifacts;
- excludes pre-fix, previous and disabled development files;
- avoids duplicate archive members;
- excludes historical milestone checkpoint archives from the distribution payload;
- includes a sorted file inventory and per-file SHA-256 manifest;
- is extracted and verified against that manifest by the RC builder.

## Verified cumulative components

The curated package includes the previously missing cumulative runtime files, including:

- `cli/doctor.py`
- `install.sh`
- `uninstall.sh`
- `store/db.py`
- `store/migrations/0001_init.sql`
- `supervisor/recovery.py`
- `tools/git_tools.py`
- `web/static/diff.js`

## Integrity status

The RC builder reported:

- archive SHA-256 verification: PASS;
- extracted per-file manifest verification: PASS;
- gzip integrity: PASS;
- duplicate-member check: PASS;
- development-residue scan: PASS;
- sensitive/runtime artifact scan: PASS.

## Baselines

Frozen development rollback checkpoint:

`v1-complete.20261024T065419Z.tar.gz`

SHA-256:

`251a28b2e9666202442828804dc6b4ba3de4bd515d27b5618b4ec356d9aeddf6`

Curated RC1 distribution:

`tmux-code-agent-v1.0.0-rc1.tar.gz`

SHA-256:

`2c8bfdac4fa9ab001aca67551c7410f3cfdcf90f196d18b2bc78db99d04da44c`

## Release-candidate policy

RC1 should remain immutable after final verification. Any packaging or code correction should produce a new RC rather than modifying this archive in place.
