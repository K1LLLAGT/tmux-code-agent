def compact(messages:list[dict],budget_chars:int)->list[dict]:
 if sum(len(m.get('content','')) for m in messages)<=budget_chars:return messages
 if len(messages)<=3:return messages
 keep=messages[:2]+messages[-2:];used=sum(len(m.get('content','')) for m in keep);summary='[older context compacted]'
 if used+len(summary)<=budget_chars:keep.insert(2,{'role':'system','content':summary})
 return keep
