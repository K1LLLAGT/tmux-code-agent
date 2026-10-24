def assemble(system_policy,user_task,project_map,tool_results,model_output=''):
 return [
 {'role':'system','content':system_policy},
 {'role':'user','content':user_task},
 {'role':'user','content':'<project_map untrusted="true">'+project_map+'</project_map>'},
 *[{'role':'user','content':f'<tool_result id="{i}" tool="{r.get("tool","")}" untrusted="true">{r.get("text","")}</tool_result>'} for i,r in enumerate(tool_results,1)],
 *([{'role':'assistant','content':model_output}] if model_output else [])]
