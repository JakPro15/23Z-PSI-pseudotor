import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as connecting_socket:
    connecting_socket.connect(('127.0.0.1', 8000))
    data = bytearray(socket.inet_aton('127.0.0.1'))
    data.extend(b'Hello' * 100)
    connecting_socket.sendall(data)
    response = connecting_socket.recv(1024)
    print(response)
    assert data[4:].decode('ascii') == response.decode('ascii')