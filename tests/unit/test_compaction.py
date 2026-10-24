from agent.compaction import compact
def test_compaction_keeps_recent_and_policy():
 m=[{'role':'system','content':'POLICY'},{'role':'user','content':'TASK'}]+[{'role':'user','content':'x'*100} for _ in range(8)];c=compact(m,250);assert c[0]['content']=='POLICY' and c[1]['content']=='TASK' and len(c)<len(m)
