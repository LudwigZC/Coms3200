import socket
import thread
import sys

def listen_stdin(sock):
    try:
        while True:
            msg = sys.stdin.readline()
            if not msg:
                break
            sock.sendall(msg.encode())
    except Exception as e:
        print("somthing went wrong:",e)
        
        
        
        
    