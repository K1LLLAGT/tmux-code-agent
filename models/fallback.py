def switch(current,candidates,healthy,audit):
 for x in candidates:
  if x!=current and healthy(x):audit('model.switched',{'from':current,'to':x});return x
 return current
