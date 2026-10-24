# M1 Implementation

M1 implements invocation context capture, environment allowlisting and redaction,
Git facts, immutable launch manifests, atomic mutable state, strict configuration,
the CLI launcher shim, and `start --dry-run`.

## Session safety
- Session IDs are full 128-bit lowercase hex values; short IDs are display/runtime labels only.
- TCA-owned state and per-session runtime directories are mode 0700.
- Manifest is exclusive-create and mode 0400.
- Mutable state is atomically replaced and mode 0600.
- HOME and filesystem-root workspaces require explicit overrides.

## Privacy
Only allowlisted environment facts are captured. Secret-like names are excluded.
Known secret values and common authorization/private-key text can be scrubbed before rendering.

## M1 acceptance command

```sh
./tmux-code-agent start --dry-run --json
```
