# tmux-code-agent V1 Release Checklist

## Frozen baseline

- [x] V1 development checkpoint exists
- [x] V1 SHA-256 exists
- [x] V1 SHA-256 independently verifies
- [x] M14 checkpoint independently verifies
- [ ] Frozen archive remains unmodified

## Regression

- [x] Final cumulative suite passed
- [x] M14 readiness passed
- [x] V1 result reports PASS
- [ ] Extracted RC regression suite passes
- [ ] Extracted RC SM-T870 smoke passes

## Security packaging scan

- [x] No obvious private-key filenames found
- [x] No `authorized_keys` found
- [x] No `known_hosts` found
- [x] No `auth.json` found
- [x] No `session.nonce` found
- [x] No `sshd.log` found
- [ ] RC sensitive-content scan passes

## Release archive cleanliness

- [ ] No `__pycache__/`
- [ ] No `*.pyc`
- [ ] No duplicate members
- [ ] No `*.pre-*`
- [ ] No `*.previous`
- [ ] No `*.disabled`
- [ ] No historical failure evidence
- [ ] No old milestone checkpoint archives
- [ ] Historical documentation inclusion reviewed

## Cumulative content

- [ ] `cli/doctor.py` included
- [ ] `install.sh` included
- [ ] `uninstall.sh` included
- [ ] `store/` included
- [ ] `supervisor/recovery.py` included
- [ ] `tools/git_tools.py` included
- [ ] `web/static/diff.js` included

## Release build

- [ ] Build separate V1 RC1 archive
- [ ] Generate sorted inventory
- [ ] Generate content SHA-256 manifest
- [ ] Generate archive SHA-256
- [ ] Verify archive SHA-256
- [ ] Test archive extraction
- [ ] Run release from extracted tree
- [ ] Compare required M8 application paths

## Documentation

- [ ] `RELEASE-RECOMMENDATION.md` included
- [ ] `POST-V1-CHANGELOG.md` included
- [ ] `V1-RELEASE-CHECKLIST.md` included
- [ ] README current
- [ ] Installation documented
- [ ] CLI documented
- [ ] Security boundary documented
- [ ] Upgrade and rollback documented
- [ ] Known limitations documented

## Final decision

- [ ] RC contents reviewed
- [ ] Release notes finalized
- [ ] Final release SHA-256 frozen
- [ ] GO
- [ ] NO-GO

Signed:

Date:
