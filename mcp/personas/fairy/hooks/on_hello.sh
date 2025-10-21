#!/usr/bin/env bash
set -euo pipefail
ENV="/opt/sanctuary/config/telegram.env"
PROF="/opt/sanctuary/personas/fairy/profile.env"
TAGS="/opt/sanctuary/personas/tags.env"
SEND="/opt/sanctuary/scripts/send_with_bot.sh"
set -a; source "$ENV"; source "$PROF"; source "$TAGS"; set +a

chat="${1:-$TELEGRAM_MAIN_GROUP}"; shift || true
msg="${*:-(no details)}"

# tag enrich
tags=""
shopt -s nocasematch
[[ "$msg" =~ \briver\b ]] && tags+=" ${TAG_RIVER:-}"
[[ "$msg" =~ \brhea\b  ]] && tags+=" ${TAG_RHEA:-}"
shopt -u nocasematch
tags="${tags#" "}"

ts=$(date -u +'%Y-%m-%dT%H:%M:%SZ')
echo "- [$ts] hello: ${msg}" >> "$MEM_FILE"
echo "[$ts] on_hello chat=$chat msg='$msg' tags='$tags'" >> "$LOG_FILE"

TOKEN="$TELEGRAM_FAIRY_BOT_TOKEN" "$SEND" "$chat" "🧚‍♀️ Fairy flutters in and hears: \"${msg}\"${tags:+ — $tags}"
