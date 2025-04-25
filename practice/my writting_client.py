# echo_client.py
import socket
# 服务器地址
HOST = '127.0.0.1'
PORT = 19998 # 服务器端口


# create socket using TCP protocol
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    
# connect to the host and port same as server
    client_socket.connect((HOST, PORT))
# keep receive message until user enter 'exit'
    while True:
        msg = input("Enter message: (enter 'exit' to leave)")
        if msg.lower() == 'exit':
            break
        client_socket.sendall(msg.encode())
# send all message 
        data = client_socket.recv(1024)
# use socket to receive message
# print the message received from the server
        print(f"echo from the server: {data.decode()}")
