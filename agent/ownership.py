class PaneOwned(ValueError):pass
class Ownership:
 def __init__(self):self.owner={'user':'user','agent':'agent','logs':'none'}
 def take(self):self.owner['agent']='user'
 def release(self):self.owner['agent']='agent'
 def agent_write(self,window):
  if window!='agent' or self.owner.get(window)!='agent':raise PaneOwned('ERR_PANE_OWNED_BY_USER')
  return True
