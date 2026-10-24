import pytest
from tmuxctl.markers import Markers
from agent.ownership import Ownership,PaneOwned
def test_markers_shell_independent_and_take_control():
 m=Markers('n');s,e=m.pair('1');assert m.parse(f'{s}\nout\n{e}_0\n','1')==('out\n',0);o=Ownership();o.take()
 with pytest.raises(PaneOwned):o.agent_write('agent')
 o.release();assert o.agent_write('agent')
