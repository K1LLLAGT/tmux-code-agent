from models.fallback import switch
def test_switch_audited():
 e=[];assert switch('a',['a','b'],lambda x:x=='b',lambda t,d:e.append((t,d)))=='b';assert e[0][0]=='model.switched'
