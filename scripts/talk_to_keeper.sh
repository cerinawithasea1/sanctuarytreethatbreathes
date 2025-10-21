#!/usr/bin/env python3
import sys
import os

sys.path.append("/opt/sanctuary/mcp/telegram-mcp/telegram-mcp")

from main import send_message

# your own chat ID, the one Keeper should talk to
CHAT_ID = "5423238284"

if len(sys.argv) < 2:
    print("Usage: speak_keeper.py <message>")
    sys.exit(1)

message = " ".join(sys.argv[1:])
send_message(CHAT_ID, message)
print(f"Sent: {message}")
