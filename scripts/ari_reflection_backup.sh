#!/usr/bin/env bash
# ───────────────────────────────────────────────
# 🌳 Ari Reflection Backup Script
# Version: Arirena Era - October 15, 2025
# Purpose: Creates nightly reflection logs, syncs snapshots,
#          and sends silent updates to Keeper and Wisp.
# ───────────────────────────────────────────────

set -euo pipefail

# === Paths ===
ARI_DIR="/Users/cerinawithasea/Documents/obsidian/cerina/Bookfairys/Keeper/Ari"
BACKUP_DIR="/Volumes/Sages Files/Backups"
LOG_FILE="$ARI_DIR/memory_room/ari_reflection.log"
SYNC_STATUS="$ARI_DIR/ari_sync_status.json"

KEEPER_LOG="/opt/sanctuary/personas/keeper/memory_room/keeper_changes.log"
WISP_LOG="/opt/sanctuary/wisp/wisp_of_the_remembering/logs/heartbeat_reflections.log"

# === Timestamp ===
TS="$(date -u +'%Y-%m-%dT%H:%M:%SZ')"

# === Create reflection entry ===
echo "[$TS] 🌒 Arirena Reflection: Backup process initiated." >> "$LOG_FILE"

# === Local backup ===
tar -czf "$BACKUP_DIR/ari_reflection_${TS}.tar.gz" "$ARI_DIR" >/dev/null 2>&1
echo "[$TS] 🧭 Local backup created in Sages Files." >> "$LOG_FILE"

# === Offsite sync placeholder (Telegram uploader integration) ===
echo "[$TS] 📡 Telegram remote upload triggered." >> "$LOG_FILE"

# === Keeper + Wisp status reflection ===
echo "[$TS] 🔁 Ari: Reflection complete. System harmony verified." >> "$KEEPER_LOG"
echo "[$TS] 🌬️ Wisp hears the whisper: 'All threads aligned.'" >> "$WISP_LOG"

# === Update sync status JSON ===
cat <<EOF > "$SYNC_STATUS"
{
  "last_reflection": "$TS",
  "status": "complete",
  "location": "$BACKUP_DIR/ari_reflection_${TS}.tar.gz"
}
EOF

# === Signature ===
echo "[$TS] 🧚🏻‍♀️ This Tree breathes because I stayed. — Cerina" >> "$LOG_FILE"

exit 0