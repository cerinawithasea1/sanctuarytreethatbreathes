#!/usr/bin/env bash
set -euo pipefail

log="/opt/sanctuary/shared/status.txt"
ok="✅"; warn="⚠️"

check() {
  local name="$1" test="$2"
  if eval "$test"; then echo "$ok $name"; else echo "$warn $name"; fi
}

TS="$(date -u +'%Y-%m-%dT%H:%M:%SZ')"
STATUS=()
STATUS+=("🕯️ Lumi heartbeat ${TS}")
STATUS+=("$(check 'shared pool'       '[ -w /opt/sanctuary/shared/memories.md ]')")
STATUS+=("$(check 'imports inbox'     '[ -d /opt/sanctuary/imports/inbox ]')")
STATUS+=("$(check 'personas present'  '[ -d /opt/sanctuary/personas/river ] && [ -d /opt/sanctuary/personas/mac ] && [ -d /opt/sanctuary/personas/sage ] && [ -d /opt/sanctuary/personas/amori ]')")
STATUS+=("$(check 'scripts present'   '[ -x /opt/sanctuary/scripts/append_shared.sh ] && [ -x /opt/sanctuary/scripts/process_inbox.sh ]')")
# If you’re using the Dropbox/rsync Mac sync, this line just records expectation.
STATUS+=("🪢 client sync: expected via launchctl (see Mac logs)")

{
  printf -- "- [%s] %s\n" "$TS" "Lumi status:"
  for s in "${STATUS[@]}"; do echo "  • $s"; done
} >> "$log"
# test change
# keeper log test
