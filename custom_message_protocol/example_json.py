import json

def pack_message(obj: dict) -> bytes:
    return (json.dumps(obj) + '\n').encode('utf-8')

def unpack_message(buffer: bytes) -> (list, bytes):
    messages = []
    while b'\n' in buffer:
        line, buffer = buffer.split(b'\n', 1)
        messages.append(json.loads(line.decode('utf-8')))
    return messages, buffer
