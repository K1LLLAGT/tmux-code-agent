class InvalidArgs(ValueError):pass
def validate(spec:dict,args:dict):
 for k,t in spec.get('required',{}).items():
  if k not in args:raise InvalidArgs(f'missing {k}')
  if not isinstance(args[k],t):raise InvalidArgs(f'{k} has wrong type')
 extra=set(args)-set(spec.get('required',{}))-set(spec.get('optional',{}))
 if extra:raise InvalidArgs(f'unknown fields: {sorted(extra)}')
 return args
