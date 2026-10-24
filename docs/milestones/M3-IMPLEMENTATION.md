# M3 Implementation
- Private `tmux -S <runtime>/tmux.sock` only.
- New server starts from a minimal allowlisted environment.
- Windows `user`, `agent`, `logs` are separate.
- Persistent registry data is derived from authoritative `list-panes`, not screen scraping.
- Control mode is a hint channel; polling remains a fallback.
- Existing private server can be adopted after supervisor/backend restart.
