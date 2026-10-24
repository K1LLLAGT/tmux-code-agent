import os,subprocess,time,asyncio
from models.openai_compat import OpenAICompatProvider
from supervisor.ports import reserve_loopback_port
def test_fake_http():
 s,p=reserve_loopback_port();s.close();proc=subprocess.Popen([os.environ.get('PYTHON',os.sys.executable),'tests/fixtures/fake_model_server.py','--port',str(p)]);time.sleep(.15)
 try:
  m=asyncio.run(OpenAICompatProvider(f'http://127.0.0.1:{p}/v1').discover());assert m[0].id=='fake-model'
 finally:proc.terminate();proc.wait(timeout=2)
