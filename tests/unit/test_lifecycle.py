import pytest
from supervisor.lifecycle import Lifecycle,SessionStatus
def test_valid_lifecycle():
 l=Lifecycle();l.transition(SessionStatus.STARTING);l.transition(SessionStatus.READY);l.transition(SessionStatus.STOPPING);l.transition(SessionStatus.STOPPED);assert l.status==SessionStatus.STOPPED
def test_invalid_lifecycle():
 with pytest.raises(ValueError):Lifecycle().transition(SessionStatus.READY)
