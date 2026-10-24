from pathlib import Path
def classify(daemon_alive:bool,tmux_alive:bool,manifest_exists=True):
 if daemon_alive:return 'ALIVE'
 if tmux_alive:return 'ORPHANED'
 if manifest_exists:return 'STOPPED'
 return 'MISSING'
def recover_result(command_dir:Path):
 p=command_dir/'result.json';return p.read_text() if p.exists() else None
