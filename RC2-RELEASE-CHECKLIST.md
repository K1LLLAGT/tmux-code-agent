# tmux-code-agent v1.0.0-rc2 Release Checklist

## Immutable RC1 baseline
- [x] RC1 source tag: `v1.0.0-rc1-source`
- [x] RC1 source commit: `87eb3f1a297715e400b9dbd16f97feccce12f5f9`
- [x] RC1 annotated tag object: `749f15cf096f892c500bf75ae45ac3ed106994ee`
- [x] Post-RC1 main baseline: `996a0d6269e4f668d14a226f796d5783353444a6`
- [x] RC1 distribution SHA-256: `2c8bfdac4fa9ab001aca67551c7410f3cfdcf90f196d18b2bc78db99d04da44c`
- [x] V1 development rollback SHA-256: `251a28b2e9666202442828804dc6b4ba3de4bd515d27b5618b4ec356d9aeddf6`
- [ ] Confirm RC1 archive is still byte-for-byte unchanged before RC2 packaging

## RC2 starting state
- [ ] Working tree clean before first RC2 code change
- [ ] Baseline test suite passes
- [ ] RC1 identity checks pass
- [ ] RC2 changes recorded in `POST-V1-CHANGELOG.md`

## RC2 changes
- [ ] Reason documented
- [ ] Files changed recorded
- [ ] Behavior before/after recorded
- [ ] Security impact reviewed
- [ ] Compatibility impact reviewed
- [ ] Tests added or updated where needed

## Regression
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Fault tests pass
- [ ] Device tests pass as applicable
- [ ] No unexpected failures/skips

## Packaging
- [ ] Build `tmux-code-agent-v1.0.0-rc2.tar.gz`
- [ ] Do not overwrite RC1
- [ ] No `__pycache__/`, `*.pyc`, `*.pyo`
- [ ] No `*.pre-*`, `*.previous`, `*.disabled`
- [ ] No historical checkpoint archives
- [ ] No duplicate archive members
- [ ] No sensitive/runtime artifacts
- [ ] Required cumulative application files present

## RC1 vs RC2 comparison
- [ ] Added files reviewed
- [ ] Removed files reviewed
- [ ] Modified files reviewed
- [ ] No unexplained differences
- [ ] Release notes match actual differences

## RC2 integrity
- [ ] Sorted inventory generated
- [ ] Per-file SHA-256 manifest generated
- [ ] Archive SHA-256 generated
- [ ] `gzip -t` passes
- [ ] Extracted manifest verification passes
- [ ] Duplicate scan passes
- [ ] Sensitive-name/content scans pass

## Installation
- [ ] Isolated `install.sh --dry-run` passes
- [ ] Isolated install passes
- [ ] Installation target verified
- [ ] Project sentinel preserved
- [ ] `~/.ssh` sentinel preserved
- [ ] Isolated uninstall passes

## RC2 source identity
- [ ] Final RC2 source committed
- [ ] Working tree clean
- [ ] Annotated tag `v1.0.0-rc2-source` created
- [ ] Tag resolves to intended commit

RC2 source commit: `<fill after freeze>`
RC2 tag object: `<fill after freeze>`
RC2 distribution SHA-256: `<fill after build>`

## Final decision
- [ ] RC2 release notes complete
- [ ] RC2 identity record complete
- [ ] RC1 remains independently verifiable
- [ ] RC2 independently verifiable
- [ ] GO
- [ ] NO-GO
