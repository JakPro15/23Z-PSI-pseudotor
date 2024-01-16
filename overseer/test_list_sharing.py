import socket


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(("127.0.0.1", 8001))
    s.send(b"PSEUDOTOR_GET_NODES")
    data = s.recv(1024)
    ip_addresses = data.decode('ascii').split(' ')
    for ip_address in ip_addresses:
        print(ip_address)
s.close()
