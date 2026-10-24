from starlette.responses import JSONResponse
async def health(request):return JSONResponse({'ok':True,'status':request.app.state.status})
async def state(request):return JSONResponse({'status':request.app.state.status,'components':request.app.state.components})
