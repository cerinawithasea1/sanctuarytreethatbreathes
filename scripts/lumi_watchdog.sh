#!/usr/bin/env bash
set -euo pipefail

# ===========================
# Lumi Watchdog (cooldowned)
# ===========================

# --- Tunables ---
OK_DM_EVERY_SECS=3600         # while healthy, DM you at most once per hour
STALE_GROUP_EVERY_SECS=1800   # while stale, post to group at most once every 30 min
STALE_DM_EVERY_SECS=900       # while stale, DM you at most once every 15 min
STALE_THRESHOLD_SECS=900      # >15 min w/out heartbeat => stale

# --- Paths / env ---
LOG_DIR="/opt/sanctuary/logs"
LOG="$LOG_DIR/lumi_watchdog.log"
STATE="$LOG_DIR/lumi_state.kv"
WT="/opt/sanctuary/scripts/watch_telegram.sh"
WT_LOG="$LOG_DIR/telegram_watch.out"
ENV="/opt/sanctuary/config/telegram.env"
STATUS_TXT="/opt/sanctuary/shared/status.txt"
SEND="/opt/sanctuary/scripts/send_to_telegram.sh"

mkdir -p "$LOG_DIR"

# Load env (needs TELEGRAM_MAIN_GROUP, TELEGRAM_USER_ID; optional TELEGRAM_RIVER_GROUP)
set -a
source "$ENV"
set +a

# --- helpers ---
ts()  { date -u +'%Y-%m-%dT%H:%M:%SZ'; }
now() { date -u +%s; }
log() { echo "[$(ts)] $*" >>"$LOG"; }

kv_get(){ grep -E "^$1=" "$STATE" 2>/dev/null | cut -d= -f2- || true; }
kv_set(){
  local k="$1" v="$2"
  touch "$STATE"
  if grep -qE "^$k=" "$STATE" 2>/dev/null; then
    sed -i "s|^$k=.*|$k=$v|" "$STATE"
  else
    echo "$k=$v" >>"$STATE"
  fi
}

# notify shortcuts
dm()    { "$SEND" "${TELEGRAM_USER_ID}"      "$*"; }
grp()   { "$SEND" "${TELEGRAM_MAIN_GROUP}"   "$*"; }
both()  { dm "$*"; grp "$*"; }
river(){ [[ -n "${TELEGRAM_RIVER_GROUP:-}" ]] && "$SEND" "$TELEGRAM_RIVER_GROUP" "$*" || true; }

# --- make sure the Telegram watcher is running ---
if ! /usr/bin/pgrep -af watch_telegram.sh >/dev/null 2>&1; then
  log "watch_telegram: not running → starting"
  nohup "$WT" >"$WT_LOG" 2>&1 &
  sleep 1
  if /usr/bin/pgrep -af watch_telegram.sh >/dev/null 2>&1; then
    log "watch_telegram: ✅ started"
  else
    log "watch_telegram: ❌ failed to start"
  fi
else
  log "watch_telegram: ok"
fi

# --- determine heartbeat age ---
last_secs=0
if [[ -f "$STATUS_TXT" ]]; then
  last_line=$(tail -n 1 "$STATUS_TXT" || true)
  iso=$(echo "$last_line" | grep -Eo '[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9:]{8}Z' || true)
  if [[ -n "${iso:-}" ]]; then
    last_secs=$(date -u -d "$iso" +%s 2>/dev/null || echo 0)
  fi
fi
now_secs=$(now)
age=$(( now_secs - last_secs ))
[[ $last_secs -eq 0 ]] && age=$(( STALE_THRESHOLD_SECS + 1 ))  # treat "no file" as stale

is_stale=$([[ $age -gt $STALE_THRESHOLD_SECS ]] && echo "1" || echo "0")
prev_state=$(kv_get state)
prev_state=${prev_state:-fresh}
curr_state=$([[ $is_stale -eq 1 ]] && echo "stale" || echo "fresh")

# cooldown helpers
should_fire(){
  # $1:key  $2:interval_secs
  local key="$1" interval="$2" last next
  last=$(kv_get "$key"); last=${last:-0}
  next=$(( last + interval ))
  if [[ $now_secs -ge $next ]]; then
    kv_set "$key" "$now_secs"
    return 0
  fi
  return 1
}

# --- transitions get priority ---
if [[ "$prev_state" != "$curr_state" ]]; then
  kv_set state "$curr_state"
  if [[ "$curr_state" == "stale" ]]; then
    log "⚠️ transition: fresh → stale (age=${age}s)"
    both "⚠️ Lumi stale (age=${age}s). Snapshot poked."
  else
    log "🟢 transition: stale → fresh (age=0s)"
    both "🟢 Lumi recovered. Heartbeat fresh again."
  fi
  exit 0
fi

# --- continuous state handling with cooldowns ---
if [[ "$curr_state" == "stale" ]]; then
  log "stale: evaluating cooldowns (age=${age}s)"
  # DM to you more frequently than group
  if should_fire stale_dm_last "$STALE_DM_EVERY_SECS"; then
    dm "🟠 Lumi looks stale (age=${age}s). Snapshot poked."
  else
    log "stale: DM suppressed by cooldown"
  fi

  if should_fire stale_grp_last "$STALE_GROUP_EVERY_SECS"; then
    grp "🟠 Lumi looks stale (age=${age}s). Snapshot poked."
  else
    log "stale: group suppressed by cooldown"
  fi
else
  # fresh: quiet DM only, on hourly cadence
  log "fresh: evaluating OK cadence (age=${age}s)"
  if should_fire ok_dm_last "$OK_DM_EVERY_SECS"; then
    dm "ℹ️ Lumi OK (heartbeat fresh)."
  else
    log "fresh: DM suppressed by cooldown"
  fi
fi
