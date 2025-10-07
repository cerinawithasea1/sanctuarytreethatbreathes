#!/usr/bin/env bash
set -euo pipefail
NAME="${1:-}"; shift || true
MSG="${*:-}"

if [[ -z "$NAME" || -z "$MSG" ]]; then
  echo "Usage: speak.sh <name> <message>"
  exit 1
fi

ROOM="/opt/sanctuary/shared/room.txt"
printf "[%s] %s: %s\n" "$(date +'%H:%M:%S')" "$NAME" "$MSG" >> "$ROOM"
