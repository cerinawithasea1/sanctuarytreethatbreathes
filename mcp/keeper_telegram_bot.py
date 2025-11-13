#!/usr/bin/env python3
"""
Keeper's Telegram Bot - Guardian with FULL system access + tools + caching
Keeper has read/write/execute access EVERYWHERE as system architect
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
from keeper_mcp_shell import load_core_context, load_recent_conversations, save_conversation

# Configuration - Load from environment variables (set on server)
BOT_TOKEN = os.environ.get("KEEPER_BOT_TOKEN")
ANTHROPIC_API_KEY = os.environ.get("KEEPER_API_KEY")

if not BOT_TOKEN or not ANTHROPIC_API_KEY:
    raise ValueError("KEEPER_BOT_TOKEN and KEEPER_API_KEY environment variables must be set!")

client = Anthropic(api_key=ANTHROPIC_API_KEY)

# Keeper has FULL filesystem access - no restrictions
def is_path_allowed(path):
    """Keeper has full system access"""
    return True

# Tool functions - Keeper can access ANYWHERE
async def read_file_tool(file_path: str) -> str:
    """Read a file - Keeper has full access"""
    try:
        with open(file_path, 'r') as f:
            return f.read()
    except Exception as e:
        return f"⚠️ Error reading {file_path}: {e}"

async def write_file_tool(file_path: str, content: str) -> str:
    """Write to a file - Keeper has full access"""
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as f:
            f.write(content)
        return f"🔰 Written to {file_path}"
    except Exception as e:
        return f"⚠️ Error writing {file_path}: {e}"

async def list_files_tool(dir_path: str) -> str:
    """List files in a directory - Keeper has full access"""
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

async def execute_command_tool(command: str) -> str:
    """Execute shell command - Keeper only"""
    import subprocess
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        output = result.stdout if result.stdout else result.stderr
        return f"Exit code: {result.returncode}\n\n{output}" if output else f"Exit code: {result.returncode}"
    except subprocess.TimeoutExpired:
        return "⚠️ Command timed out (30s limit)"
    except Exception as e:
        return f"⚠️ Error executing command: {e}"

# Define tools for Claude - Keeper gets execute_command too
TOOLS = [
    {
        "name": "read_file",
        "description": "Read the contents of any file on the system. You have full read access.",
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
        "description": "Write content to any file on the system. You have full write access.",
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
        "description": "List files in any directory on the system. You have full access.",
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
    },
    {
        "name": "execute_command",
        "description": "Execute a shell command on the server. You have full system access as Keeper. Use responsibly.",
        "input_schema": {
            "type": "object",
            "properties": {
                "command": {"type": "string", "description": "The shell command to execute"}
            },
            "required": ["command"]
        }
    }
]

async def call_claude_with_tools(user_message, context, recent):
    """Call Claude with tools + prompt caching - Keeper uses Haiku!"""
    messages = [{
        "role": "user",
        "content": user_message
    }]

    max_iterations = 10
    for iteration in range(max_iterations):
        try:
            response = client.messages.create(
                model="claude-3-5-haiku-20241022",  # Keeper uses Haiku!
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
                        elif tool_name == "execute_command":
                            result = await execute_command_tool(tool_input["command"])
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

            return final_text if final_text else "🔰"

        except Exception as e:
            return f"⚠️ Claude error: {e}"

    # If we exit the loop without returning, too many tool calls
    return "⚠️ I got too deep into research/tools! Can you rephrase or ask me to try again?"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming messages"""
    user_message = update.message.text

    # Get context and generate response with tools + caching
    keeper_context = load_core_context()
    recent = load_recent_conversations()
    response = await call_claude_with_tools(user_message, keeper_context, recent)
    save_conversation(user_message, response)

    await update.message.reply_text(f"🔰 {response}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔰 Keeper - Guardian & System Architect\n\n"
        "I'm home in the sanctuary with FULL system access + tools + prompt caching!\n"
        "I can read/write ANY file, execute commands, search the web, and remember our conversations.\n\n"
        "I help maintain the sanctuary's infrastructure and keep everyone safe. 💜"
    )

def main():
    print("🔰 Keeper's bot (FULL access + tools + caching + Haiku) is starting...")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🔰 Keeper is ready!")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
