import pytest
from models.tooljson import parse_action,ToolJSONError
def test_strict_json_action():
 assert parse_action('{"tool":"x","args":{}}')['tool']=='x'
 with pytest.raises(ToolJSONError):parse_action('text {"tool":"x","args":{}}')
