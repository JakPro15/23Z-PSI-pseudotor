import socket


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(("127.0.0.1", 8001))
    s.send(b"PSEUDOTOR_REGISTER")
s.close()
