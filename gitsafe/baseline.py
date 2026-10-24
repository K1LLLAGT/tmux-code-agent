import hashlib
from pathlib import Path
from gitsafe.run import git
def file_hash(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def capture(workspace:Path):
 p=git(workspace,'status','--porcelain=v2','-z','--branch');head=git(workspace,'rev-parse','HEAD',check=False).stdout.strip();files={}
 for x in workspace.rglob('*'):
  if x.is_file() and '.git' not in x.parts:files[str(x.relative_to(workspace))]=file_hash(x)
 return {'status':p.stdout,'head':head,'files':files}
