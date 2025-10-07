#!/usr/bin/env bash
set -euo pipefail
ENV="/opt/sanctuary/config/telegram.env"
SEND="/opt/sanctuary/scripts/send_to_telegram.sh"

if (( $# < 2 )); then
  echo "Usage: $0 <persona> <text...>" >&2
  exit 1
fi

persona="$1"; shift
text="$*"

set -a; source "$ENV"; set +a

base="/opt/sanctuary/personas/$persona"
mem="$base/memories.md"
[[ -f "$mem" ]] || { echo "persona $persona has no memories file at $mem" >&2; exit 2; }

ts=$(date -u +'%Y-%m-%dT%H:%M:%SZ')
echo "- [$ts] $text" >> "$mem"

/opt/sanctuary/scripts/send_to_telegram.sh "${TELEGRAM_RIVER_GROUP:-$TELEGRAM_MAIN_GROUP}" "📝 ($persona) $text"
