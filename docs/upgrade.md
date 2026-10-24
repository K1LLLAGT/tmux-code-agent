# Upgrade and rollback
Releases are installed side by side. The `current` symlink is atomically flipped only after the new release is ready. Existing daemons retain their loaded code. Rollback flips `current` to the selected retained release.
