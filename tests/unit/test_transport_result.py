from transport.result import ExecResult
def test_result_shape():
 r=ExecResult('c',['true'],'/w',0,None,False,False,'','','','',0,0,'/l');assert r.as_dict()['exit_code']==0
