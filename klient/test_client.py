import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as connecting_socket:
    connecting_socket.connect(('127.0.0.1', 8000))
    data = bytearray()
    address = socket.inet_aton('127.0.0.1')
    message = b'Hello'
    data.extend(address)
    data.extend(message)
    connecting_socket.sendall(data)
    response_buffer = bytearray()
    while True:
        response = connecting_socket.recv(4096)
        if not response:
            break
        response_buffer.extend(response)
    print(f"Message: {message}")
    print(f"Response: {bytes(response_buffer)}")