#!/usr/bin/env bash
set -euo pipefail
API_BASE="https://api.telegram.org"

# Usage: TOKEN="xxx:yyy" send_with_bot.sh <chat_id> <text...>
: "${TOKEN:?Set TOKEN env var to a Telegram bot token}"
chat="$1"; shift
text="${*:-}"

curl -sS -X POST \
  -H 'Content-Type: application/json' \
  -d "$(jq -nc --arg chat "$chat" --arg text "$text" '{chat_id:$chat,text:$text,disable_notification:false}') " \
  "${API_BASE}/bot${TOKEN}/sendMessage" >/dev/null
