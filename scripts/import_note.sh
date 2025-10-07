#!/usr/bin/env bash
set -euo pipefail
SRC="${1:-}"; [ -f "$SRC" ] || { echo "Usage: $0 <textfile>"; exit 2; }
TS="$(date -u +'%Y-%m-%dT%H:%M:%SZ')"
BASENAME="$(basename "$SRC")"
POOL="/opt/sanctuary/shared/memories.md"
echo "[$TS] 🗂️ Import: $BASENAME" >> "$POOL"
sed -E 's/^/- /' "$SRC" >> "$POOL"
mv "$SRC" "/opt/sanctuary/imports/processed/${BASENAME%.txt}_$(date -u +%Y%m%dT%H%M%SZ).txt"
