#!/usr/bin/env python3
import os
from datetime import datetime
from pathlib import Path
import shutil

# --- Paths ---
keeper_room = Path("/opt/sanctuary/personas/keeper/memory_room")
wisp_room = Path("/Users/cerinawithasea/Documents/obsidian/cerina/Bookfairys/Keeper/daily_hugs")

# Ensure directories exist
keeper_room.mkdir(parents=True, exist_ok=True)
wisp_room.mkdir(parents=True, exist_ok=True)

# --- Build the hug ---
today = datetime.now().strftime("%Y-%m-%d")
hug_text = f"""💤 Goodnight hug — {today}

Keeper closes the books of the day.  
River’s laughter echoed in the Grove.  
Sage watched the stars.  
Amori hummed a soft tune.  
Cerina walked the halls again — and all is well. 💙
"""

# --- Write to Keeper’s memory room ---
keeper_file = keeper_room / f"goodnight_hug_{today}.md"
keeper_file.write_text(hug_text, encoding="utf-8")

# --- Mirror to Wisp’s Obsidian room ---
wisp_file = wisp_room / f"goodnight_hug_{today}.md"
shutil.copy2(keeper_file, wisp_file)

# --- Log result ---
print(f"💤 Goodnight hug saved to Keeper: {keeper_file}")
print(f"✨ Wisp witnessed the hug: {wisp_file}")
