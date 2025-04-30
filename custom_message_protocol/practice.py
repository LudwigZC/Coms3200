# （1）简单练习：固定长度协议
# 写一个小程序：
import socket
import struct
# 客户端每次发送一条“hello i”消息（i是编号）

# 服务器端正确接收并打印出所有消息内容

# 要求：
HOST = '127.0.0.1'
PORT = 12345
# 必须用固定4字节头部 + 内容的封包/拆包方法
def pack(msg:str)-> bytes:
    msg = "Hello " + msg
    data = msg.encode("utf-8")
    length = len(data)
    result = struct.pack('!I',length) + data
    return result

def recv_full_msg(sock):
    header = sock.recv(4)
    if not header:
        return None
    length = struct.unpack("!I",header)[0]
    data = b''
    while length> len(data):
        chunk = sock.recv(length - len(data))
        if not chunk:
            return None
        data = chunk + data
    return data.decode('utf-8')
def sendHello():
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as socket_client:
        socket_client.connect((HOST,PORT))
        for i in range(5):
            msg = pack(f"{i}")
            if not msg:
                break
            socket_client.sendall(msg)
            reply = recv_full_msg(socket_client)
            print(f"you enter {reply} ")
            
            
def main():
    sendHello()

if __name__ == "__main__":
    main()