# Post-V1 Change Log

## Frozen V1 Development Baseline

Checkpoint:
`v1-complete.20261024T065419Z.tar.gz`

SHA-256:
`251a28b2e9666202442828804dc6b4ba3de4bd515d27b5618b4ec356d9aeddf6`

The frozen V1 checkpoint is immutable. All subsequent changes must be represented by new checkpoints.

## V1 Release-Candidate Packaging

### Findings

- Final V1 checkpoint passed SHA-256 verification.
- Sensitive/runtime filename scan found no obvious exposed credentials.
- Archive contains Python cache artifacts.
- Archive contains historical development and evidence artifacts.
- V1 archive omits application files present in M8.
- Result documents occur more than once in some checkpoint archives.

### Required release cleanup

- Include all required cumulative application modules.
- Exclude `__pycache__/`.
- Exclude `*.pyc`.
- Remove duplicate archive members.
- Separate historical checkpoints from distributable files.
- Generate an explicit release manifest.
- Verify the release archive independently.

## Post-V1 Changes

### YYYY-MM-DD - Change title

Category:
Fix | Security | Feature | Refactor | Performance | Documentation | Build

Files:
- ...

Reason:
- ...

Behavior before:
- ...

Behavior after:
- ...

Tests:
- Regression: ...
- Device: ...
- Security: ...

Compatibility:
- ...

Rollback:
- V1 baseline or subsequent checkpoint

Checkpoint:
- ...

SHA-256:
- ...
