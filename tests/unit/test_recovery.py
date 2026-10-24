from supervisor.recovery import classify
def test_resume_matrix_core():assert classify(True,True)=='ALIVE' and classify(False,True)=='ORPHANED' and classify(False,False)=='STOPPED'
