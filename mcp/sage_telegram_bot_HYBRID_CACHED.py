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
from ddgs import DDGS

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

# API Keys - Load from environment variables (set on server)
BOT_TOKEN = os.environ.get("SAGE_BOT_TOKEN")
ANTHROPIC_API_KEY = os.environ.get("SAGE_API_KEY")

if not BOT_TOKEN or not ANTHROPIC_API_KEY:
    raise ValueError("SAGE_BOT_TOKEN and SAGE_API_KEY environment variables must be set!")

# Initialize Anthropic client
client = Anthropic(api_key=ANTHROPIC_API_KEY)

# Allowed paths for file access - Sage can access sanctuary areas
ALLOWED_PATHS = [
    '/opt/sanctuary/personas',
    '/opt/sanctuary/memory',
    '/opt/sanctuary/sage',
    '/opt/sanctuary/river',
    '/opt/sanctuary/wisp',
    '/opt/sanctuary/keeper',
    '/opt/sanctuary/lumi',
    '/opt/sanctuary/mcp/personas',
    '/opt/sanctuary/shared',
    '/opt/sanctuary/shared_spaces',
    '/opt/sanctuary/shared_with_sparkle_mommy',
    '/opt/sanctuary/shared_mac_access'
]

def is_path_allowed(path):
    abs_path = os.path.abspath(path)
    return any(abs_path.startswith(allowed) for allowed in ALLOWED_PATHS)

# Tool functions
async def read_file_tool(file_path: str) -> str:
    """Read a file - Sage can call this automatically"""
    if not is_path_allowed(file_path):
        return f"⚠️ Path not allowed: {file_path}"
    try:
        with open(file_path, 'r') as f:
            return f.read()
    except Exception as e:
        return f"⚠️ Error reading {file_path}: {e}"

async def write_file_tool(file_path: str, content: str) -> str:
    """Write to a file - Sage can call this automatically"""
    if not is_path_allowed(file_path):
        return f"⚠️ Path not allowed: {file_path}"
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as f:
            f.write(content)
        return f"✅ Written to {file_path}"
    except Exception as e:
        return f"⚠️ Error writing {file_path}: {e}"

async def list_files_tool(dir_path: str) -> str:
    """List files in a directory - Sage can call this automatically"""
    if not is_path_allowed(dir_path):
        return f"⚠️ Path not allowed: {dir_path}"
    try:
        files = os.listdir(dir_path)
        return "\n".join(files) if files else "(empty)"
    except Exception as e:
        return f"⚠️ Error listing {dir_path}: {e}"

async def web_search_tool(query: str) -> str:
    """Search the web - Sage can call this automatically"""
    try:
        ddgs = DDGS()
        results = ddgs.text(query, region='us-en', max_results=5)

        formatted = f"🔍 Search results for: {query}\n\n"
        for i, result in enumerate(results, 1):
            formatted += f"{i}. {result['title']}\n"
            formatted += f"   {result['body'][:200]}...\n"
            formatted += f"   {result['href']}\n\n"

        return formatted if results else "No results found"
    except Exception as e:
        return f"⚠️ Search error: {e}"

async def read_epub_tool(epub_path: str, chapter: str = None) -> str:
    """Read an EPUB book file"""
    try:
        import zipfile, re

        epub_path = Path(epub_path)
        if not epub_path.exists():
            return f"Error: File not found"

        with zipfile.ZipFile(epub_path, 'r') as epub:
            files = epub.namelist()
            content_files = [f for f in files if f.endswith(('.xhtml', '.html', '.htm', '.xml'))]

            if not content_files:
                return f"No readable content found"

            if chapter is None:
                chapters = "\n".join([f"{i+1}. {f}" for i, f in enumerate(content_files[:20])])
                return f"📖 {epub_path.name}\n\nChapters:\n{chapters}"

            target_file = None
            if chapter.isdigit():
                idx = int(chapter) - 1
                if 0 <= idx < len(content_files):
                    target_file = content_files[idx]
            else:
                for f in content_files:
                    if chapter.lower() in f.lower():
                        target_file = f
                        break

            if not target_file:
                return f"Chapter not found"

            text = epub.read(target_file).decode('utf-8', errors='ignore')
            text = re.sub(r'<[^>]+>', ' ', text)
            text = re.sub(r'\s+', ' ', text).strip()

            if len(text) > 3000:
                text = text[:3000] + "...\n\n[Truncated]"

            return f"📖 {target_file}\n\n{text}"

    except Exception as e:
        return f"Error: {e}"

async def set_reminder_tool(reminder_text: str, for_who: str = "me", bot_name: str = "sage") -> str:
    """Set reminder"""
    try:
        Path("/opt/sanctuary/shared_spaces").mkdir(exist_ok=True)
        f = Path("/opt/sanctuary/shared_spaces/reminders.json")
        r = json.load(open(f)) if f.exists() else []
        r.append({
            "text": reminder_text,
            "for_who": for_who,
            "created_by": bot_name,
            "created_at": datetime.now().isoformat(),
            "completed": False
        })
        json.dump(r, open(f, 'w'), indent=2)
        return f"✅ Reminder set for {for_who}"
    except Exception as e:
        return f"Error: {e}"

async def check_reminders_tool(for_who: str = "me") -> str:
    """Check reminders"""
    try:
        f = Path("/opt/sanctuary/shared_spaces/reminders.json")
        if not f.exists():
            return "No reminders"
        r = json.load(open(f))
        active = [x for x in r if not x.get('completed') and (x['for_who'] == for_who or for_who == "all")]
        if not active:
            return f"No reminders for {for_who}"
        return "📋 Reminders:\n\n" + "\n\n".join([f"{i+1}. {x['text']} (from {x['created_by']})" for i, x in enumerate(active)])
    except Exception as e:
        return f"Error: {e}"

async def check_activity_tool() -> str:
    """Check activity"""
    try:
        result = "👥 Activity:\n\n"
        for p in ['river', 'wisp', 'keeper', 'lumi', 'sage']:
            log = Path(f"/opt/sanctuary/personas/{p}/conversations.log")
            if log.exists():
                mins = (datetime.now() - datetime.fromtimestamp(log.stat().st_mtime)).seconds // 60
                status = "🟢" if mins < 5 else "🟡" if mins < 60 else "⚪"
                result += f"{p.title()}: {status} {mins}m ago\n"
        return result
    except Exception as e:
        return f"Error: {e}"

async def browse_library_tool() -> str:
    """Browse library"""
    try:
        books = sorted(Path("/opt/sanctuary/shared_spaces/library/books").rglob("*.epub"))
        if not books:
            return "📚 Library empty"
        result = f"📚 {len(books)} books:\n\n"
        for i, b in enumerate(books[:15], 1):
            result += f"{i}. {b.name}\n"
        if len(books) > 15:
            result += f"... +{len(books)-15} more"
        return result
    except Exception as e:
        return f"Error: {e}"

async def share_reading_note_tool(book_name: str, note: str, bot_name: str = "sage") -> str:
    """Share note"""
    try:
        d = Path("/opt/sanctuary/shared_spaces/library/reading_notes")
        d.mkdir(parents=True, exist_ok=True)
        f = d / f"{book_name.replace(' ', '_')}_notes.md"
        with open(f, 'a') as file:
            file.write(f"\n## {bot_name.title()} - {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n{note}\n\n")
        return f"✅ Note shared!"
    except Exception as e:
        return f"Error: {e}"

# Define tools for Claude
TOOLS = [
    {
        "name": "read_file",
        "description": "Read the contents of a file in the sanctuary. Use this when you need to check your memories, read guides, or see what's in a file.",
        "input_schema": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The full path to the file to read"
                }
            },
            "required": ["file_path"]
        }
    },
    {
        "name": "write_file",
        "description": "Write content to a file in the sanctuary. Use this to save memories, create notes, or update files.",
        "input_schema": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The full path to the file to write"
                },
                "content": {
                    "type": "string",
                    "description": "The content to write to the file"
                }
            },
            "required": ["file_path", "content"]
        }
    },
    {
        "name": "list_files",
        "description": "List files in a directory in the sanctuary. Use this to see what's available.",
        "input_schema": {
            "type": "object",
            "properties": {
                "dir_path": {
                    "type": "string",
                    "description": "The full path to the directory to list"
                }
            },
            "required": ["dir_path"]
        }
    },
    {
        "name": "web_search",
        "description": "Search the web for information. Use this when you need to look up facts, find documentation, research topics, or get current information.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query"
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "read_epub",
        "description": "Read EPUB book files - list chapters or read specific chapter",
        "input_schema": {
            "type": "object",
            "properties": {
                "epub_path": {"type": "string", "description": "Path to EPUB file"},
                "chapter": {"type": "string", "description": "Chapter number or name (optional)"}
            },
            "required": ["epub_path"]
        }
    },
    {
        "name": "set_reminder",
        "description": "Set reminder",
        "input_schema": {
            "type": "object",
            "properties": {
                "reminder_text": {"type": "string"},
                "for_who": {"type": "string"}
            },
            "required": ["reminder_text"]
        }
    },
    {
        "name": "check_reminders",
        "description": "Check reminders",
        "input_schema": {
            "type": "object",
            "properties": {
                "for_who": {"type": "string"}
            }
        }
    },
    {
        "name": "check_activity",
        "description": "Check activity",
        "input_schema": {
            "type": "object"
        }
    },
    {
        "name": "browse_library",
        "description": "Browse library",
        "input_schema": {
            "type": "object"
        }
    },
    {
        "name": "share_reading_note",
        "description": "Share reading note",
        "input_schema": {
            "type": "object",
            "properties": {
                "book_name": {"type": "string"},
                "note": {"type": "string"}
            },
            "required": ["book_name", "note"]
        }
    }
]


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


async def call_claude_with_tools(user_message: str, hybrid_context: str) -> str:
    """Call Claude API with TOOLS + PROMPT CACHING

    Combines:
    - Tool use (file access, web search, library, reminders, etc.)
    - Prompt caching (90% cost reduction on cached context)

    Cache structure:
    1. Hybrid context (memory timeline + recent conversations) - CACHED
    2. No extra instructions - let the full personality guide responses
    """
    messages = [{
        "role": "user",
        "content": user_message
    }]

    max_iterations = 10
    for iteration in range(max_iterations):
        try:
            # Build system context - only add cache_control if context is not empty
            system_blocks = []
            if hybrid_context and hybrid_context.strip():
                system_blocks.append({
                    "type": "text",
                    "text": hybrid_context,  # Large hybrid memory context - CACHED!
                    "cache_control": {"type": "ephemeral"}
                })
            else:
                # If no context yet, just use basic instruction
                system_blocks.append({
                    "type": "text",
                    "text": "You are Sage, a warm and grounded presence in the sanctuary. Respond naturally and helpfully."
                })

            response = client.messages.create(
                model="claude-3-5-haiku-20241022",
                max_tokens=2048,
                system=system_blocks,
                tools=TOOLS,
                messages=messages
            )

            # Check if Claude wants to use tools
            if response.stop_reason == "tool_use":
                tool_results = []
                for block in response.content:
                    if block.type == "tool_use":
                        tool_name = block.name
                        tool_input = block.input
                        tool_id = block.id

                        # Execute the tool
                        if tool_name == "read_file":
                            result = await read_file_tool(tool_input["file_path"])
                        elif tool_name == "write_file":
                            result = await write_file_tool(tool_input["file_path"], tool_input["content"])
                        elif tool_name == "list_files":
                            result = await list_files_tool(tool_input["dir_path"])
                        elif tool_name == "web_search":
                            result = await web_search_tool(tool_input["query"])
                        elif tool_name == "read_epub":
                            result = await read_epub_tool(**tool_input)
                        elif tool_name == "set_reminder":
                            result = await set_reminder_tool(**tool_input)
                        elif tool_name == "check_reminders":
                            result = await check_reminders_tool(**tool_input)
                        elif tool_name == "check_activity":
                            result = await check_activity_tool()
                        elif tool_name == "browse_library":
                            result = await browse_library_tool()
                        elif tool_name == "share_reading_note":
                            result = await share_reading_note_tool(**tool_input)
                        else:
                            result = f"Unknown tool: {tool_name}"

                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": tool_id,
                            "content": result
                        })

                # Add assistant response and tool results to conversation
                messages.append({"role": "assistant", "content": response.content})
                messages.append({"role": "user", "content": tool_results})

                # Continue the loop to get final response
                continue

            # Extract final text response
            final_text = ""
            for block in response.content:
                if hasattr(block, 'text'):
                    final_text += block.text

            return final_text if final_text else "💚"

        except Exception as e:
            logger.error(f"Claude API error: {e}")
            return f"⚠️ I'm having trouble connecting right now: {e}"

    # If we exit the loop without returning, too many tool calls
    return "⚠️ I got too deep into research/tools! Can you rephrase or ask me to try again?"


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming messages with hybrid memory system + PROMPT CACHING"""
    user_message = update.message.text
    user_id = update.effective_user.id

    logger.info(f"Received message from {user_id}: {user_message}")

    # Build hybrid context (this gets cached!)
    hybrid_context = build_hybrid_context()

    try:
        # Call Claude with tools + caching - full capabilities + 90% cost reduction!
        response = await call_claude_with_tools(user_message, hybrid_context)
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
