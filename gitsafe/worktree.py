import subprocess
from pathlib import Path
def should_offer(dirty:bool)->bool:return dirty
def create(repo:Path,dest:Path,branch:str):subprocess.run(['git','-C',str(repo),'worktree','add','--detach',str(dest)],check=True);subprocess.run(['git','-C',str(dest),'switch','-c',branch],check=True)
def export_patch(repo:Path,out:Path):out.write_text(subprocess.run(['git','-C',str(repo),'diff','--binary'],text=True,capture_output=True,check=True).stdout);return out
def apply_checked(workspace:Path,patch:Path):
 check=subprocess.run(['git','-C',str(workspace),'apply','--check',str(patch)],capture_output=True)
 if check.returncode:return False
 return subprocess.run(['git','-C',str(workspace),'apply',str(patch)]).returncode==0
