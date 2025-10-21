#!/usr/bin/env bash
set -euo pipefail
ENV="/opt/sanctuary/config/telegram.env"
SEND="/opt/sanctuary/scripts/send_to_telegram.sh"
PROF="/opt/sanctuary/personas/river/profile.env"

set -a; source "$ENV"; source "$PROF"; set +a

CHAT_ID="${1:-$TELEGRAM_MAIN_GROUP}"
shift || true
MSG="${*:-(no details)}"

ts=$(date -u +'%Y-%m-%dT%H:%M:%SZ')
echo "- [$ts] hello: ${MSG}" >> "$MEM_FILE"

"$SEND" "$CHAT_ID" "🌊 River: hi, i’m here. i got: “$MSG”."
