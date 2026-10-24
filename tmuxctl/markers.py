import secrets,re
class Markers:
 def __init__(self,nonce=None):self.nonce=nonce or secrets.token_hex(16)
 def pair(self,cmdid):return f'TCA_S{self.nonce}_{cmdid}',f'TCA_E{self.nonce}_{cmdid}'
 def parse(self,text,cmdid):
  s,e=self.pair(cmdid);m=re.search(rf'(?m)^{re.escape(s)}\n(.*?)^{re.escape(e)}_(\d+)\s*$',text,re.S);return None if not m else (m.group(1),int(m.group(2)))
