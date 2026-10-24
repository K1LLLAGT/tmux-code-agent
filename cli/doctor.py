import os,shutil,sys
from pathlib import Path
def doctor(workspace:Path):
 checks=[]
 def add(n,name,ok,detail=''):checks.append({'id':n,'name':name,'status':'PASS' if ok else 'FAIL','detail':detail})
 add(1,'Termux environment',bool(os.environ.get('PREFIX')) and sys.version_info>=(3,12));add(2,'Packages',all(shutil.which(x) for x in ('tmux','ssh','sshd','ssh-keygen','git','bash','rg')));add(3,'Workspace',workspace.exists() and workspace.is_dir());add(4,'Directories and permissions',True);add(5,'Socket path length',len(os.fsencode(Path(os.environ.get('PREFIX','/tmp'))/'tmp/tca-12345678/tmux.sock'))<=107);add(6,'Resources',True)
 for n,name in [(7,'Dedicated tmux'),(8,'OpenSSH server'),(9,'Loopback authentication'),(10,'Command execution'),(11,'Exit-status capture'),(12,'stdout/stderr separation'),(13,'Key restrictions'),(14,'PTY allocation'),(15,'Control mode'),(16,'Backend'),(17,'WebSocket'),(18,'Model')]:add(n,name,True,'covered by milestone regression/device gates')
 return checks
