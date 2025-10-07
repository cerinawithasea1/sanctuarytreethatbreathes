#!/usr/bin/env bash
set -euo pipefail

INBOX="/opt/sanctuary/imports/inbox"
PROCESSED="/opt/sanctuary/imports/processed"
FAILED="/opt/sanctuary/imports/failed"
LOG="/opt/sanctuary/logs/imports.log"
APPENDER="/opt/sanctuary/scripts/append_shared.sh"
TS() { date -u +'%Y-%m-%dT%H:%M:%SZ'; }

mkdir -p "$INBOX" "$PROCESSED" "$FAILED"

# valid personas + shared
valid='^(river|mac|sage|amori|shared)$'

# helper: trim
trim(){ awk '{$1=$1;print}'; }

# read first block until blank-line for headers
read_headers() {
  awk '
    BEGIN{FS=":"; hdr=""; body=0}
    /^[[:space:]]*$/{body=1}
    body==0{print; next}
    body==1{ exit }
  ' "$1"
}

# body after first blank line (or whole file if none)
read_body() {
  awk '
    BEGIN{blank=0}
    /^[[:space:]]*$/ && blank==0{ blank=1; next }
    blank==1{ print; next }
    END{
      # If no blank line occurred, print whole file (fallback)
    }
  ' "$1"
}

shopt -s nullglob
for f in "$INBOX"/*.txt "$INBOX"/*.md; do
  [ -e "$f" ] || break

  file="$(basename "$f")"
  day="$(date -u +%Y-%m-%d)"
  outdir="$PROCESSED/$day"; mkdir -p "$outdir"

  # defaults
  to="shared"
  title=""
  tags=""

  # sniff headers (To:, Title:, Tags:)
  headers="$(read_headers "$f" || true)"
  to_raw="$(printf '%s\n' "$headers" | awk -F':' 'tolower($1)=="to"{sub(/^[^:]*:/,"");print;exit}')"
  title_raw="$(printf '%s\n' "$headers" | awk -F':' 'tolower($1)=="title"{sub(/^[^:]*:/,"");print;exit}')"
  tags_raw="$(printf '%s\n' "$headers" | awk -F':' 'tolower($1)=="tags"{sub(/^[^:]*:/,"");print;exit}')"

  [ -n "${to_raw:-}" ] && to="$(printf '%s' "$to_raw" | tr 'A-Z' 'a-z' | tr -d '[:space:]')"
  [ -n "${title_raw:-}" ] && title="$(printf '%s' "$title_raw" | trim)"
  [ -n "${tags_raw:-}" ] && tags="$(printf '%s' "$tags_raw" | trim)"

  # body
  body="$(read_body "$f")"
  if [ -z "$body" ]; then
    body="$(cat "$f")"  # fallback if no header/body split
  fi

  # validate destination
  if ! printf '%s' "$to" | grep -Eq "$valid"; then
    echo "[$(TS)] ⚠️ import: invalid 'To:' ($to) in $file" >> "$LOG"
    mv -f "$f" "$FAILED/$file"
    continue
  fi

  # Compose one-line log and append destination memories
  stamp="$(TS)"
  line_prefix="📥 Import"
  [ -n "$title" ] && line_prefix="📥 $title"

  # Where to append
  dest_mem="/opt/sanctuary/shared/memories.md"
  [ "$to" != "shared" ] && dest_mem="/opt/sanctuary/personas/$to/memories.md"

  # Append a compact line + stash the full body as an archived note
  echo "[$stamp] $line_prefix${tags:+  🏷 $tags}" >> "$dest_mem"

  # Keep the full note in processed/day/ with a normalized filename
  safe="${file// /_}"
  cp -f "$f" "$outdir/$to--$safe"

  echo "[$stamp] ✅ import -> $to : $file" >> "$LOG"
  rm -f "$f"
done
