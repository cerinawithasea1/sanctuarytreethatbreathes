#!/usr/bin/env bash
set -euo pipefail
source /opt/sanctuary/config/ingest.env

LOG="/opt/sanctuary/logs/ingest.log"
NORM="/opt/sanctuary/scripts/normalize_note.sh"
mkdir -p "$(dirname "$LOG")"

ts() { date -u +'%Y-%m-%dT%H:%M:%SZ'; }
log(){ echo "[$(ts)] $*" | tee -a "$LOG" ; }

shopt -s nullglob
entries=()
for ext in $INGEST_EXTS; do
  for f in "$INCOMING_DIR"/*."$ext"; do entries+=("$f"); done
done

(( ${#entries[@]} == 0 )) && { log "No incoming files."; exit 0; }

# Ensure persona directories exist
for p in $P_PERSONAS; do
  mkdir -p "$BASE_DIR/$p"
  touch    "$BASE_DIR/$p/memories.md"
done
touch "$SHARED_MEM"

date_tag="$(date +%Y%m%d)"
ARCH="/opt/sanctuary/archive/$date_tag"
mkdir -p "$ARCH"

route_file(){
  local f="$1"
  local base="$(basename "$f")"
  local lower="${base,,}"

  # default routing
  local target="$SHARED_MEM"
  local persona=""

  # persona by filename prefix: river__foo.md
  if [[ "$lower" =~ ^(river|mac|sage|amori)__(.+)$ ]]; then
    persona="${BASH_REMATCH[1]}"
    target="$BASE_DIR/$persona/memories.md"
  fi

  # parse inline header for persona / tags if present
  # first 20 lines only to avoid huge scans
  local header
  header="$(head -n 20 "$f" || true)"

  # persona header wins (e.g. [persona:River])
  if [[ "$header" =~ \[persona:([A-Za-z]+)\] ]]; then
    local hpers="${BASH_REMATCH[1],,}"
    if [[ " $P_PERSONAS " == *" $hpers "* ]]; then
      persona="$hpers"
      target="$BASE_DIR/$persona/memories.md"
    fi
  fi

  # flags
  local speculative="$DEFAULT_SPECULATIVE"
  [[ "$header" =~ \[speculative:(true|false)\] ]] && speculative="${BASH_REMATCH[1]}"
  local source_tag="$DEFAULT_SOURCE"
  [[ "$header" =~ \[source:([A-Za-z0-9_-]+)\] ]] && source_tag="${BASH_REMATCH[1]}"

  log "Ingesting '$base' → ${persona:-shared} (speculative=$speculative source=$source_tag)"
  {
    echo ""
    echo "---"
    echo "### Ingest: $base  ($(date -u +'%Y-%m-%d %H:%MZ'))"
    echo "_source: $source_tag  speculative: $speculative_"
    echo ""
    # strip header bracket lines when copying body
    # (anything like [persona:*] or [speculative:*] or [source:*] in first 20 lines)
    awk 'NR>20 || $0 !~ /^\[ *(persona|speculative|source):/ {print}' "$f" \
      | "$NORM"
  } >> "$target"

  # archive the original file
  mv -f "$f" "$ARCH/"
}

for f in "${entries[@]}"; do
  route_file "$f"
done

log "Done. Archived originals to $ARCH"
