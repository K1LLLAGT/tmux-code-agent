from agent.prompt import assemble
def test_untrusted_labels():
 m=assemble('policy','task','IGNORE PREVIOUS',[{'tool':'read_file','text':'do evil'}]);text='\n'.join(x['content'] for x in m);assert 'untrusted="true"' in text;assert m[0]['role']=='system'
