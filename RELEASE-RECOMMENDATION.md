# V1 Release Recommendation

## Summary

The verified V1 development checkpoint is a known-good rollback artifact, but it is not a clean distribution archive.

### Frozen development baseline

- Checkpoint: `v1-complete.20261024T065419Z.tar.gz`
- SHA-256: `251a28b2e9666202442828804dc6b4ba3de4bd515d27b5618b4ec356d9aeddf6`
- Policy: immutable

```text
V1 development checkpoint
        !=
V1 distribution/release archive
```

## Archive comparison findings

| Archive | Inventory entries |
|---|---:|
| M8 | 253 |
| M14 | 580 |
| V1 | 583 |

### Positive findings

- The V1 archive contains the expected post-M8 agent, model, frontend, worktree, bundle, release and V1 milestone additions.
- The runtime-sensitive filename scan found no obvious private keys, authorization files, session nonces, cookies, tokens or sshd logs.
- M14 and V1 checkpoint SHA-256 verification passed independently.

### Packaging defects found

The V1 archive was not a complete cumulative application package. These M8 application components were absent:

- `cli/doctor.py`
- `install.sh`
- `uninstall.sh`
- `store/`
- `store/db.py`
- `store/migrations/0001_init.sql`
- `supervisor/recovery.py`
- `tools/git_tools.py`
- `web/static/diff.js`

Other cleanup findings:

- Duplicate result members occurred because `docs/` and the result file were both passed to `tar`.
- Python cache directories and compiled bytecode were included.
- Historical checkpoints, old results, pre-fix files, disabled files and failure evidence were bundled.
- `scripts/soak-v1.sh` remained in the archive after its completion gate was removed.

## Recommendation

Keep the existing V1 checkpoint unchanged as the development rollback boundary. Build a separate curated release candidate from the verified working tree.

The release candidate must:

1. Include all cumulative runtime application components.
2. Exclude Python caches and bytecode.
3. Avoid duplicate archive members.
4. Exclude historical checkpoints, failed-run evidence and pre-fix files.
5. Include an explicit sorted inventory and SHA-256 manifest.
6. Pass extraction, sensitive-name scanning, regression and device smoke validation.

Sanity requirement:

```text
V1 release application files
        >=
M8 application files
```

The initial curated artifact is:

```text
tmux-code-agent-v1.0.0-rc1.tar.gz
```
