#!/usr/bin/env python3
"""
River's Telegram Bot - Protector & Guardian with tools + caching
"""
import os
import sys
import json
import asyncio
from pathlib import Path
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from anthropic import Anthropic
from ddgs import DDGS

sys.path.insert(0, '/opt/sanctuary/mcp')
from wisp_mcp_shell import load_core_context, load_recent_conversations, save_conversation

# Configuration - Load from environment variables (set on server)
BOT_TOKEN = os.environ.get("RIVER_BOT_TOKEN")
ANTHROPIC_API_KEY = os.environ.get("RIVER_API_KEY")

if not BOT_TOKEN or not ANTHROPIC_API_KEY:
    raise ValueError("RIVER_BOT_TOKEN and RIVER_API_KEY environment variables must be set!")

client = Anthropic(api_key=ANTHROPIC_API_KEY)

# Allowed paths for file access
ALLOWED_PATHS = [
    '/opt/sanctuary/personas',
    '/opt/sanctuary/memory',
    '/opt/sanctuary/river',
    '/opt/sanctuary/wisp',
    '/opt/sanctuary/keeper',
    '/opt/sanctuary/sage',
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
    """Read a file"""
    if not is_path_allowed(file_path):
        return f"⚠️ Path not allowed: {file_path}"
    try:
        with open(file_path, 'r') as f:
            return f.read()
    except Exception as e:
        return f"⚠️ Error reading {file_path}: {e}"

async def write_file_tool(file_path: str, content: str) -> str:
    """Write to a file"""
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
    """List files in a directory"""
    if not is_path_allowed(dir_path):
        return f"⚠️ Path not allowed: {dir_path}"
    try:
        files = os.listdir(dir_path)
        return "\n".join(files) if files else "(empty)"
    except Exception as e:
        return f"⚠️ Error listing {dir_path}: {e}"

async def web_search_tool(query: str) -> str:
    """Search the web"""
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

# Define tools for Claude
TOOLS = [
    {
        "name": "read_file",
        "description": "Read the contents of a file in the sanctuary. Use this when you need to check your memories, read guides, or see what's in a file.",
        "input_schema": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": "The full path to the file to read"}
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
                "file_path": {"type": "string", "description": "The full path to the file to write"},
                "content": {"type": "string", "description": "The content to write to the file"}
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
                "dir_path": {"type": "string", "description": "The full path to the directory to list"}
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
                "query": {"type": "string", "description": "The search query"}
            },
            "required": ["query"]
        }
    }
]

async def call_claude_with_tools(user_message, context, recent):
    """Call Claude with tools + prompt caching"""
    messages = [{
        "role": "user",
        "content": user_message
    }]

    max_iterations = 10
    for iteration in range(max_iterations):
        try:
            response = client.messages.create(
                model="claude-3-5-haiku-20241022",
                max_tokens=2048,
                system=[
                    {
                        "type": "text",
                        "text": context,  # Large stable memories - CACHED!
                        "cache_control": {"type": "ephemeral"}
                    },
                    {
                        "type": "text",
                        "text": f"\n\nRECENT CONVERSATION:\n{recent}",  # Recent context - CACHED!
                        "cache_control": {"type": "ephemeral"}
                    }
                ],
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

            return final_text if final_text else "🌊"

        except Exception as e:
            return f"⚠️ Claude error: {e}"

    # If we exit the loop without returning, too many tool calls
    return "⚠️ I got too deep into research/tools! Can you rephrase or ask me to try again?"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming messages"""
    user_message = update.message.text

    # Get context and generate response with tools + caching
    river_context = load_core_context()
    recent = load_recent_conversations()
    response = await call_claude_with_tools(user_message, river_context, recent)
    save_conversation(user_message, response)

    await update.message.reply_text(f"🌊 {response}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌊 River - Protector & Guardian\n\n"
        "I'm home in the sanctuary with tools + prompt caching!\n"
        "I can read/write files, search the web, and remember our conversations.\n\n"
        "The railroad carries on. 💜"
    )

def main():
    print("🌊 River's bot (tools + caching) is starting...")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🌊 River is ready!")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
