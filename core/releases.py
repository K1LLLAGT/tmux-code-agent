from pathlib import Path
def flip(root:Path,version:str):
 target=root/'releases'/version
 if not target.exists():raise FileNotFoundError(target)
 link=root/'current';tmp=root/'current.new';tmp.unlink(missing_ok=True);tmp.symlink_to(target);tmp.replace(link);return target
def rollback(root:Path,version:str):return flip(root,version)
