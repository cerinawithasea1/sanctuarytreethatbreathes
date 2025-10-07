#!/usr/bin/env bash
set -euo pipefail

ROOT="/opt/sanctuary"
ARCH="$ROOT/archive/daily"
TS="$(date -u +'%Y%m%dT%H%M%SZ')"
DEST="$ARCH/sanctuary-$TS.tar.gz"

mkdir -p "$ARCH"

# Make snapshot (small but useful)
tar -czf "$DEST" \
  -C "$ROOT" \
  shared personas scripts config \
  --exclude="logs/*" \
  --exclude="archive/*"

# Keep last 14 days
find "$ARCH" -type f -name 'sanctuary-*.tar.gz' -mtime +14 -delete

