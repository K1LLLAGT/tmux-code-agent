#!/data/data/com.termux/files/usr/bin/python
from common import *
import os,urllib.request
base=os.getenv('TCA_MODEL_BASE_URL')
if not base: emit('Q09','model-protocol','SKIP','NO_MODEL_ENDPOINT','Set TCA_MODEL_BASE_URL; quality benchmarking remains M7/M12');raise SystemExit(2)
try:
 with urllib.request.urlopen(base.rstrip('/')+'/models',timeout=5) as r: body=r.read(4000).decode(errors='replace')
 emit('Q09','model-protocol','PASS','MODELS_ENDPOINT_OK','Configured OpenAI-compatible models endpoint responded',{'body':body});
except Exception as e: emit('Q09','model-protocol','FAIL','ENDPOINT_FAILED',repr(e),{'base_url':base});raise SystemExit(1)
