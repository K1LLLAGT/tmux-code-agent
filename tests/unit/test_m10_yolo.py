from policy.v1 import yolo_grants_root,root_enabled
def test_yolo_never_root():assert not yolo_grants_root() and not root_enabled(True,True,False)
