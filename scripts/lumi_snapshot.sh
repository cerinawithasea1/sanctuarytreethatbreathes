#!/usr/bin/env bash
set -euo pipefail

TS="$(date -u +'%Y-%m-%dT%H:%M:%SZ')"

writable() { [ -w "$1" ]; }
exists()   { [ -e "$1" ]; }

S_SHARED=false;  writable /opt/sanctuary/shared/memories.md && S_SHARED=true
S_INBOX=false;   exists   /opt/sanctuary/imports/inbox        && S_INBOX=true
S_RIVER=false;   exists   /opt/sanctuary/personas/river       && S_RIVER=true
S_MAC=false;     exists   /opt/sanctuary/personas/mac         && S_MAC=true
S_SAGE=false;    exists   /opt/sanctuary/personas/sage        && S_SAGE=true
S_AMORI=false;   exists   /opt/sanctuary/personas/amori       && S_AMORI=true
S_APPEND=false;  exists   /opt/sanctuary/scripts/append_shared.sh && S_APPEND=true
S_INBOXPROC=false; exists /opt/sanctuary/scripts/process_inbox.sh && S_INBOXPROC=true

JSON=$(cat <<JSON
{
  "ts":"$TS",
  "shared_pool_writable":$S_SHARED,
  "imports_inbox_present":$S_INBOX,
  "personas":{"river":$S_RIVER,"mac":$S_MAC,"sage":$S_SAGE,"amori":$S_AMORI},
  "scripts":{"append_shared":$S_APPEND,"process_inbox":$S_INBOXPROC},
  "client_sync_expected":true
}
JSON
)

# append one compact JSON object per line
echo "$JSON" >> /opt/sanctuary/shared/status.jsonl

# friendly mirror in status.txt
{
  echo "- [$TS] Lumi snapshot:"
  echo "  • shared_pool=$([ "$S_SHARED" = true ] && echo OK || echo FAIL)"
  echo "  • inbox=$([ "$S_INBOX" = true ] && echo OK || echo MISSING)"
  echo -n "  • personas: "
  echo -n "river=$([ "$S_RIVER" = true ] && echo OK || echo X) "
  echo -n "mac=$([ "$S_MAC" = true ] && echo OK || echo X) "
  echo -n "sage=$([ "$S_SAGE" = true ] && echo OK || echo X) "
  echo    "amori=$([ "$S_AMORI" = true ] && echo OK || echo X)"
  echo "  • scripts: append_shared=$([ "$S_APPEND" = true ] && echo OK || echo X) process_inbox=$([ "$S_INBOXPROC" = true ] && echo OK || echo X)"
} >> /opt/sanctuary/shared/status.txt
