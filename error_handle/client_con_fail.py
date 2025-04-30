import sys
import socket

try:
    port = int(sys.argv[1])
    username = sys.argv[2]
except:
    print("Usage: client port_number client_username", file = sys.stderr)
    sys.exit(3)