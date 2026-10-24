import pytest
from tools.schema import validate,InvalidArgs
def test_schema():
 assert validate({'required':{'path':str}},{'path':'x'})['path']=='x'
 with pytest.raises(InvalidArgs):validate({'required':{'path':str}},{'path':1})
