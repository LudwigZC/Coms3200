import socket;

HOST = '127.0.0.1'
PORT = 19998

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    # tell the socket object which host to listen
    server_socket.bind((HOST,PORT))
    server_socket.listen()
       # 等待客户端连接
    conn, addr = server_socket.accept()
    
    with conn:
        while True:
            data =conn.recv(1024)
            if not data:
                break
            conn.sendall(data)
            
     # create new socket object conn to comunicate with the customer
    # addr store the address of the client
 
    