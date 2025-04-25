# echo_server.py
import socket

HOST = '127.0.0.1'  # 本地回环地址
PORT = 64450      # 非特权端口


# create a socket object
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
# tell the socket object which host to listen
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"Server listening on {HOST}:{PORT}")
    
    # create new socket object conn to comunicate with the customer
    # addr store the address of the client
    conn, addr = server_socket.accept()  # 等待客户端连接
    # receive message after 
    with conn:
        print(f"Connected by {addr}")
        # receive message repeatly
        while True:
            data = conn.recv(1024)  # 接收最多1024字节
            if not data:
                break  # 连接断开
            print(f"Received from client: {data.decode()}")
            conn.sendall(data)  # 发送原样数据
