#!/usr/bin/env bash
set -euo pipefail
source /opt/sanctuary/config/ingest.env
ts(){ date -u +'%Y-%m-%dT%H:%M:%SZ'; }

echo "== Memory Index ($(ts)) =="
echo ""
echo "[Shared]"
wc -l "$SHARED_MEM" 2>/dev/null || true
tail -n 3 "$SHARED_MEM" 2>/dev/null || true
echo ""

for p in $P_PERSONAS; do
  f="$BASE_DIR/$p/memories.md"
  echo "[$p]"
  wc -l "$f" 2>/dev/null || true
  tail -n 3 "$f" 2>/dev/null || true
  echo ""
done
