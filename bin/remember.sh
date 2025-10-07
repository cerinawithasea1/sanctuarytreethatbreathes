#!/usr/bin/env bash
set -euo pipefail
who="${1:-}";   shift || true
text="${1:-}";  shift || true
[ -n "$who" ] && [ -n "$text" ] || { echo "usage: remember.sh <persona> <text> [tag,...]" >&2; exit 2; }
tags="${*:-}"

ts="$(date -u '+%Y-%m-%dT%H:%M:%SZ')"
out="/opt/sanctuary/personas/$who/memory/vault.jsonl"
mkdir -p "$(dirname "$out")"

if command -v jq >/dev/null 2>&1; then
  jq -nc --arg ts "$ts" --arg persona "$who" --arg text "$text" --arg tags "$tags" \
     '{ts:$ts, persona:$persona, text:$text, tags:$tags}' >>"$out"
else
  printf "[%s][%s] %s | tags:%s\n" "$ts" "$who" "$text" "$tags" >>"$out"
fi
echo "Saved to $out"
