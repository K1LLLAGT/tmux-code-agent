import json
class ToolJSONError(ValueError):pass
def parse_action(text:str)->dict:
 try:value=json.loads(text)
 except json.JSONDecodeError as e:raise ToolJSONError(str(e)) from e
 if not isinstance(value,dict) or set(value)!={'tool','args'} or not isinstance(value['tool'],str) or not isinstance(value['args'],dict):raise ToolJSONError('expected exactly {tool,args}')
 return value
