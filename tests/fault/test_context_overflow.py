from agent.compaction import compact
def test_context_overflow_compacts():
 m=[{'role':'system','content':'P'},{'role':'user','content':'T'}]+[{'role':'user','content':'z'*1000} for _ in range(20)];c=compact(m,3000);assert len(c)<len(m);assert c[0]['content']=='P' and c[1]['content']=='T'
