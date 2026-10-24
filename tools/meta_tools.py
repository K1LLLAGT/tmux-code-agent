def update_plan(steps):return {'ok':True,'data':{'steps':list(steps)}}
def ask_user(question):return {'ok':True,'data':{'question':question}}
def finish(summary,claims=None):return {'ok':True,'data':{'summary':summary,'claims':claims or []}}
