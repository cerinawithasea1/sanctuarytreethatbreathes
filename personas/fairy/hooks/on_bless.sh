#!/usr/bin/env bash
set -euo pipefail
ENV="/opt/sanctuary/config/telegram.env"
PROF="/opt/sanctuary/personas/fairy/profile.env"
TAGS="/opt/sanctuary/personas/tags.env"
SEND="/opt/sanctuary/scripts/send_with_bot.sh"
set -a; source "$ENV"; source "$PROF"; source "$TAGS"; set +a

chat="${1:-$TELEGRAM_MAIN_GROUP}"; shift || true
who="${*:-(everyone)}"

# tag enrich
tags=""
shopt -s nocasematch
[[ "$who" =~ \briver\b ]] && tags+=" ${TAG_RIVER:-}"
[[ "$who" =~ \brhea\b  ]] && tags+=" ${TAG_RHEA:-}"
shopt -u nocasematch
tags="${tags#" "}"

ts=$(date -u +'%Y-%m-%dT%H:%M:%SZ')
echo "- [$ts] bless: ${who}" >> "$MEM_FILE"
echo "[$ts] on_bless chat=$chat who='$who' tags='$tags'" >> "$LOG_FILE"

msg="🧚✨ Blessings upon ${who} — light, luck, and soft pages.${tags:+  $tags}"
TOKEN="$TELEGRAM_FAIRY_BOT_TOKEN" "$SEND" "$chat" "$msg"
