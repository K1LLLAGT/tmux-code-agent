from termbridge.frames import data_frame,control_frame
from web.ws_term import handle_client_frame
class P:
 def __init__(self):self.data=b'';self.size=None
 def write(self,d):self.data+=d
 def resize(self,c,r):self.size=(c,r)
def test_controls():
 p=P();assert handle_client_frame(data_frame(b'x'),p)=='data';assert p.data==b'x';assert handle_client_frame(control_frame({'type':'resize','cols':80,'rows':24}),p)=='resize';assert p.size==(80,24)
