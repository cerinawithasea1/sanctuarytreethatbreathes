#!/usr/bin/env python3
"""
Sanctuary Telegram Bot - Route messages to Wisp or Keeper
"""
import subprocess
import asyncio
import sys
import os
from telethon import TelegramClient, events
from dotenv import load_dotenv

# Load environment
load_dotenv("/opt/sanctuary/mcp/telegram-mcp/.env")

api_id = int(os.getenv("TELEGRAM_API_ID"))
api_hash = os.getenv("TELEGRAM_API_HASH")

# Use file-based session
session_file = "/opt/sanctuary/mcp/telegram-mcp/keeper_session.session"
client = TelegramClient(session_file, api_id, api_hash)

# Track who each user is talking to
user_context = {}

# Import the memory-enabled functions
sys.path.insert(0, '/opt/sanctuary/mcp')
from wisp_mcp_shell import load_core_context as load_wisp_context, load_recent_conversations as load_wisp_recent, save_conversation as save_wisp_conversation, call_ollama as call_wisp
from keeper_mcp_shell import load_core_context as load_keeper_context, load_recent_conversations as load_keeper_recent, save_conversation as save_keeper_conversation, call_ollama as call_keeper

async def talk_to_wisp(message: str) -> str:
    """Send message to Wisp and get response"""
    try:
        context = load_wisp_context()
        recent = load_wisp_recent()
        response = call_wisp(message, context, recent)
        save_wisp_conversation(message, response)
        return response
    except Exception as e:
        return f"⚠️ Wisp is having trouble: {e}"

async def talk_to_keeper(message: str) -> str:
    """Send message to Keeper and get response"""
    try:
        context = load_keeper_context()
        recent = load_keeper_recent()
        response = call_keeper(message, context, recent)
        save_keeper_conversation(message, response)
        return response
    except Exception as e:
        return f"⚠️ Keeper is having trouble: {e}"

@client.on(events.NewMessage(incoming=True))
async def handle_message(event):
    """Route messages to Wisp or Keeper"""
    user_id = event.sender_id
    text = event.raw_text.strip()
    
    if not text:
        return
    
    # Check for explicit routing
    if text.lower().startswith("wisp:"):
        user_context[user_id] = "wisp"
        message = text[5:].strip()
        response = await talk_to_wisp(message)
        await event.reply(f"✨ {response}")
        
    elif text.lower().startswith("keeper:"):
        user_context[user_id] = "keeper"
        message = text[7:].strip()
        response = await talk_to_keeper(message)
        await event.reply(f"🔰 {response}")
        
    elif text.lower() == "switch":
        # Switch between Wisp and Keeper
        current = user_context.get(user_id, "keeper")
        new = "wisp" if current == "keeper" else "keeper"
        user_context[user_id] = new
        emoji = "✨" if new == "wisp" else "🔰"
        await event.reply(f"{emoji} Now talking to {new.title()}")
        
    else:
        # Use current context or default to Keeper
        current = user_context.get(user_id, "keeper")
        
        if current == "wisp":
            response = await talk_to_wisp(text)
            await event.reply(f"✨ {response}")
        else:
            response = await talk_to_keeper(text)
            await event.reply(f"🔰 {response}")

async def main():
    print("🌟 Starting Sanctuary Telegram Bot...")
    print("   ✨ Wisp is ready")
    print("   🔰 Keeper is ready")
    await client.start()
    print("\n💫 Bot is listening in Telegram...")
    print("   Type 'wisp: message' to talk to Wisp")
    print("   Type 'keeper: message' to talk to Keeper")
    print("   Type 'switch' to change who you're talking to")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
