from __future__ import annotations
from starlette.applications import Starlette
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import HTMLResponse,JSONResponse,RedirectResponse
from starlette.routing import Route
from web.auth import AuthState
from web.csp import SECURITY_HEADERS
from web.routes_state import health,state

class SecurityMiddleware(BaseHTTPMiddleware):
 async def dispatch(self,request:Request,call_next):
  host=request.headers.get('host','').split(':')[0]
  if host not in {'127.0.0.1','localhost'}:return JSONResponse({'error':'bad_host'},status_code=400)
  origin=request.headers.get('origin')
  if origin and not (origin.startswith('http://127.0.0.1:') or origin.startswith('http://localhost:')):return JSONResponse({'error':'bad_origin'},status_code=403)
  if request.method not in {'GET','HEAD','OPTIONS'} and request.url.path!='/bootstrap/claim':
   sid=request.cookies.get('tca_session'); expected=request.app.state.auth.csrf(sid)
   if not expected or request.headers.get('x-csrf-token')!=expected:return JSONResponse({'error':'csrf'},status_code=403)
  response=await call_next(request)
  for k,v in SECURITY_HEADERS.items():response.headers[k]=v
  return response

async def claim(request:Request):
 token=(await request.json()).get('token','')
 result=request.app.state.auth.claim(token)
 if not result:return JSONResponse({'error':'invalid_bootstrap'},status_code=403)
 sid,csrf=result; r=JSONResponse({'ok':True,'csrf':csrf}); r.set_cookie('tca_session',sid,httponly=True,samesite='strict'); return r
async def index(request):return HTMLResponse('<!doctype html><title>TCA</title><h1>TMUX CODE AGENT</h1>')

def create_app(status='READY'):
 app=Starlette(routes=[Route('/',index),Route('/health',health),Route('/api/state',state),Route('/bootstrap/claim',claim,methods=['POST'])])
 app.state.auth=AuthState(); app.state.status=status; app.state.components={'backend':'READY'}; app.add_middleware(SecurityMiddleware); return app
