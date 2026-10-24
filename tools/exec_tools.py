from policy.hard_deny import command_denied
from policy.classify import classify
from tools.envelope import ok,error
def inspect_exec(argv):
 if command_denied(argv):return error('ERR_POLICY_DENIED','hard-denied command')
 return ok({'required_capabilities':sorted(c.value for c in classify(argv))})
