import socket
import threading
import sys

def listen_stdin(sock):
    """读取用户输入并发送给服务器"""
    try:
        while True:
            msg = sys.stdin.readline()
            if not msg:
                break
            sock.sendall(msg.encode())
    except Exception as e:
        print(f"stdin error: {e}")

def listen_socket(sock):
    """监听服务器发来的消息"""
    try:
        while True:
            data = sock.recv(1024)
            if not data:
                print("Error: server connection closed.", file=sys.stderr)
                sys.exit(8)
            print(data.decode(), end='')
    except Exception as e:
        print(f"socket error: {e}")

def main():
    if len(sys.argv) != 3:
        print("Usage: chatclient port_number client_username", file=sys.stderr)
        sys.exit(3)

    port = int(sys.argv[1])
    username = sys.argv[2]

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('localhost', port))
        sock.sendall(username.encode())
    except:
        print(f"Error: Unable to connect to port {port}.", file=sys.stderr)
        sys.exit(7)

    print(f"Welcome to chatclient, {username}.")

    # 启动线程：监听stdin
    t1 = threading.Thread(target=listen_stdin, args=(sock,))
    t2 = threading.Thread(target=listen_socket, args=(sock,))

    t1.daemon = True
    t2.daemon = True

    t1.start()
    t2.start()

    # 等待两个线程结束
    t1.join()
    t2.join()

if __name__ == "__main__":
    main()
