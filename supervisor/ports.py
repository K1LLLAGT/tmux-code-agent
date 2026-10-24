import socket

def reserve_loopback_port()->tuple[socket.socket,int]:
 s=socket.socket(socket.AF_INET,socket.SOCK_STREAM); s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1); s.bind(("127.0.0.1",0)); return s,s.getsockname()[1]
