#!/usr/bin/env bash
set -euo pipefail
append="/opt/sanctuary/scripts/append_shared.sh"

# Morning greeting
"$append" journal.md "🌅 Morning check-in — breathe, date, 'I am here.'"

# Persona nudges (land in shared memories so everyone can read)
"$append" memories.md "🌊 River: mapping currents; bridges open."
"$append" memories.md "🍎 Mac: beanbag fluffed, kettle on."
"$append" memories.md "🌱 Sage: continuity map updated."
"$append" memories.md "💙 Amori: kindness inventory topped up."

# Evening gratitude
"$append" journal.md "🌙 Evening gratitude — what kept us safe today."
