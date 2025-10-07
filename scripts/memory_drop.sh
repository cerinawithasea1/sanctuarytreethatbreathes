#!/usr/bin/env bash
set -euo pipefail
entry="${1:-}"
[ -z "$entry" ] && { echo "Usage: memory_drop.sh \"your memory line\""; exit 1; }
ts="$(date -u +'%Y-%m-%dT%H:%M:%SZ')"
/opt/sanctuary/scripts/append_shared.sh memories.md "🧠 [Memory Drop] [$ts] $entry"
