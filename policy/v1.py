def yolo_capabilities():return {'fs.write.workspace','shell.execute','shell.install','git.write','network.local'}
def yolo_grants_root():return False
def root_enabled(detected:bool,explicit:bool,typed:bool)->bool:return detected and explicit and typed
