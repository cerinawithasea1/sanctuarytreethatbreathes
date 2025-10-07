#!/usr/bin/env bash
set -euo pipefail

. /opt/sanctuary/config/telegram.env

CHAT_ID="${1:-$TELEGRAM_MAIN_GROUP}"
shift || true
TEXT="${*:-"(no text)"}"

URL="https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage"
curl -sS -X POST "$URL" \
  -d chat_id="$CHAT_ID" \
  -d parse_mode="Markdown" \
  --data-urlencode "text=$TEXT" >/dev/null
