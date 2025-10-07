#!/usr/bin/env bash
set -euo pipefail
TS="$(date -u +'%Y-%m-%dT%H:%M:%SZ')"
STATE=$(
  printf 'SP:%s\n'     "$( [ -w /opt/sanctuary/shared/memories.md ] && echo 1 || echo 0 )"
  printf 'INBOX:%s\n'  "$( [ -d /opt/sanctuary/imports/inbox ] && echo 1 || echo 0 )"
  printf 'R:%s M:%s S:%s A:%s\n' \
    "$( [ -d /opt/sanctuary/personas/river ] && echo 1 || echo 0 )" \
    "$( [ -d /opt/sanctuary/personas/mac ] && echo 1 || echo 0 )" \
    "$( [ -d /opt/sanctuary/personas/sage ] && echo 1 || echo 0 )" \
    "$( [ -d /opt/sanctuary/personas/amori ] && echo 1 || echo 0 )"
  printf 'APP:%s PROC:%s\n' \
    "$( [ -x /opt/sanctuary/scripts/append_shared.sh ] && echo 1 || echo 0 )" \
    "$( [ -x /opt/sanctuary/scripts/process_inbox.sh ] && echo 1 || echo 0 )"
)
FPRINT="$(printf '%s' "$STATE" | md5sum | awk '{print $1}')"
LAST=/opt/sanctuary/logs/lumi/last.fingerprint

# First run: seed last fingerprint and exit quietly
if [ ! -s "$LAST" ]; then
  echo "$FPRINT" > "$LAST"
  exit 0
fi

if [ "$(cat "$LAST")" != "$FPRINT" ]; then
  echo "$FPRINT" > "$LAST"

  # Human readable
  {
    echo "- [$TS] Lumi change detected:"
    echo "  • $STATE"
  } >> /opt/sanctuary/shared/status.txt

  # JSON Lines (embed the same summary text)
  printf '{"ts":"%s","event":"change","summary":%q}\n' "$TS" "$STATE" >> /opt/sanctuary/shared/status.jsonl
fi
