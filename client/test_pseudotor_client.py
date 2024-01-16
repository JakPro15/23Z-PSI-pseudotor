import socket
import ssl

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain('./client/certfile.pem', './client/keyfile.key', password='bruh')
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listening_socket:
    with context.wrap_socket(listening_socket, server_side=True) as ssl_socket:
        ssl_socket.bind(("127.0.0.1", 8002))
        ssl_socket.listen(5)
        while True:
            conn, addr = ssl_socket.accept()
            print(f"Connected to {addr[0]}:{addr[1]}")
            with conn:
                data_buffer = bytearray()
                while True:
                    data = conn.recv(1024)
                    if (not data) or data[-3:] == b'END':
                        break
                    data_buffer.extend(data)
                
                for i in range(3):
                    conn.send(data_buffer[6:])
            conn.close()
