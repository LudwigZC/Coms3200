def pack_message(msg: str) -> bytes:
    return (msg + '\n').encode('utf-8')

def unpack_message(buffer: bytes) -> (list, bytes):
    """
    从buffer中提取完整消息列表，同时返回剩余buffer
    """
    messages = []
    while b'\n' in buffer:
        line, buffer = buffer.split(b'\n', 1)
        messages.append(line.decode('utf-8'))
    return messages, buffer
