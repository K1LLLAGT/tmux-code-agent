from pathlib import Path
from tmuxctl.panes import registry
def poll_registry(socket:Path):return registry(socket)
