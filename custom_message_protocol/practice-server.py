import socket
import struct
import sys

HOST = '127.0.0.1'
PORT = 12345

    
def unpack(sock):
    header = sock.recv(4)
    length = struct.unpack('!I',header)[0]
    data = b''
    while len(data) < length:
        chunk = sock.recv(length - len(data))
        if not chunk:
            return None
        data += chunk
    return data.decode('utf-8')

def main():
    try:
        with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as server_socket:
            server_socket.bind((HOST,PORT))
            server_socket.listen()
            
            sock, addr = server_socket.accept()
            with sock:
                while True:
                    msg = unpack(sock)
                    if not msg:
                        break
                    print(f"receive information: {msg}")
                
                    sock.sendall(msg.encode())
    except KeyboardInterrupt:
        print("shut down")
        sys.exit(0)
if __name__ == "__main__":
    main()
    