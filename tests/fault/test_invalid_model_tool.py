import pytest
from models.tooljson import parse_action,ToolJSONError
def test_invalid_tool_shape_rejected():
 with pytest.raises(ToolJSONError):parse_action('{"tool":7,"args":[]}')
