from __future__ import annotations
import json
DATA=0x00; CONTROL=0x01

def data_frame(data:bytes)->bytes:return bytes([DATA])+data
def control_frame(payload:dict)->bytes:return bytes([CONTROL])+json.dumps(payload,separators=(',',':')).encode()
def parse_frame(frame:bytes):
 if not frame:raise ValueError('empty frame')
 if frame[0]==DATA:return ('data',frame[1:])
 if frame[0]==CONTROL:return ('control',json.loads(frame[1:]))
 raise ValueError('unknown frame type')
