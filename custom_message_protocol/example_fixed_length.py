import struct
import socket

# 封包（发送前处理）
def pack_message(msg: str) -> bytes:
    # convert string to bytes
    data = msg.encode('utf-8')
    # Calculate the number of bytes
    length = len(data)
    # return pack of length in 4 bytes
    return struct.pack('!I', length) + data
    # '!I' 表示 network byte order 的 unsigned int（4字节）

# 拆包（接收后处理）
def unpack_message(sock: socket.socket) -> str:
    # read first 4 bytes
    header = sock.recv(4)
    if not header:
        return None
    # parse 4 bytes into integer
    length = struct.unpack('!I', header)[0]

    # continue reading until you get "length" bytes
    data = b''
    while len(data) < length:
        more = sock.recv(length - len(data))
        if not more:
            return None
        data += more

    return data.decode('utf-8')
