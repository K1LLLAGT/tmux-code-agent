#!/data/data/com.termux/files/usr/bin/python
import json,sys,pathlib,datetime,re
root=pathlib.Path(__file__).resolve().parents[2] if 'scripts' in pathlib.Path(__file__).parts else pathlib.Path.cwd()
# Installed destination is ROOT/scripts/m0-review-results.py, so parent is project root.
root=pathlib.Path(__file__).resolve().parent.parent
out=root/'docs'/'spike-results'; dec=root/'docs'/'decisions'; device=sys.argv[1] if len(sys.argv)>1 else 'sm-t870'
titles={
'Q01':'tmux control mode PTY','Q02':'tmux feature baseline','Q03':'private sshd restrictions','Q04':'SSH ControlMaster','Q05':'Android process budget','Q06':'browser launch','Q07':'Python web stack','Q08':'Termux dependencies','Q09':'model tool protocol','Q10':'filesystem primitives','Q11':'Android IME','Q12':'CI device fidelity','Q13':'dependency licenses','Q14':'wake-lock policy'}
files=[]
for i in range(1,15):
 q=f'Q{i:02d}'; p=out/f'{device}-{q.lower()}.json'
 if p.exists():
  try: files.append((q,p,json.loads(p.read_text())))
  except Exception as e: files.append((q,p,{"status":"FAIL","code":"INVALID_JSON","summary":str(e),"evidence":{}}))
summary={"device":device,"generated_at":datetime.datetime.now(datetime.timezone.utc).isoformat(),"results":[]}
for q,p,r in files:
 summary['results'].append({"question":q,"status":r.get('status'),"code":r.get('code'),"exit":r.get('runner_exit_code'),"file":str(p.relative_to(root))})
(out/f'{device}-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
for q,p,r in files:
 n=int(q[1:]); matches=list(dec.glob(f'ADR-{n:04d}-*.md'))
 if not matches: continue
 adr=matches[0]
 evidence=json.dumps(r.get('evidence',{}),indent=2,sort_keys=True)
 text=f'''# ADR-{n:04d}: {titles[q].title()}\nStatus: Proposed\n\n## §44 Question\n{q} — {titles[q]}.\n\n## Evidence\n- Device result: `{p.relative_to(root)}`\n- Status: `{r.get("status","UNKNOWN")}`\n- Code: `{r.get("code","UNKNOWN")}`\n- Probe exit: `{r.get("runner_exit_code","UNKNOWN")}`\n- Summary: {r.get("summary","")}\n\n```json\n{evidence}\n```\n\n## Draft Decision\nReview required. A probe PASS is evidence, not automatic architectural approval. A FAIL or SKIP must be resolved or covered by an explicitly accepted fallback.\n\n## Fallback\nUse the fallback stated in §44 of the master design until this ADR is changed from `Proposed` after review.\n\n## Consequences\nDocument compatibility, security, performance, maintenance, and test effects during review.\n\n## M1 Impact\nKeep `Approved to begin M1: NO` until all blocking evidence and the two-device dependency requirement are resolved.\n'''
 adr.write_text(text)
print(json.dumps(summary,indent=2))
