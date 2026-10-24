from tmuxctl.panes import Pane
def test_pane_shape():
 p=Pane('%1','@1','user',True,False,80,24);assert p.window_name=='user' and p.width==80
