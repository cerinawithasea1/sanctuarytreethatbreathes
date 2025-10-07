#!/usr/bin/env bash
set -euo pipefail

# Config
MEMORIES="/opt/sanctuary/shared/memories.md"
LOG="/opt/sanctuary/logs/note.log"
SEND="/opt/sanctuary/scripts/send_to_telegram.sh"
ENV="/opt/sanctuary/config/telegram.env"

# Load Telegram variables
set -a
source "$ENV"
set +a

# Chat ID (optional arg, fallback to TELEGRAM_MAIN_GROUP)
CHAT_ID="${1:-$TELEGRAM_MAIN_GROUP}"

# If the first argument looks like a number, treat it as chat_id and shift
if [[ "$CHAT_ID" =~ ^-?[0-9]+$ ]]; then
  shift || true
else
  CHAT_ID="$TELEGRAM_MAIN_GROUP"
fi

# Require a message
if [[ $# -eq 0 ]]; then
  echo "Usage: $0 [chat_id] <message>"
  exit 1
fi

TEXT="$*"

# Make sure directories exist
mkdir -p "$(dirname "$MEMORIES")" "$(dirname "$LOG")"

# Append to memory and log
ts=$(date -u +'%Y-%m-%dT%H:%M:%SZ')
echo "- [$ts] $TEXT" >> "$MEMORIES"
echo "[$ts] noted: $TEXT" >> "$LOG"

# Notify Telegram
"$SEND" "$CHAT_ID" "📝 Noted in the shared pool: $TEXT"
