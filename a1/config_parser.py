# config_parser.py
# =================
# This module reads and validates the configuration file provided to chatserver.
# It parses channels with name, port, and capacity, and ensures the values are valid.
# Assignment Spec References:
# - Line 266–273: Line format and content
# - Line 274–280: Value ranges and rules
# - Line 290–303: Error handling and invalid file detection

import sys
import re

def parse_config_file(filename):
    channels = {}
    used_ports = set()

    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
    except:
        print("Error: Invalid configuration file.", file=sys.stderr)
        sys.exit(5)  # Assignment requirement (Line 291)

    for line in lines:  
        parts = line.strip().split()

        # Line must have exactly 4 parts and start with 'channel'
        if len(parts) != 4 or parts[0] != "channel":
            print("Error: Invalid configuration file.", file=sys.stderr)
            sys.exit(5)  # Assignment requirement (Line 295, 301)

        _, name, port_str, capacity_str = parts

        # Validate channel name (letters, numbers, underscores only)
        if not re.fullmatch(r'\w+', name):
            print("Error: Invalid configuration file.", file=sys.stderr)
            sys.exit(5)  # Assignment requirement (Line 275)

        # Convert port and capacity to int
        try:
            port = int(port_str)
            capacity = int(capacity_str)
        except ValueError:
            print("Error: Invalid configuration file.", file=sys.stderr)
            sys.exit(5)  # Assignment requirement (Line 297)

        # Validate port range
        if port < 1024 or port > 65535:
            print("Error: Invalid configuration file.", file=sys.stderr)
            sys.exit(5)  # Assignment requirement (Line 298)

        # Validate capacity range
        if capacity < 1 or capacity > 8:
            print("Error: Invalid configuration file.", file=sys.stderr)
            sys.exit(5)  # Assignment requirement (Line 299)

        # Check for duplicate channel name or port
        if name in channels or port in used_ports:
            print("Error: Invalid configuration file.", file=sys.stderr)
            sys.exit(5)  # Assignment requirement (Line 300)

        # Save valid channel
        channels[name] = {
            "port": port,
            "capacity": capacity
        }
        used_ports.add(port)

    return channels