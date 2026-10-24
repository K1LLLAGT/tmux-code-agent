import dataclasses
from policy.approvals import request,valid
def test_binding_and_expiry():
 a=request('exec',{'argv':['true']},'/w');assert valid(a,'exec',{'argv':['true']},'/w');assert not valid(a,'exec',{'argv':['false']},'/w');assert not valid(dataclasses.replace(a,expires_at=0),'exec',{'argv':['true']},'/w')
