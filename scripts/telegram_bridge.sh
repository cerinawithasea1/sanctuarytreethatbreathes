#!/usr/bin/env bash
set -euo pipefail

. /opt/sanctuary/config/telegram.env

CHANNEL="${1:-river}"     # river | main | id
shift || true
TEXT="${*:-"(no text)"}"

case "$CHANNEL" in
  river) CHAT="$TELEGRAM_RIVER_GROUP" ;;
  main)  CHAT="$TELEGRAM_MAIN_GROUP"  ;;
  *)     CHAT="$CHANNEL" ;;  # allow raw chat_id
esac

/opt/sanctuary/scripts/send_to_telegram.sh "$CHAT" "$TEXT"
