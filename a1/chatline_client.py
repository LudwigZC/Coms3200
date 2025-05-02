# chatclient.py
# =============
# This script implements the chat client.
# It connects to the chatserver using TCP, supports command-line arguments,
# reads both from stdin and from socket (asynchronously), and handles messages.
# Related spec lines: 49–252

import sys
import socket
import threading
from msg_protocol import send_message, receive_message
from stdin_server_listen import listen_socket, listen_stdin

# ========= Command-Line Argument Checking =========
# Lines 53–77: Argument order and validation
# If invalid arguments, print to stderr and exit with status 3

if len(sys.argv) != 3:
    print("Usage: chatclient port_number client_username", file=sys.stderr)
    sys.exit(3)

try:
    port = int(sys.argv[1])
except ValueError:
    print("Error: Unable to connect to port", file=sys.stderr)
    sys.exit(7)

username = sys.argv[2]

if not username or ' ' in username:
    print("Usage: chatclient port_number client_username", file=sys.stderr)
    sys.exit(3)

# ========= Attempt Connection to Server =========
# Line 81–85: If connection fails, exit status 7

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('127.0.0.1', port))
except Exception:
    print(f"Error: Unable to connect to port {port}.", file=sys.stderr)
    sys.exit(7)

# ========= Initial Handshake =========
# Line 94–105: After connecting, must send username and receive join/queue message

send_message(sock, username)

# Waiting for server welcome or queue message
server_response = receive_message(sock)
print("Welcome to chatclient, " + username)
print(server_response)


# ========= Start and Join Threads =========
# Daemon threads so program exits cleanly
stdin_thread = threading.Thread(target=listen_stdin, args=(sock, username), daemon=True)
socket_thread = threading.Thread(target=listen_socket, args=(sock,), daemon=True)

stdin_thread.start()
socket_thread.start()

# Wait until stdin thread exits (e.g., on /quit or EOF)
stdin_thread.join()
sock.close()

