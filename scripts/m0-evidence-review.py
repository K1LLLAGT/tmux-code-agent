#!/data/data/com.termux/files/usr/bin/python
import json,pathlib,sys
root=pathlib.Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve(); out=root/'docs'/'spike-results'; dec=root/'docs'/'decisions'
rows=[]
for n in range(1,15):
 q=f'Q{n:02d}'; p=out/f'sm-t870-q{n:02d}.json'
 if p.exists():
  try:r=json.loads(p.read_text()); status=r.get('status','?');code=r.get('code','?');valid=True
  except Exception as e:status='INVALID';code=str(e);valid=False
 else:status='MISSING';code='NO_FILE';valid=False
 a=list(dec.glob(f'ADR-{n:04d}-*.md')); ast='MISSING'
 if a:
  for line in a[0].read_text(errors='replace').splitlines():
   if line.startswith('Status:'):ast=line.split(':',1)[1].strip();break
 rows.append((q,status,code,ast,str(p.relative_to(root)),valid))
print('Q    RESULT  CODE                                  ADR')
print('-'*82)
for q,s,c,a,p,v in rows:print(f'{q:<4} {s:<7} {c[:36]:<36} {a}')
print('\nPASS:',sum(s=='PASS' for _,s,_,_,_,_ in rows),'FAIL:',sum(s=='FAIL' for _,s,_,_,_,_ in rows),'SKIP:',sum(s=='SKIP' for _,s,_,_,_,_ in rows),'MISSING:',sum(s=='MISSING' for _,s,_,_,_,_ in rows))
print('\nOutstanding:')
for q,s,c,a,p,v in rows:
 if s!='PASS' or a not in ('Accepted','Rejected'):print(f'- {q}: result={s}/{c}; ADR={a}')
print('\nAdditional M0 gates:')
print('- Two-device dependency install must be confirmed manually from device evidence.')
print('- Manual/deferred Q06, Q09, Q11, Q12, and Q14 must be resolved or covered by accepted ADR fallbacks.')
print('- Approved to begin M1 must remain NO until every gate is satisfied.')
