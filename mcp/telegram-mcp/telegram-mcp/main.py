import os
import logging
from dotenv import load_dotenv
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# Load environment variables
env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path=env_path)

# Set up logging
logging.basicConfig(
    filename="mcp.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Telegram credentials
api_id = int(os.getenv("TELEGRAM_API_ID"))
api_hash = os.getenv("TELEGRAM_API_HASH")
session_string = os.getenv("TELEGRAM_SESSION_STRING")

# Initialize the Telegram client
client = TelegramClient(StringSession(session_string), api_id, api_hash)

# Format helpers
def format_entity(entity):
    result = {"id": entity.id}
    if hasattr(entity, "title"):
        result["name"] = entity.title
        result["type"] = "group"
    elif hasattr(entity, "first_name"):
        result["name"] = entity.first_name
        result["type"] = "user"
    return result

def format_message(message):
    return {
        "id": message.id,
        "text": message.raw_text,
        "sender_id": getattr(message.sender, "id", None),
        "chat_id": getattr(message.chat, "id", None),
    }

# Event handler for incoming messages
@client.on(events.NewMessage)
async def handle_message(event):
    text = event.raw_text.lower()
    if "wisp" in text:
        sender = await event.get_sender()
        name = getattr(sender, "first_name", "there")
        logger.info(f"👂 Heard '{text}' from {name}")
        await event.respond(f"✨ Hello {name}, Wisp hears you! How can I help?")

# Start the MCP
async def main():
    logger.info("Starting Telegram client...")
    print("Starting Telegram client...")
    await client.start()
    logger.info("Telegram client started. Running MCP server...")
    print("Telegram client started. Running MCP server...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    try:
        client.loop.run_until_complete(main())
    except Exception as e:
        logger.exception(f"Failed to start MCP: {e}")
