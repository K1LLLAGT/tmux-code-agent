from web.ws_events import EventRing
def test_ring_discards_oldest():
 r=EventRing(2);r.publish('1',{});r.publish('2',{});r.publish('3',{});assert [e['seq'] for e in r.replay(0)]==[2,3]
