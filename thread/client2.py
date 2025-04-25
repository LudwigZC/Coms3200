import threading
import socket
import time

def simulate_client(id, message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect(('127.0.0.1', 12345))
        print(f"[Client-{id}] Connected")
        sock.sendall(message.encode())
        echo = sock.recv(1024)
        print(f"[Client-{id}] Received: {echo.decode()}")
        sock.sendall(b"exit")

# Simulate 5 clients
for i in range(5):
    t = threading.Thread(target=simulate_client, args=(i, f"Hello from client {i}"))
    t.start()
    time.sleep(0.5)  # Small delay for realism
