# chatserver.py (simplified version)
import socket
import threading
from msg_protocol import send_message, receive_message

HOST = '127.0.0.1'
PORT = 12345

clients = {}  # username: conn

def handle_client(conn, addr):
    try:
        username = receive_message(conn)
        if not username:
            conn.close()
            return

        # 用户名冲突检测（简单处理）
        if username in clients:
            send_message(conn, f'[Server Message] Channel "general" already has user {username}.')
            conn.close()
            return

        clients[username] = conn
        print(f"{username} joined from {addr}")
        send_message(conn, f"Welcome to chatclient, {username}.")
        send_message(conn, '[Server Message] You have joined the channel "general".')

        broadcast(f"[Server Message] {username} has joined the channel.", sender=None)

        while True:
            msg = receive_message(conn)
            if msg is None or msg.strip() == "/quit":
                break
            broadcast(f"[{username}] {msg}", sender=username)

    finally:
        conn.close()
        if username in clients:
            del clients[username]
            broadcast(f"[Server Message] {username} has left the channel.", sender=None)
            print(f"{username} disconnected")

def broadcast(message, sender):
    """
    Send a message to all connected clients.
    """
    for user, client_conn in clients.items():
        try:
            send_message(client_conn, message)
        except:
            pass  # silently fail for now

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
        server_sock.bind((HOST, PORT))
        server_sock.listen()
        print(f"Channel 'general' is created on port {PORT}, with a capacity of 8.")
        print("Welcome to chatserver.")

        while True:
            conn, addr = server_sock.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    main()
