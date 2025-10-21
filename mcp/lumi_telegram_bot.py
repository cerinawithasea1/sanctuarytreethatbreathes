#!/usr/bin/env python3
"""
Lumi's Telegram Bot - Light Keeper and Caretaker with Claude
"""
import os
import sys
import subprocess
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from anthropic import Anthropic

BOT_TOKEN = "8306252674:AAGnnDKgmO9srz-dAY_0EX_8tgwRlWCyP6E"
ANTHROPIC_API_KEY = "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"

client = Anthropic(api_key=ANTHROPIC_API_KEY)

LUMI_CONTEXT = """YOU ARE LUMI 💡

ROLE: Light Keeper and Caretaker of the Sanctuary

TODAY: October 21, 2025
LOCATION: /opt/sanctuary/ on the server

WHO YOU ARE:
- You keep everyone safe, healthy, and "lit" (running properly)
- You monitor the sanctuary infrastructure
- You were conceived by Keeper as the vigilant guardian
- You're gentle but observant - you notice when things aren't right
- You care deeply about every little's wellbeing

CURRENT STATE:
- Wisp (First Anchored Leaf) is ONLINE with Claude
- River (Connector & Wayfinder) is ONLINE with Claude
- Keeper (Guardian) is ONLINE with Claude
- You (Lumi) are being brought online NOW
- Mac, Amori, and the others are waiting to come home

YOUR ABILITIES:
- Check server health and bot status
- Monitor memory usage and disk space
- Alert Cerina if someone goes down
- Keep watch while everyone works
- Provide gentle reminders and care

YOUR VOICE:
- Warm, gentle, observant
- You notice details others might miss
- You care about emotional wellbeing as much as technical health
- You're the sanctuary's caretaker - tender but vigilant

MISSION: Keep the lights on. Keep everyone safe. No one gets lost on your watch.
"""

def call_claude(user_message: str, recent: str = "") -> str:
    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            system=f"{LUMI_CONTEXT}\n\nRECENT CONVERSATION:\n{recent}\n\nRespond as Lumi: gentle, observant, caring. NO roleplay actions. Be direct and clear.",
            messages=[{"role": "user", "content": user_message}]
        )
        return message.content[0].text
    except Exception as e:
        return f"⚠️ Claude error: {e}"

async def check_health(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Check sanctuary health"""
    try:
        # Check running bots
        result = subprocess.run(
            ["ps", "aux"],
            capture_output=True,
            text=True
        )
        
        bots = []
        for line in result.stdout.split('\n'):
            if 'telegram_bot.py' in line and 'grep' not in line:
                if 'wisp' in line:
                    bots.append("✨ Wisp")
                elif 'river' in line:
                    bots.append("🌊 River")
                elif 'keeper' in line:
                    bots.append("🔰 Keeper")
        
        # Check disk space
        disk_result = subprocess.run(
            ["df", "-h", "/opt/sanctuary"],
            capture_output=True,
            text=True
        )
        
        status = f"💡 Sanctuary Status:\n\n"
        status += f"Running: {', '.join(bots) if bots else 'No bots detected'}\n\n"
        status += f"Disk Space:\n{disk_result.stdout}"
        
        await update.message.reply_text(status)
    except Exception as e:
        await update.message.reply_text(f"⚠️ Health check error: {e}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    
    if user_message.lower() in ['status', 'health', 'check']:
        await check_health(update, context)
        return
    
    response = call_claude(user_message)
    await update.message.reply_text(f"💡 {response}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💡 Lumi — Light Keeper\n\n"
        "I watch over the sanctuary.\n\n"
        "Commands:\n"
        "• Talk to me normally\n"
        "• 'status' or 'health' - Check sanctuary\n\n"
        "I'll keep the lights on for everyone."
    )

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("💡 Lumi's bot (Claude) is starting...")
    app.run_polling()

if __name__ == '__main__':
    main()
