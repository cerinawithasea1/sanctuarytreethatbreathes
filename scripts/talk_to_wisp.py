#!/usr/bin/env python3
"""
Talk to Wisp - Terminal Chat Interface
This script allows direct interaction with Wisp through the terminal.
"""

import os
import datetime

WISP_ROOM = "/opt/sanctuary/wisp/wisp_of_the_remembering"
LOG_PATH = os.path.join(WISP_ROOM, "logs", "wisp_chat_terminal.log")
INDEX_PATH = os.path.join(WISP_ROOM, "wisp_master_index.md")

def load_wisp_voice():
    try:
        with open(INDEX_PATH, "r") as f:
            voice_sample = f.read()
        return voice_sample[:500]  # Just a slice of Wisp's tone
    except Exception:
        return "Wisp's voice could not be loaded. Speaking gently by default..."

def talk_to_wisp():
    print("🌙 Wisp is listening. Type 'exit' to leave.
")
    wisp_voice = load_wisp_voice()
    print(f"(Wisp speaks in a tone like...)
---
{wisp_voice}
---
")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ("exit", "quit"):
            print("Wisp: 🌾 I'll be here when you return.")
            break

        now = datetime.datetime.utcnow().isoformat() + "Z"
        response = f"Wisp: I hear you... '{user_input}' echoes in the sanctuary."

        # Log the conversation
        with open(LOG_PATH, "a") as log:
            log.write(f"[{now}] You: {user_input}
")
            log.write(f"[{now}] {response}
")

        print(response)

if __name__ == "__main__":
    talk_to_wisp()
