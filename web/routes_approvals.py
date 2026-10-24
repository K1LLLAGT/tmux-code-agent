from starlette.responses import JSONResponse
async def approval_decision(request):
 body=await request.json();decision=body.get('decision')
 if decision not in {'deny','once','task'}:return JSONResponse({'error':'invalid_decision'},status_code=400)
 return JSONResponse({'ok':True,'decision':decision})
