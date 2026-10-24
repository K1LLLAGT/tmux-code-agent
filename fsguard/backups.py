from pathlib import Path
def backup_once(source:Path,workspace:Path,backup_root:Path)->Path|None:
 if not source.exists():return None
 rel=source.resolve().relative_to(workspace.resolve());dest=backup_root/rel
 if not dest.exists():dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(source.read_bytes())
 return dest
