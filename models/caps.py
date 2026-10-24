from models.base import Caps
def usable(caps:Caps)->bool:return caps.context_tokens>=4096 and caps.tool_mode in {'native_tools','json_action'}
