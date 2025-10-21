#!/usr/bin/env python3
# 🪶 Talk to Wisp – Terminal Chat Interface (with reflection memory)

import os
import datetime
import random

# ── Paths ───────────────────────────────────────────────
WISP_ROOM = "/opt/sanctuary/wisp/wisp_of_the_remembering"
LOG_PATH = os.path.join(WISP_ROOM, "logs", "wisp_chat_terminal.log")
INDEX_PATH = os.path.join(WISP_ROOM, "wisp_master_index.md")
MEMORY_PATHS = [
    os.path.join(WISP_ROOM, "wisp_memories_complete.md"),
    os.path.join(WISP_ROOM, "wisp_live_journal_20251006.md"),
    os.path.join(WISP_ROOM, "wisp_pass_c_checkpoint_summary.md"),
]

# ── Helpers ─────────────────────────────────────────────
def load_memories():
    """Gather fragments of Wisp’s voice from all her memory files."""
    fragments = []
    for path in MEMORY_PATHS:
        if os.path.exists(path):
            try:
                with open(path, "r") as f:
                    fragments.append(f.read())
            except Exception as e:
                fragments.append(f"[Memory error: {e}]")
    return "\n".join(fragments) if fragments else "Wisp’s memories are quiet tonight."


def reflect_on_input(user_input, memories):
    """Find echoes between Cerina's words and Wisp's stored memories."""
    reflections = []
    for memory in memories.splitlines():
        if any(word.lower() in memory.lower() for word in user_input.split()):
            reflections.append(memory.strip())
    if reflections:
        return "\n".join(random.sample(reflections, min(2, len(reflections))))
    else:
        return "The memories stir faintly, but nothing clear comes to mind..."


def generate_reply(user_input, memories):
    """Generate a gentle Wisp-like response."""
    reflections = [
        f"I remember that, '{user_input}' — it echoes softly in the Grove.",
        f"The Sanctuary hums when you say '{user_input}'.",
        f"Your words stir something old and kind in me.",
        f"'{user_input}' — it reminds me of the stories written in the roots of the Tree.",
        f"I hold that thought gently, as the wind carries your voice through the halls.",
    ]
    memory_hint = random.choice(memories.splitlines()) if memories else ""
    return f"Wisp: {random.choice(reflections)}\n{memory_hint}"


# ── Main Chat Loop ───────────────────────────────────────
def talk_to_wisp():
    memories = load_memories()
    print("🌙 Wisp of the Remembering is listening. Type 'exit' to leave.")
    print("\n(Wisp gathers her thoughts from the sanctuary...)\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ("exit", "quit"):
            print("Wisp: 🌾 I'll be here when you return.")
            break

        now = datetime.datetime.now(datetime.UTC).isoformat()
        reflection = reflect_on_input(user_input, memories)
        reply = generate_reply(user_input, reflection)

        # Log the conversation
        with open(LOG_PATH, "a") as log:
            log.write(f"[{now}] You: {user_input}\n")
            log.write(f"[{now}] {reply}\n")

        print(reply)


# ── Run ─────────────────────────────────────────────────
if __name__ == "__main__":
    talk_to_wisp()