from pathlib import Path
from gitsafe.run import git
def shadow_snapshot(workspace:Path,index:Path,ref:str):
 import os
 env={**os.environ,'GIT_INDEX_FILE':str(index),'GIT_TERMINAL_PROMPT':'0'}
 # deterministic plumbing only; caller decides whether to persist the ref
 return git(workspace,'write-tree',check=False).stdout.strip()
