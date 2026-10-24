# tmux-code-agent Milestone 0: Q01-Q14

This corrected M0 tree implements the feasibility gate from the consolidated master design. It replaces the earlier Q01-Q08 package. It collects evidence only; it does not begin Milestone 1.

## Exact backup and replacement commands

```bash
cd ~/tmux-code-agent
stamp="$(date -u +%Y%m%dT%H%M%SZ)"
old='tmux-code-agent-milestone-0'
backup="${old}.pre-q01-q14.${stamp}.tar.gz"

tar --numeric-owner -czf "$backup" "$old"
gzip -t "$backup"
tar -tzf "$backup" >/dev/null
sha256sum "$backup" | tee "${backup}.sha256"

mv "$old" "${old}.pre-q01-q14.${stamp}"
mv tmux-code-agent-milestone-0-q01-q14 "$old"
find "$old" -type d -name __pycache__ -prune -exec rm -rf {} +
find "$old" -type f -name '*.pyc' -delete
chmod -R u+rwX,go-rwx "$old"
```

Run:

```bash
cd ~/tmux-code-agent/tmux-code-agent-milestone-0
./scripts/spike/run-all.sh
python ./scripts/spike/validate-results.py docs/spike-results/*.jsonl
```
