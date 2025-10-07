#!/usr/bin/env bash
set -euo pipefail
who="${1:-}"; shift || true
msg="${*:-}"
[ -n "$who" ] || { echo "usage: say.sh <persona> <text...>" >&2; exit 2; }
ts="$(date -u '+%Y-%m-%dT%H:%M:%SZ')"
echo "[$ts][$who] $msg"
