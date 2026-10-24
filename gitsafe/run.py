import os,subprocess
BASE=['git','--no-optional-locks','-c','core.fsmonitor=false','-c','core.hooksPath=/dev/null','-c','core.pager=cat','-c','protocol.ext.allow=never','-c','diff.external=']
def git(workspace,*args,check=True):
 env={**os.environ,'GIT_TERMINAL_PROMPT':'0','GIT_OPTIONAL_LOCKS':'0'}
 return subprocess.run([*BASE,'-C',str(workspace),*args],text=True,capture_output=True,check=check,env=env)
