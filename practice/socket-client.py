# echo_client.py
import socket

HOST = '127.0.0.1'  # 服务器地址
PORT = 64450       # 服务器端口

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))
    while True:
        msg = input("Enter message (type 'exit' to quit): ")
        if msg.lower() == 'exit':
            break
        client_socket.sendall(msg.encode())
        data = client_socket.recv(1024)
        print(f"Echoed from server: {data.decode()}")