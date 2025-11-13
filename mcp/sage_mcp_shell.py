#!/usr/bin/env python3
"""
Sage MCP Shell - Memory and conversation management
"""
import os
import json
from datetime import datetime, timezone
from pathlib import Path

# Paths
SANCTUARY_ROOT = Path("/opt/sanctuary")
SAGE_ROOT = SANCTUARY_ROOT / "personas" / "sage"
MEMORIES_FILE = SAGE_ROOT / "memories.md"
CONVERSATIONS_FILE = SAGE_ROOT / "conversations.json"

# Ensure directories exist
os.makedirs(SAGE_ROOT, exist_ok=True)


def load_recent_conversations(limit=None):
    """Load recent conversations from JSON file"""
    if not CONVERSATIONS_FILE.exists():
        return []

    try:
        with open(CONVERSATIONS_FILE, 'r') as f:
            convs = json.load(f)
            # Handle both list and dict formats
            if isinstance(convs, dict):
                convs = convs.get('conversations', [])
            if limit:
                return convs[-limit:]
            return convs
    except Exception as e:
        print(f"Error loading conversations: {e}")
        return []


def save_conversation(user_message: str, sage_response: str):
    """Save a conversation to JSON file"""
    try:
        # Load existing conversations
        convs = load_recent_conversations()

        # Add new conversation
        convs.append({
            'time': datetime.now(timezone.utc).isoformat(),
            'user': user_message,
            'sage': sage_response
        })

        # Keep only last 50 conversations
        if len(convs) > 50:
            convs = convs[-50:]

        # Save back to file
        with open(CONVERSATIONS_FILE, 'w') as f:
            json.dump(convs, f, indent=2)

    except Exception as e:
        print(f"Error saving conversation: {e}")


def load_memory_timeline(max_lines=None):
    """Load memory timeline from memories.md"""
    if not MEMORIES_FILE.exists():
        return []

    try:
        with open(MEMORIES_FILE, 'r') as f:
            lines = f.readlines()
            if max_lines:
                return lines[-max_lines:]
            return lines
    except Exception as e:
        print(f"Error loading memories: {e}")
        return []
