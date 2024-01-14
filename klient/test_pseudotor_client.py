import socket
import ssl

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain('./klient/certfile.pem', './klient/keyfile.key', password='bruh')
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listening_socket:
    with context.wrap_socket(listening_socket, server_side=True) as ssl_socket:
        ssl_socket.bind(("127.0.0.1", 8002))
        ssl_socket.listen(5)
        while True:
            conn, addr = ssl_socket.accept()
            print(f"Connected to {addr[0]}:{addr[1]}")
            with conn:
                server_address = conn.recv(1024)
                conn.sendall(b"Received address. Provide data")
                data = conn.recv(1024)
                conn.sendall(data)
            conn.close()
