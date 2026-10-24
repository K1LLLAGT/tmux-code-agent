def verify_claims(claims:list[dict],facts:dict)->list[dict]:
 out=[]
 for c in claims:
  ok=True
  if c.get('kind')=='tests_pass':ok=bool(facts.get('tests_after_last_edit') is True)
  out.append({**c,'verified':ok})
 return out
def final_report(facts:dict,notes:str='')->dict:return {'files_changed':facts.get('files_changed',[]),'commands':facts.get('commands',[]),'agent_notes':notes}
