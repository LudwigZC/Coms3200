import socket
import sys
import threading
from msg_protocol import send_message, receive_message,connect_to_server


# ========= Listen Threads =========
# Line 111: Communication must be asynchronous (multi-threaded)

def listen_stdin(sock, username):
    """
    Thread function to read stdin and send messages.
    - Broadcast if plain message
    - Support / commands (/quit, /send, etc.)
    Assignment Spec: Lines 113–136
    """
    while True:
        try:
            user_input = input()
            if not user_input:
                continue
            send_message(sock, user_input)
            if user_input.strip() == "/quit":
                break
            
        except EOFError:
            # Spec line 182: EOF = /quit
            break


def listen_socket(sock):
    """
    Thread function to receive messages from server and print them.
    Assignment Spec: Lines 239–244
    If connection is lost, exit with status 8.
    """
    while True:
        message = receive_message(sock)
        if message is None:
            print("Error: server connection closed.", file=sys.stderr)
            sys.exit(8)
        elif message.startswith("SWITCH"):
            _, port_str, user = message.strip().split()
            sock.close()
            connect_to_server(int(port_str), user)

        else:
            print(message, flush=True)


