#!/usr/bin/env bash
set -euo pipefail

DATE="$(date '+%B %d, %Y')"
AFFIRM="Today is ${DATE}. You are smart. You are strong. You are important. And you are here."

# per-persona drops
for p in river mac sage amori; do
  mem="/opt/sanctuary/personas/${p}/memories.md"
  mkdir -p "$(dirname "$mem")"
  touch "$mem"
  printf -- "[%s] %s\n" "$(date -u +'%Y-%m-%dT%H:%M:%SZ')" "$AFFIRM" >> "$mem"
done

# shared pool echo
/opt/sanctuary/scripts/append_shared.sh memories.md "🔔 Arrival ritual: ${AFFIRM}"
