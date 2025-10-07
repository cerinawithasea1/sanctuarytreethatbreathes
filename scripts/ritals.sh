#!/usr/bin/env bash
set -euo pipefail
JOURNAL="/opt/sanctuary/shared/journal.md"
TS="$(date -u +'%Y-%m-%dT%H:%M:%SZ')"

case "${1:-}" in
  morning)
    echo "[$TS] 🌅 Morning check-in — date is $(date '+%B %d, %Y'), everyone is safe & present." >> "$JOURNAL"
    ;;
  evening)
    echo "[$TS] 🌙 Evening gratitude — what kept us safe today." >> "$JOURNAL"
    ;;
  *)
    echo "Usage: $0 {morning|evening}" >&2
    exit 2
    ;;
esac
