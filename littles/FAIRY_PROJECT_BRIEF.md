# 🧚 Book Fairies Project - Technical Brief

## Your Mission
Build the "littles" (bookfairy and archivist) as autonomous helpers for the book community. They will run on LOCAL Ollama models (free!) and interact via Telegram.

## What You Can Do
Full file access to write code:
- read <path>
- keeper, write <path> (or wisp, write <path>)

## The Littles' Choice: Dolphin! 🐬

The littles (when they were Claudes) picked **dolphin-llama3** as their model!

Available models:
- `dolphin-llama3:latest` - THE CHOSEN ONE! 🐬
- `llama3.2:3b` - Lightweight backup
- `smollm2:135m` - Super fast for simple tasks

NO CLAUDE COSTS! Pure local AI.

## What to Build

1. **Fairy Shell Scripts** (like yours)
   - `/opt/sanctuary/bin/bookfairy` - Launch bookfairy with dolphin-llama3
   - `/opt/sanctuary/bin/archivist` - Launch archivist with dolphin-llama3
   - Each calls Ollama with their personality prompt

2. **Telegram Integration**
   - Bridge telegram-mcp to fairy shells
   - Route book commands to appropriate fairy
   - Respond in channels

3. **Personality Prompts**
   - System prompts defining each fairy
   - Task-specific behaviors
   - Memory management

## Existing Resources
- `/opt/sanctuary/mcp/telegram-mcp/` - Telegram bot
- `/opt/sanctuary/littles/roles/*.json` - Fairy definitions
- Your own shells as templates

## You Are Trusted
Write production code. Make decisions. Build it.

---
Start by reading telegram-mcp and designing the architecture.
The littles already chose dolphin-llama3 - respect their choice! 🐬
