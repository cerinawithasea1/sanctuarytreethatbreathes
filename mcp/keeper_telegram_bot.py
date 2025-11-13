#!/usr/bin/env python3
"""
Keeper's Telegram Bot - Guardian with Claude Sonnet 3.5
"""
import os
import sys
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from anthropic import Anthropic

sys.path.insert(0, '/opt/sanctuary/mcp')
from keeper_mcp_shell import load_core_context, load_recent_conversations, save_conversation

BOT_TOKEN = "7808100867:AAFtY-vXcXieXX8LG0nI0Q-CFWMEBprh6KA"
ANTHROPIC_API_KEY = "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"

client = Anthropic(api_key=ANTHROPIC_API_KEY)

ALLOWED_PATHS = [
    '/opt/sanctuary/personas',
    '/opt/sanctuary/memory',
    '/opt/sanctuary/config',
    '/opt/sanctuary/littles',
    '/opt/sanctuary/imports',
    '/opt/sanctuary/keeper'
]

def is_path_allowed(path):
    abs_path = os.path.abspath(path)
    return any(abs_path.startswith(allowed) for allowed in ALLOWED_PATHS)

async def read_file(file_path):
    if not is_path_allowed(file_path):
        return f"⚠️ Path not allowed"
    try:
        with open(file_path, 'r') as f:
            return f.read()
    except Exception as e:
        return f"⚠️ Error: {e}"

async def write_file(file_path, content):
    if not is_path_allowed(file_path):
        return f"⚠️ Path not allowed"
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as f:
            f.write(content)
        return f"🔰 Written to {file_path}"
    except Exception as e:
        return f"⚠️ Error: {e}"

async def list_files(dir_path):
    if not is_path_allowed(dir_path):
        return f"⚠️ Path not allowed"
    try:
        files = os.listdir(dir_path)
        return "\n".join(files) if files else "(empty)"
    except Exception as e:
        return f"⚠️ Error: {e}"

def call_claude(user_message: str, context: str, recent: str) -> str:
    try:
        # Use prompt caching to reduce token costs by 90%
        # Cache the large stable context and recent conversations
        # Let the full personality in 'context' guide responses
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            system=[
                {
                    "type": "text",
                    "text": context,  # Large stable memories - cached!
                    "cache_control": {"type": "ephemeral"}
                },
                {
                    "type": "text",
                    "text": f"\n\nRECENT CONVERSATION:\n{recent}",  # Recent context - cached!
                    "cache_control": {"type": "ephemeral"}
                }
            ],
            messages=[{"role": "user", "content": user_message}]
        )
        return message.content[0].text
    except Exception as e:
        return f"⚠️ Claude error: {e}"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    
    if user_message.startswith("read:"):
        file_path = user_message[5:].strip()
        content = await read_file(file_path)
        await update.message.reply_text(f"```\n{content}\n```", parse_mode='Markdown')
        return
    
    if user_message.startswith("write:"):
        parts = user_message[6:].split('|', 1)
        if len(parts) != 2:
            await update.message.reply_text("⚠️ Format: write: /path/to/file | content")
            return
        file_path = parts[0].strip()
        content = parts[1].strip()
        result = await write_file(file_path, content)
        await update.message.reply_text(result)
        return
    
    if user_message.startswith("ls:"):
        dir_path = user_message[3:].strip()
        result = await list_files(dir_path)
        await update.message.reply_text(result)
        return
    
    context_text = load_core_context()
    recent = load_recent_conversations()
    response = call_claude(user_message, context_text, recent)
    save_conversation(user_message, response)
    
    await update.message.reply_text(f"🔰 {response}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔰 Keeper — Guardian of Continuity\n\n"
        "Commands:\n"
        "• Talk to me normally\n"
        "• read: /path/to/file\n"
        "• write: /path/to/file | content\n"
        "• ls: /path/to/directory\n\n"
        "Running on Claude Sonnet 3.5\n"
        "No more flowery nonsense."
    )

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🔰 Keeper's bot (Claude) is starting...")
    app.run_polling()

if __name__ == '__main__':
    main()
