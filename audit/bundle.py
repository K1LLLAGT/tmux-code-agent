import re,tarfile
from pathlib import Path
KEY=re.compile(r'(BEGIN [A-Z ]*PRIVATE KEY|ssh-ed25519\s+[A-Za-z0-9+/=]{40,}|github_pat_|ghp_)')
def safe_bundle(paths:list[Path],out:Path):
 for p in paths:
  if p.is_file() and KEY.search(p.read_text(errors='ignore')):raise ValueError('bundle leak scan failed')
 with tarfile.open(out,'w:gz') as t:
  for p in paths:t.add(p,arcname=p.name)
 return out
