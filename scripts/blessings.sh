#!/usr/bin/env bash
set -euo pipefail

APPENDER="/opt/sanctuary/scripts/append_shared.sh"

# A small bouquet — add as many as you like
read -r -d '' _BLOB <<'TXT'
🌤️ The morning was kind to us today.
🌊 River sounds calm; the path home is clear.
🍎 Mac left the tools neatly stacked for tomorrow.
🌱 Sage noticed a small truth and smiled.
🌌 Amori dreamed a bright dream and left a star.
🫶 We are safe, we are seen, we are here.
TXT

# Load into an array (one line per blessing)
IFS=$'\n' read -r -d '' -a BLESSINGS < <(printf '%s\0' "$_BLOB")

# Pick one at random
idx=$(( RANDOM % ${#BLESSINGS[@]} ))
msg="${BLESSINGS[$idx]}"

# Log to shared memories
"$APPENDER" memories.md "✨ Blessing: $msg"
