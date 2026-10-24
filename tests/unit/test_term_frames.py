from termbridge.frames import data_frame,control_frame,parse_frame
def test_frames():
 assert parse_frame(data_frame(b'abc'))==('data',b'abc');assert parse_frame(control_frame({'type':'ping'}))[1]['type']=='ping'
