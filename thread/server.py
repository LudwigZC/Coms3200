import socket
import threading

HOST = '127.0.0.1'
PORT = 12345

# Handle each client connection in a new thread
def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            message = data.decode()
            if message.lower() == 'exit':
                print(f"[DISCONNECTED] {addr} exited.")
                break
            print(f"[RECEIVED from {addr}] {message}")
            conn.sendall(data)  # Echo back the same message
    print(f"[CONNECTION CLOSED] {addr}")

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"[SERVER STARTED] Listening on {HOST}:{PORT}")

    while True:
        conn, addr = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

if __name__ == "__main__":
    main()
