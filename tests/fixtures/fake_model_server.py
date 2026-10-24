from __future__ import annotations
import argparse,json
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
SCRIPT=[]
class H(BaseHTTPRequestHandler):
 def log_message(self,*a):pass
 def _send(self,obj):b=json.dumps(obj).encode();self.send_response(200);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(b)));self.end_headers();self.wfile.write(b)
 def do_GET(self):
  if self.path.endswith('/models'):self._send({'data':[{'id':'fake-model'}]})
  else:self.send_error(404)
 def do_POST(self):
  n=int(self.headers.get('Content-Length','0'));self.rfile.read(n);action=SCRIPT.pop(0) if SCRIPT else {'tool':'finish','args':{'summary':'done','claims':[]}};self._send({'choices':[{'message':{'role':'assistant','content':None,'tool_calls':[{'id':'c','type':'function','function':{'name':action['tool'],'arguments':json.dumps(action['args'])}}]}}]})
def main():
 p=argparse.ArgumentParser();p.add_argument('--port',type=int,required=True);p.add_argument('--script');a=p.parse_args();
 if a.script:SCRIPT.extend(json.loads(a.script))
 ThreadingHTTPServer(('127.0.0.1',a.port),H).serve_forever()
if __name__=='__main__':main()
