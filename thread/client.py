import socket

HOST = '127.0.0.1'
PORT = 12345

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((HOST, PORT))
    print("Connected to server. Type messages, or 'exit' to quit.")
    while True:
        message = input("You: ")
        sock.sendall(message.encode())
        if message.lower() == 'exit':
            break
        data = sock.recv(1024)
        print("Echoed:", data.decode())
