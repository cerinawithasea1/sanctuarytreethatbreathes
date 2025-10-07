#!/usr/bin/env bash
set -euo pipefail

# stdin -> stdout; turns free text into "- [ISO] text" lines
ts() { date -u +'%Y-%m-%dT%H:%M:%SZ'; }

while IFS= read -r line || [ -n "${line:-}" ]; do
  # skip empties
  [[ -z "${line// }" ]] && continue
  # already looks like a dated line? keep it
  if [[ "$line" =~ ^-?\ \[[0-9]{4}-[0-9]{2}-[0-9]{2}T ]]; then
    echo "$line"
  else
    echo "- [$(ts)] $line"
  fi
done
