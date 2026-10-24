#!/data/data/com.termux/files/usr/bin/python
import json,sys
required={f'Q{i:02d}' for i in range(1,15)};rows=[]
for p in sys.argv[1:]:
 for n,line in enumerate(open(p),1):
  if line.strip():
   try:rows.append(json.loads(line))
   except Exception as e:print(f'{p}:{n}: invalid JSON: {e}',file=sys.stderr);raise SystemExit(1)
seen={r.get('question') for r in rows};missing=sorted(required-seen);bad=[r for r in rows if r.get('status') not in {'PASS','FAIL','SKIP'}]
summary={'schema_version':1,'required':14,'records':len(rows),'pass':sum(r.get('status')=='PASS' for r in rows),'fail':sum(r.get('status')=='FAIL' for r in rows),'skip':sum(r.get('status')=='SKIP' for r in rows),'missing':missing,'complete_for_review':not missing and not bad,'approved_for_m1':False}
print(json.dumps(summary,indent=2));raise SystemExit(0 if summary['complete_for_review'] else 1)
