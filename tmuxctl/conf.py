from pathlib import Path
CONFIG='''set -g prefix None\nset -g status off\nset -g history-limit 10000\nset -g remain-on-exit on\nset -g allow-rename off\nset -g set-titles off\n'''
def write_config(path:Path)->Path:
 path.parent.mkdir(parents=True,exist_ok=True);path.write_text(CONFIG);path.chmod(0o600);return path
