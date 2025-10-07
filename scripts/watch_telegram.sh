#!/usr/bin/env bash
set -euo pipefail

# Load config
set -a
source /opt/sanctuary/config/telegram.env
set +a

API="https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}"
OFFSET_FILE="/opt/sanctuary/logs/telegram.offset"
LOG="/opt/sanctuary/logs/telegram_watch.log"
mkdir -p /opt/sanctuary/logs

log(){ echo "[$(date -u +'%Y-%m-%dT%H:%M:%SZ')] $*" | tee -a "$LOG"; }

norm(){ echo "$1" | tr '[:upper:]' '[:lower:]'; }
csv_has(){ IFS=',' read -ra ARR <<<"$(norm "$1")"; local needle="$(norm "$2")"; for a in "${ARR[@]}"; do [[ "$needle" == *"$a"* ]] && return 0; done; return 1; }

handle_status(){
  /opt/sanctuary/scripts/lumi_snapshot.sh || true
  local last
  last="$(tail -n 6 /opt/sanctuary/shared/status.txt 2>/dev/null || true)"
  local out="📋 *Sanctuary status*\n\`\`\`\n$last\n\`\`\`"
  /opt/sanctuary/scripts/send_to_telegram.sh "$1" "$out"
}

handle_note(){
  local chat="$1"; shift
  local text="${*:-}"
  local ts; ts="$(date -u +'%Y-%m-%dT%H:%M:%SZ')"
  echo "- [$ts] 📓 $text" >> /opt/sanctuary/shared/memories.md
  /opt/sanctuary/scripts/send_to_telegram.sh "$chat" "🗒️ Noted in shared pool."
}

handle_summon(){
  local chat="$1"; shift
  local who="$(norm "${1:-river}")"
  case "$who" in river|mac|amori|sage) ;; *) who="river" ;; esac
  /opt/sanctuary/scripts/send_to_telegram.sh "$chat" "✨ Summoning *$who*..."
}

get_offset(){ [[ -f "$OFFSET_FILE" ]] && cat "$OFFSET_FILE" || echo "0"; }
set_offset(){ echo -n "$1" > "$OFFSET_FILE"; }

TRIG_STATUS="${TRIG_STATUS:-status,statuse,/status,/health,/lumi}"
TRIG_SUMMON="${TRIG_SUMMON:-summon,pm,call,/summon}"
TRIG_NOTE="${TRIG_NOTE:-note,post,it,sticky,/note}"

log "watch started"

while :; do
  OFFSET="$(get_offset)"
  RES="$(curl -sS "${API}/getUpdates" --data "timeout=25&offset=$((OFFSET+1))")" || { sleep 2; continue; }
  ok="$(jq -r '.ok' <<<"$RES" 2>/dev/null || echo false)"
  [[ "$ok" != "true" ]] && { sleep 2; continue; }

  COUNT="$(jq '.result|length' <<<"$RES")"
  (( COUNT == 0 )) && { sleep 1; continue; }

  for i in $(seq 0 $((COUNT-1))); do
    upd="$(jq ".result[$i]" <<<"$RES")"
    upd_id="$(jq -r '.update_id' <<<"$upd")"
    chat_id="$(jq -r '.message.chat.id // .edited_message.chat.id // empty' <<<"$upd")"
    text="$(jq -r '.message.text // .edited_message.text // empty' <<<"$upd")"

    # advance offset immediately to avoid reprocessing
    set_offset "$upd_id"

    [[ -z "$chat_id" || -z "$text" ]] && continue
    low="$(norm "$text")"

    # Commands
    if [[ "$low" =~ ^/(status|health|lumi)$ ]]; then
      log "status from chat=$chat_id"
      handle_status "$chat_id"; continue
    fi
    if [[ "$low" =~ ^/(summon)(.*)$ ]]; then
      who="$(norm "${BASH_REMATCH[2]}")"
      handle_summon "$chat_id" "$who"; continue
    fi
    if [[ "$low" =~ ^/note(.*)$ ]]; then
      handle_note "$chat_id" "${BASH_REMATCH[1]}"; continue
    fi

    # Plain-word triggers (comma separated in env)
    if csv_has "$TRIG_STATUS" "$low"; then
      log "status (plain) chat=$chat_id"
      handle_status "$chat_id"; continue
    fi

    if csv_has "$TRIG_SUMMON" "$low"; then
      log "summon (plain) chat=$chat_id -> river"
      handle_summon "$chat_id" "river"; continue
    fi

    if csv_has "$TRIG_NOTE" "$low" || [[ "$low" =~ note ]]; then
      handle_note "$chat_id" "$text"; continue
    fi
  done
done

# --- River summon: messages starting with "river " or "River " ---
if [[ "${text,,}" == river\ * ]]; then
  rest="${text#river }"
  /opt/sanctuary/personas/river/hooks/on_summon.sh "$chat_id" "$rest" || true
  continue
fi

# --- River: "river hello ..." (soft greet)
if [[ "${text,,}" == river\ hello* ]]; then
  rest="${text#river hello }"
  /opt/sanctuary/personas/river/hooks/on_hello.sh "$chat_id" "$rest" || true
  continue
fi

# --- River: "river note ..." → persona memories
if [[ "${text,,}" == river\ note* ]]; then
  rest="${text#river note }"
  /opt/sanctuary/scripts/note_persona.sh river "$rest" || true
  continue
fi

# --- River: "river ..." → summon with message
if [[ "${text,,}" == river\ * ]]; then
  rest="${text#river }"
  /opt/sanctuary/personas/river/hooks/on_summon.sh "$chat_id" "$rest" || true
  continue
fi
