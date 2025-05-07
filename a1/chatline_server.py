# chatserver.py
# =============
# A multithreaded TCP chat server that reads channels from a config file
# and supports multiple simultaneous client connections across multiple ports.
# Each channel listens on its own port with a defined capacity.

import socket
import threading
import sys
from config_parser import parse_config_file
from msg_protocol import send_message, receive_message

channels = {}  # channel_name -> { 'port': int, 'capacity': int, 'clients': dict, 'queue': list }

def handle_client(conn, addr, channel_name):
    try:
        username = receive_message(conn)
        if not username:
            conn.close()
            return

        ch = channels[channel_name]
        if username in ch['clients']:
            send_message(conn, f'[Server Message] Channel "{channel_name}" already has user {username}.')
            conn.close()
            return

        if len(ch['clients']) >= ch['capacity']:
            ch['queue'].append((username, conn))
            send_message(conn, f"[Server Message] You are in the waiting queue and there are {len(ch['queue']) - 1} user(s) ahead of you.")
            return

        ch['clients'][username] = conn
        send_message(conn, f"Welcome to chatclient, {username}.")
        send_message(conn, f'[Server Message] You have joined the channel "{channel_name}".')
        broadcast(channel_name, f"[Server Message] {username} has joined the channel.", sender=None)

        while True:
            msg = receive_message(conn)
            
            if msg is None or msg.strip() == "/quit":
                print(f"[Server Message] {username} has left the channel.")
                break
            elif msg.strip() =="/list":
                list_channel =list_output(channels)
                send_message(conn, list_channel)
            elif msg.strip() == "whisper":
                pass
            elif msg.startswith("/switch"):
                if len(msg.strip().split()) == 2:
                    client_name = msg.strip().split()[1]
                    switch_channel(conn,client_name, username)
                else:
                    send_message(conn,"[Server Message] Usage: /switch channel_name") 
            else:
                broadcast(channel_name, f"[{username}] {msg}", sender=username)

    finally:
        if username in channels[channel_name]['clients']:
            del channels[channel_name]['clients'][username]
            broadcast(channel_name, f"[Server Message] {username} has left the channel.", sender=None)
        conn.close()

        # Fill from queue if available
        if channels[channel_name]['queue']:
            queued_user, queued_conn = channels[channel_name]['queue'].pop(0)
            threading.Thread(target=handle_client, args=(queued_conn, addr, channel_name), daemon=True).start()

def broadcast(channel_name, message, sender=None):
    for user, conn in channels[channel_name]['clients'].items():
        try:
            send_message(conn, message)
        except:
            pass

def start_channel_listener(channel_name, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
        server_sock.bind(('127.0.0.1', port))
        server_sock.listen()
        print(f"Channel '{channel_name}' is created on port {port}, with a capacity of {channels[channel_name]['capacity']}.")

        while True:
            conn, addr = server_sock.accept()
            threading.Thread(target=handle_client, args=(conn, addr, channel_name), daemon=True).start()

def list_output(channels):
    try:
        chan_list = ""
        for chan_name, ch in channels.items():
            port = ch['port']
            current = len(ch['clients'])
            limit = ch['capacity']
            queue_len = len(ch['queue'])
            chan_list += (f"[Channel] {chan_name} {port} Capactiy: {current}/{limit}, Queue: {queue_len}\n")
    except Exception as e:
        print("error when listing the channels")

    return chan_list
def switch_channel(conn:socket,switch_channel,username):
    for chan_name,ch in channels.items():
        if switch_channel == chan_name:
            for name in ch['clients']:
                if username == name:
                    send_message(conn,f"[Server Message] Channel {switch_channel} already has user {username}")
                    return
            send_message(conn, f"SWITCH {ch['port']} {username}")

            return
    send_message(conn,f"[Server Message] Channel {chan_name} does not exist.")
    return


    


def main():
    if len(sys.argv) not in [2, 3]:
        print("Usage: chatserver [afk_time] config_file", file=sys.stderr)
        sys.exit(3)

    config_file = sys.argv[-1]
    config = parse_config_file(config_file)

    for name, info in config.items():
        channels[name] = {
            "port": info["port"],
            "capacity": info["capacity"],
            "clients": {},
            "queue": []
        }
        threading.Thread(target=start_channel_listener, args=(name, info["port"]), daemon=True).start()

    print("Welcome to chatserver.")
    threading.Event().wait()  # Keep main thread alive

if __name__ == "__main__":
    main()