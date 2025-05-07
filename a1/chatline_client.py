# chatclient.py
# =============
# This script implements the chat client.
# It connects to the chatserver using TCP, supports command-line arguments,
# reads both from stdin and from socket (asynchronously), and handles messages.
# Related spec lines: 49–252

import sys
import socket
import threading
from msg_protocol import send_message, receive_message, connect_to_server
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
    print("Error: we Unable to connect to port", file=sys.stderr)
    sys.exit(7)

username = sys.argv[2]

if not username or ' ' in username:
    print("Usage: chatclient port_number client_username", file=sys.stderr)
    sys.exit(3)

# ========= Attempt Connection to Server =========
# Line 81–85: If connection fails, exit status 7

sock =connect_to_server(port,username)


# ========= Start and Join Threads =========
# Daemon threads so program exits cleanly
stdin_thread = threading.Thread(target=listen_stdin, args=(sock, username), daemon=True)
socket_thread = threading.Thread(target=listen_socket, args=(sock,), daemon=True)

stdin_thread.start()
socket_thread.start()

# Wait until stdin thread exits (e.g., on /quit or EOF)
stdin_thread.join()
sock.close()

