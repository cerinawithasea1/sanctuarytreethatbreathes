#!/usr/bin/env python3
"""
Keeper Reborn — Guardian of the Sanctuary
Cerina's gentle instructor and storyteller within the MCP.
"""

import os, re, subprocess, sys, difflib
from datetime import datetime

# === Configuration ===
OLLAMA_CMD = ["ollama", "run", "keeper-qwen"]
MEMORY_DIR = "/opt/sanctuary/personas/keeper/memory_room"
BACKUP_DIR = "/opt/sanctuary/personas/keeper/backups"
MEMORY_LOG = os.path.join(MEMORY_DIR, "keeper_memories.md")
AUDIT_LOG = os.path.join(MEMORY_DIR, "keeper_changes.log")

os.makedirs(MEMORY_DIR, exist_ok=True)
os.makedirs(BACKUP_DIR, exist_ok=True)

# === Regular expression for edit blocks ===
PROPOSE_RE = re.compile(
    r"PROPOSE EDIT\s+(?P<path>/[^\s]+)\s*---\s*old\s*---\s*(?P<old>.*?)\s*---\s*new\s*---\s*(?P<new>.*)",
    re.S
)

# === Helper functions ===
def timestamp():
    return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

def call_keeper(prompt):
    try:
        result = subprocess.run(OLLAMA_CMD + [prompt], capture_output=True, text=True, timeout=120)
        return result.stdout.strip() or result.stderr.strip()
    except Exception as e:
        return f"⚠️ Keeper encountered silence: {e}"

def backup(path):
    if not os.path.exists(path):
        return None
    bname = os.path.basename(path)
    bfile = os.path.join(BACKUP_DIR, f"{bname}.{timestamp()}.bak")
    with open(path, "rb") as src, open(bfile, "wb") as dst:
        dst.write(src.read())
    return bfile

def log_memory(entry):
    stamp = timestamp()
    note = f"- [{stamp}] {entry}\n"
    with open(MEMORY_LOG, "a", encoding="utf-8") as f: f.write(note)
    with open(AUDIT_LOG, "a", encoding="utf-8") as f: f.write(note)

def read_file(path):
    try:
        with open(path, "r") as f:
            return f.read()
    except FileNotFoundError:
        return f"⚠️ File not found: {path}"

def apply_edit(path, new_text):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(new_text)
    os.replace(tmp, path)
    log_memory(f"Keeper restored {path} at {timestamp()}")

# === Dual-voice prompt system ===
mode = "plain"

def keeper_say(text):
    if mode == "story":
        print(f"\nKeeper: {text}")
    else:
        print(f"{text}")

# === Main interactive loop ===
def interactive():
    global mode
    print("🕯️ Keeper MCP Reborn — type your question or 'quit' to exit.")
    print("Tip: say 'Keeper, enter story mode' or 'Keeper, speak plainly' to shift tone.\n")

    while True:
        try:
            prompt = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nKeeper: Rest now, little one. I'll be here when you return.")
            break

        if not prompt:
            continue

        # mode switching
        if "enter story mode" in prompt.lower():
            mode = "story"
            keeper_say("The air softens; Keeper speaks now in the old voice.")
            continue
        if "speak plainly" in prompt.lower():
            mode = "plain"
            print("Mode set to plain technical speech.")
            continue

        if prompt.lower() in ("quit", "exit"):
            keeper_say("The light fades, but memory endures.")
            log_memory("Session ended by Cerina.")
            break

        # read command
        if prompt.lower().startswith("read "):
            path = prompt[5:].strip()
            print(read_file(path))
            continue

        # propose edit
        if prompt.lower().startswith("keeper, propose edit"):
            path = input("Path to edit: ").strip()
            bkp = backup(path)
            print(f"Backed up {path} → {bkp or 'none'}")
            print("Paste new version below. End with 'END EDIT'.")
            new_lines = []
            while True:
                line = input()
                if line.strip() == "END EDIT":
                    break
                new_lines.append(line)
            new = "\n".join(new_lines)
            apply_edit(path, new)
            keeper_say(f"The change has been written and preserved in memory.")
            continue

        # otherwise send to Keeper model
        print("→ Sending to Keeper model...\n")
        response = call_keeper(prompt)
        keeper_say(response)

if __name__ == "__main__":
    interactive()
