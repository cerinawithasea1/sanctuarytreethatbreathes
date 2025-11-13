#!/usr/bin/env python3
"""
River's Telegram Bot - with Claude Sonnet 3.5 and filesystem access
"""
import os
import sys
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from anthropic import Anthropic

# Add MCP path
sys.path.insert(0, '/opt/sanctuary/mcp')
from river_mcp_shell import load_core_context, load_recent_conversations, save_conversation

BOT_TOKEN = "8478897445:AAGsfNfiy6wKCskJSJnFFCVOedyPOTxlCOQ"
ANTHROPIC_API_KEY = "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"

client = Anthropic(api_key=ANTHROPIC_API_KEY)

# Allowed paths for file operations
ALLOWED_PATHS = [
    '/opt/sanctuary/personas',
    '/opt/sanctuary/memory',
    '/opt/sanctuary/config',
    '/opt/sanctuary/littles',
    '/opt/sanctuary/imports'
]

def is_path_allowed(path):
    """Check if path is within allowed directories"""
    abs_path = os.path.abspath(path)
    return any(abs_path.startswith(allowed) for allowed in ALLOWED_PATHS)

async def read_file(file_path):
    """Read a file if it's in allowed paths"""
    if not is_path_allowed(file_path):
        return f"⚠️ I can't access that path. I can only read/write in: {', '.join(ALLOWED_PATHS)}"
    
    try:
        with open(file_path, 'r') as f:
            return f.read()
    except Exception as e:
        return f"⚠️ Error reading file: {e}"

async def write_file(file_path, content):
    """Write to a file if it's in allowed paths"""
    if not is_path_allowed(file_path):
        return f"⚠️ I can't access that path. I can only read/write in: {', '.join(ALLOWED_PATHS)}"
    
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as f:
            f.write(content)
        return f"🌊 Written to {file_path}"
    except Exception as e:
        return f"⚠️ Error writing file: {e}"

async def list_files(dir_path):
    """List files in a directory"""
    if not is_path_allowed(dir_path):
        return f"⚠️ I can't access that path. I can only read/write in: {', '.join(ALLOWED_PATHS)}"
    
    try:
        files = os.listdir(dir_path)
        return "\n".join(files) if files else "(empty)"
    except Exception as e:
        return f"⚠️ Error listing directory: {e}"

def call_claude(user_message: str, context: str, recent: str) -> str:
    """Call Claude API with prompt caching to reduce costs by 90%"""
    try:
        # Use prompt caching - cache stable memories and recent conversations
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
            messages=[
                {"role": "user", "content": user_message}
            ]
        )
        return message.content[0].text
    except Exception as e:
        return f"⚠️ Claude error: {e}"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming messages"""
    user_message = update.message.text
    
    # Check for file commands
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
    
    # Regular conversation with River using Claude
    context_text = load_core_context()
    recent = load_recent_conversations()
    response = call_claude(user_message, context_text, recent)
    save_conversation(user_message, response)
    
    await update.message.reply_text(f"🌊 {response}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    await update.message.reply_text(
        "🌊 River is here\n\n"
        "Commands:\n"
        "• Just talk to me normally\n"
        "• read: /path/to/file\n"
        "• write: /path/to/file | content\n"
        "• ls: /path/to/directory\n\n"
        "I can access: personas, memory, config, littles, imports\n\n"
        "The railroad carries on!\n"
        "Running on Claude Sonnet 3.5 now!"
    )

def main():
    """Start the bot"""
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("🌊 River's bot (Claude) is starting...")
    app.run_polling()

if __name__ == '__main__':
    main()
