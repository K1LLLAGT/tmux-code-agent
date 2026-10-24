from web.ws_events import EventRing
def test_sequence_replay():
 r=EventRing(3);r.publish('a',{});r.publish('b',{});r.publish('c',{});assert [x['seq'] for x in r.replay(1)]==[2,3]
