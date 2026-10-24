def ok(data=None,**extra):return {'ok':True,'data':data,**extra}
def error(code,message,hint=None):return {'ok':False,'error':{'code':code,'message':message,'hint':hint}}
