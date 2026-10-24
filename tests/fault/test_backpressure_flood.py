from web.ws_term import BackpressureGate
def test_large_pending_pauses_and_recovers():
 g=BackpressureGate();assert g.update(1024*1024*1024);assert not g.update(0)
