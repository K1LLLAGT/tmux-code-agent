from web.ws_term import BackpressureGate
def test_hysteresis():
 g=BackpressureGate(10,4);assert not g.update(9);assert g.update(10);assert g.update(5);assert not g.update(4)
