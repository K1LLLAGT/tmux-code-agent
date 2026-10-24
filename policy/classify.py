from policy.capabilities import Capability as C
NETWORK={'curl','wget','ssh','scp','nc'};INSTALL={'pkg','pip','pip3','npm','cargo'};OPAQUE={'sh','bash','zsh','python','python3'}
def classify(argv:list[str])->set[C]:
 if not argv:return set()
 out={C.SHELL_EXEC};cmd=argv[0].rsplit('/',1)[-1]
 if cmd in NETWORK:out.add(C.NETWORK_EXTERNAL)
 if cmd in INSTALL:out|={C.SHELL_INSTALL,C.NETWORK_EXTERNAL}
 if cmd=='git' and len(argv)>1 and argv[1] in {'clone','fetch','pull','push'}:out.add(C.NETWORK_EXTERNAL)
 if cmd in OPAQUE and '-c' in argv:out.add(C.SHELL_INSTALL) # approval-driving opaque execution
 return out
