import socket;

HOST = '128.0.0'
PORT = 19998;

with socket.socket(socket.AF_INET, SOCK_STREAM) as server_socket:
    