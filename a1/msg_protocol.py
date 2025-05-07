# message_protocol.py
# ===================
# This module implements the communication protocol used by both the chatclient and chatserver.
# All messages are prefixed with a 4-byte big-endian integer indicating the length of the message.
# This prevents message truncation and supports proper unpacking.
# Related spec lines: 94–111, 239–244

import struct
import socket
import sys

HEADER_LENGTH = 4  # Fixed header size in bytes

def send_message(sock, message: str):
    """
    Sends a message through the socket with a 4-byte length prefix.
    Assignment Requirement:
    - Must use TCP socket for communication (Line 42)
    - Messages must be flushed to socket (Line 111)
    - Client and server may send messages at any time (Line 110)
    - Communication is asynchronous
    """
    message_bytes = message.encode('utf-8')
    length = len(message_bytes)
    header = struct.pack('!I', length)
    sock.sendall(header + message_bytes)  # Send full message


def receive_message(sock) -> str:
    """
    Receives a full message from the socket based on the 4-byte header.
    Assignment Requirement:
    - Clients must print server messages immediately upon receipt (Line 243)
    - If connection is closed unexpectedly, client exits with status 8 (Line 246–249)
    """
    
    header = sock.recv(HEADER_LENGTH)
    if not header:
        return None
    length = struct.unpack('!I', header)[0]

    data = b''
    while len(data) < length:
        chunk = sock.recv(length - len(data))
        if not chunk:
            return None
        data += chunk

    return data.decode('utf-8')

def connect_to_server(port:int,username:str)-> socket:
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
    return sock