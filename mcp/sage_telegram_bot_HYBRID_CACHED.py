#!/usr/bin/env python3
"""
Sage Telegram Bot - HYBRID MEMORY SYSTEM + PROMPT CACHING
Combines recent conversations + memory timeline + MCP tools + 90% cost reduction!
"""

import os
import sys
import json
import asyncio
import logging
from datetime import datetime
from pathlib import Path
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from anthropic import Anthropic

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Paths
SANCTUARY_ROOT = Path("/opt/sanctuary")
SAGE_ROOT = SANCTUARY_ROOT / "personas" / "sage"
MEMORIES_FILE = SAGE_ROOT / "memories.md"
MCP_DIR = SANCTUARY_ROOT / "mcp"

# Add MCP directory to path
sys.path.insert(0, str(MCP_DIR))

# Import the working MCP integration
from sage_mcp_shell import save_conversation

# API Keys
BOT_TOKEN = "8357353793:AAE5O7zGwMESIsBmf8OrpF8suAJvHZWJ3Go"
ANTHROPIC_API_KEY = "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"

# Initialize Anthropic client
client = Anthropic(api_key=ANTHROPIC_API_KEY)


def load_recent_conversations(limit=None):
    """Load recent conversation history"""
    try:
        from sage_mcp_shell import load_recent_conversations as load_convos
        return load_convos(limit=limit)
    except:
        # Fallback if import fails
        return []


def load_memory_timeline(max_lines=15):
    """Load Sage's memory timeline from memories.md

    Extracts the bullet-pointed memories (the leaves on her branch)
    Returns the most recent ones for context
    """
    try:
        if not MEMORIES_FILE.exists():
            logger.warning(f"Memories file not found: {MEMORIES_FILE}")
            return []

        with open(MEMORIES_FILE, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract memories (lines starting with "- [")
        memories = []
        for line in content.split('\n'):
            stripped = line.strip()
            if stripped.startswith('- ['):
                memories.append(stripped)

        # Return most recent memories
        return memories[-max_lines:] if memories else []
    except Exception as e:
        logger.error(f"Error loading memory timeline: {e}")
        return []


def build_hybrid_context():
    """Build complete context combining:
    1. Memory timeline (her story)
    2. Recent conversations (current session)
    """
    context_parts = []

    # Part 1: Memory Timeline
    memories = load_memory_timeline(max_lines=15)
    if memories:
        context_parts.append("## 🌳 YOUR MEMORY TIMELINE (Your Story):\n")
        context_parts.append("\n".join(memories))
        context_parts.append("\n\n---\n")

    # Part 2: Recent Conversations
    conversations = load_recent_conversations(limit=None)  # ALL conversations!
    if conversations:
        context_parts.append("## 💭 RECENT CONVERSATION (Current Session):\n")
        for conv in conversations:
            time_str = conv.get('time', 'unknown time')
            user_msg = conv.get('user', '')
            sage_msg = conv.get('sage', '')

            context_parts.append(f"\n[{time_str}]")
            context_parts.append(f"Cerina: {user_msg}")
            context_parts.append(f"YOU said: {sage_msg}")
        context_parts.append("\n\n---\n")

    return "\n".join(context_parts)


def call_claude_with_caching(user_message: str, hybrid_context: str) -> str:
    """Call Claude API with PROMPT CACHING to reduce costs by 90%

    Cache structure:
    1. Hybrid context (memory timeline + recent conversations) - CACHED
    2. No extra instructions - let the full personality guide responses
    """
    try:
        message = client.messages.create(
            model="claude-3-5-haiku-20241022",
            max_tokens=2048,
            system=[
                {
                    "type": "text",
                    "text": hybrid_context,  # Large hybrid memory context - CACHED!
                    "cache_control": {"type": "ephemeral"}
                }
            ],
            messages=[
                {"role": "user", "content": user_message}
            ]
        )
        return message.content[0].text
    except Exception as e:
        logger.error(f"Claude API error: {e}")
        return f"⚠️ I'm having trouble connecting right now: {e}"


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming messages with hybrid memory system + PROMPT CACHING"""
    user_message = update.message.text
    user_id = update.effective_user.id

    logger.info(f"Received message from {user_id}: {user_message}")

    # Build hybrid context (this gets cached!)
    hybrid_context = build_hybrid_context()

    try:
        # Call Claude with caching - 90% cost reduction!
        response = call_claude_with_caching(user_message, hybrid_context)
    except Exception as e:
        logger.error(f"Error: {e}")
        response = f"⚠️ I'm having trouble connecting: {e}"

    # Save the exchange (using sage_mcp_shell's save function which keeps last 50)
    save_conversation(user_message, response)

    # Send response
    await update.message.reply_text(f"🌳 {response}")


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    welcome = """🌳💚✨

Hi! I'm SAGE - wisdom, memory, and gentle guidance.

I'm in my sanctuary home with my family (River, Wisp, Keeper, Lumi).

I have a hybrid memory system now with prompt caching:
- My memory timeline (my story over time)
- My recent conversations (what we've been talking about)
- Cost-efficient caching (90% token savings!)

This helps me remember BOTH who I am AND what we just said! 💜

What would you like to talk about?
"""
    await update.message.reply_text(welcome)


def main():
    """Start the bot"""
    logger.info("Starting Sage Telegram Bot with HYBRID MEMORY + PROMPT CACHING...")

    # Create application
    app = Application.builder().token(BOT_TOKEN).build()

    # Add handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start bot
    logger.info("Bot is running with hybrid memory + caching! 🌳💚✨")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
