#!/usr/bin/env bash
set -euo pipefail
ts="$(date -u +'%Y-%m-%dT%H:%M:%SZ')"
ARCH="/opt/sanctuary/archive/import_$(date -u +'%Y%m%dT%H%M%SZ')"
mkdir -p "$ARCH"

append_line() {
  # $1 = target file, $2 = prefix emoji+label, $3 = content file
  local target="$1" label="$2" src="$3"
  mkdir -p "$(dirname "$target")"; touch "$target"
  while IFS= read -r line || [ -n "$line" ]; do
    echo "[$ts] $label $line" >> "$target"
  done < "$src"
}

# Shared imports
for f in /opt/sanctuary/imports/shared/*.md 2>/dev/null; do
  [ -e "$f" ] || continue
  append_line "/opt/sanctuary/shared/memories.md" "📥 [Shared]" "$f"
  mkdir -p "$ARCH/shared"; mv "$f" "$ARCH/shared/"
done

# Persona imports
for p in river mac sage amori; do
  for f in /opt/sanctuary/imports/$p/*.md 2>/dev/null; do
    [ -e "$f" ] || continue
    append_line "/opt/sanctuary/personas/$p/memories.md" "📥 [${p^}]" "$f"
    mkdir -p "$ARCH/$p"; mv "$f" "$ARCH/$p/"
  done
done

echo "Imported. Archive: $ARCH"
