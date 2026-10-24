import pytest
from supervisor.lifecycle import Lifecycle,SessionStatus
def test_valid_lifecycle():
 l=Lifecycle();l.transition(SessionStatus.STARTING);l.transition(SessionStatus.READY);l.transition(SessionStatus.STOPPING);l.transition(SessionStatus.STOPPED);assert l.status==SessionStatus.STOPPED
def test_invalid_lifecycle():
 with pytest.raises(ValueError):Lifecycle().transition(SessionStatus.READY)

def test_same_state_transition_is_idempotent():
 l=Lifecycle(); before=l.updated_at; l.transition(SessionStatus.CREATED); assert l.status==SessionStatus.CREATED; assert l.updated_at==before

def test_stopped_state_is_idempotent_but_terminal():
 l=Lifecycle(); l.transition(SessionStatus.STARTING); l.transition(SessionStatus.READY); l.transition(SessionStatus.STOPPING); l.transition(SessionStatus.STOPPED); before=l.updated_at; l.transition(SessionStatus.STOPPED); assert l.updated_at==before
 with pytest.raises(ValueError): l.transition(SessionStatus.STARTING)
