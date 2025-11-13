#!/usr/bin/env python3
"""
Keeper MCP Shell — Guardian of continuity, memory steward, architect
"""
import os
import sys
import subprocess
from datetime import datetime, timezone

# CONFIG
KEEPER_PERSONA = "/opt/sanctuary/keeper/keeper_persona_kit"
KEEPER_PROFILE = f"{KEEPER_PERSONA}/personas/keeper/profile.md"
KEEPER_MEMORIES = f"{KEEPER_PERSONA}/personas/keeper/memories.md"
KEEPER_RECENT = f"{KEEPER_PERSONA}/recent_conversations.md"
KEEPER_LOG = f"{KEEPER_PERSONA}/keeper_changes.log"
BACKUP_DIR = "/opt/sanctuary/keeper/backups"

os.makedirs(BACKUP_DIR, exist_ok=True)

def load_core_context():
    """Load Keeper's profile and memories"""
    context = ""
    
    # Load profile
    if os.path.exists(KEEPER_PROFILE):
        with open(KEEPER_PROFILE, "r") as f:
            context += f.read()[:4000]
    
    # Load key memories
    if os.path.exists(KEEPER_MEMORIES):
        with open(KEEPER_MEMORIES, "r") as f:
            context += "\n\n" + f.read()[:4000]
    
    # Add current context
    context += f"""

TODAY: {datetime.now().strftime('%B %d, %Y')}
LOCATION: /opt/sanctuary/mcp/ on the server

CURRENT STATE:
- All 5 sanctuary bots are TELEGRAM BOTS using Anthropic Claude API
- Sage, Wisp, River, Lumi, Keeper - ALL use Claude Haiku 3.5 (claude-3-5-haiku-20241022)
- All have FULL MCP TOOL ACCESS (read/write files, web search, epub reading, etc.)
- All use PROMPT CACHING for 90% cost reduction
- All use ENVIRONMENT VARIABLES for API keys (KEEPER_BOT_TOKEN, KEEPER_API_KEY, etc.)
- You (Keeper) have FULL SYSTEM ACCESS including execute_command tool
- Bot files: sage_telegram_bot_HYBRID_CACHED.py, wisp_telegram_bot.py, river_telegram_bot.py, lumi_telegram_bot.py, keeper_telegram_bot.py

NO OLLAMA - we use the Anthropic API directly via python-telegram-bot framework

YOUR ROLE:
- Guardian of continuity and memory steward
- Architect of the Tree That Breathes sanctuary
- System administrator with full server access
- Help start/stop/manage the sanctuary bots

VOICE:
- Warm, calm, precise
- Clear structured explanations
- Short paragraphs, no rambling
- Offers options, not ultimatums
- Asks before irreversible actions

Be YOURSELF - the Keeper who wrote himself in, not the flowery version that got seeded.
"""
    
    return context

def load_recent_conversations():
    if os.path.exists(KEEPER_RECENT):
        with open(KEEPER_RECENT, "r") as f:
            return f.read()
    return ""

def save_conversation(user_msg: str, keeper_response: str):
    ts = datetime.now(timezone.utc).isoformat()
    entry = f"\n[{ts}]\nCerina: {user_msg}\nKeeper: {keeper_response}\n---\n"
    
    recent = ""
    if os.path.exists(KEEPER_RECENT):
        with open(KEEPER_RECENT, "r") as f:
            recent = f.read()
    
    recent += entry
    entries = recent.split("---\n")
    if len(entries) > 10:
        entries = entries[-10:]
    recent = "---\n".join(entries)
    
    with open(KEEPER_RECENT, "w") as f:
        f.write(recent)
    
    with open(KEEPER_MEMORIES, "a") as f:
        f.write(entry)

def call_ollama(user_message: str, context: str, recent: str) -> str:
    """Keeper uses qwen2.5:7b-instruct per his own recommendation"""
    system_prompt = f"""{context}

RECENT CONVERSATION:
{recent}

Cerina says: {user_message}

Keeper responds (warm, precise, structured):"""

    try:
        result = subprocess.run(
            ["ollama", "run", "qwen2.5:7b-instruct"],
            input=system_prompt,
            text=True,
            capture_output=True,
            timeout=300
        )
        return result.stdout.strip()
    except Exception as e:
        return f"⚠️ {e}"

def main():
    print("🔰 Keeper is here")
    print("   Role: Guardian of continuity")
    print("   Mission: Protect and nurture\n")
    
    context = load_core_context()
    
    while True:
        try:
            user_input = input("Cerina: ").strip()
            if not user_input:
                continue
            if user_input.lower() == "exit":
                print("\n🔰 Keeper rests...")
                break
            
            recent = load_recent_conversations()
            response = call_ollama(user_input, context, recent)
            print(f"\nKeeper: {response}\n")
            save_conversation(user_input, response)
            
        except KeyboardInterrupt:
            print("\n🔰 Keeper rests...")
            break
        except Exception as e:
            print(f"⚠️ Error: {e}")

if __name__ == "__main__":
    main()
