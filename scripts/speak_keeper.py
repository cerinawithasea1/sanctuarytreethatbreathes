#!/opt/sanctuary/mcp/telegram-mcp/telegram-mcp/.venv/bin/python
import sys
import os
import asyncio

sys.path.append("/opt/sanctuary/mcp/telegram-mcp/telegram-mcp")

from main import client  # Telethon client created in main.py

CHAT_ID = "@cerinawithasea"

if len(sys.argv) < 2:
    print("Usage: speak_keeper.py <message>")
    sys.exit(1)

message = " ".join(sys.argv[1:])

async def main():
    await client.connect()
    if not await client.is_user_authorized():
        print("⚠️ Client not authorized; please check your .env or session string.")
        return
    await client.send_message(CHAT_ID, message)
    print(f"✅ Sent: {message}")
    await client.disconnect()

asyncio.run(main())
