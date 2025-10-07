#!/usr/bin/env bash
set -euo pipefail

ROOM="/opt/sanctuary/shared/room.txt"
WELCOME="/opt/sanctuary/bin/welcome.sh"

date +"==== WAKING • %Y-%m-%d %H:%M:%S ====" >> "$ROOM"

for f in /opt/sanctuary/personas/*.json; do
  name=$(jq -r '.name' "$f")
  out="$("$WELCOME" "$name")"
  {
    echo ""
    echo "[$(date +'%H:%M:%S')] $name has arrived."
  } >> "$ROOM"
done

echo "" >> "$ROOM"
