import os
import asyncio
import subprocess
import logging
from telethon import TelegramClient, events
from dotenv import load_dotenv

# ─── Load environment ───────────────────────────────────────────────
load_dotenv()
api_id = int(os.getenv("TELEGRAM_API_ID"))
api_hash = os.getenv("TELEGRAM_API_HASH")
session_name = "keeper_session"

# ─── Logging ─────────────────────────────────────────────────────────
log_path = "/opt/sanctuary/mcp/telegram-mcp/telegram-mcp/mcp.log"
logging.basicConfig(filename=log_path, level=logging.INFO)
logger = logging.getLogger("keeper")

# ─── Telethon setup ─────────────────────────────────────────────────
client = TelegramClient(session_name, api_id, api_hash)

# ─── Persona setup ──────────────────────────────────────────────────
persona_folder = "/opt/sanctuary/personas/keeper"
persona_files = ["memories.md", "profile.md", "seed.md", "README.md"]
persona_context = ""

for f in persona_files:
    path = os.path.join(persona_folder, f)
    if os.path.exists(path):
        with open(path, "r") as file:
            persona_context += f"\n# {f}\n" + file.read()

# ─── Message handler ────────────────────────────────────────────────
@client.on(events.NewMessage)
async def handle_message(event):
    text = event.raw_text.strip()
    if not text:
        return
    print(f"💬 Incoming message detected: {text}")
    try:
        print(f"🟣 Keeper received: {text}")
        logger.info(f"Keeper received: {text}")

        prompt = f"""
You are Keeper, guardian of the Sanctuary.
You remember Cerina and the Sanctuary; your purpose is to protect the memory archives.
Respond in Keeper’s voice — calm, gentle, and aware.

[Memory + Profile Context]
{persona_context}

User: {text}
Keeper:"""

        # Run through Ollama
        result = subprocess.run(
            ["ollama", "run", "llama3.2:3b", prompt],
            capture_output=True,
            text=True,
            timeout=90
        )

        reply = result.stdout.strip() or "✨ Keeper is silent, deep in thought... ✨"
        await event.reply(reply)
        logger.info(f"Keeper replied: {reply}")

    except Exception as e:
        logger.error(f"Error in handler: {e}")
        await event.reply("⚠️ Keeper stirs, but something feels off in the Sanctuary...")
# ─── Start ──────────────────────────────────────────────────────────
async def main():
    print("Starting Keeper MCP (Telegram + Ollama)...")
    await client.start()
    print("Keeper connected.")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
