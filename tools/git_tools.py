from gitsafe.run import git
def git_status(workspace):return {'ok':True,'data':git(workspace,'status','--porcelain=v2','--branch').stdout}
def git_diff(workspace):return {'ok':True,'data':git(workspace,'diff','--no-ext-diff').stdout}
def git_log(workspace,n=20):return {'ok':True,'data':git(workspace,'log',f'-n{int(n)}','--oneline').stdout}
