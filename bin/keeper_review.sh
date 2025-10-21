#!/bin/bash
# keeper_review.sh <filename>
# Runs diff, asks for approval, and promotes if confirmed

if [ -z "$1" ]; then
  echo "Usage: $0 <filename>"
  exit 1
fi

DEV="/opt/sanctuary_dev/scripts/$1"
PROD="/opt/sanctuary/scripts/$1"
DIFF="/opt/sanctuary_dev/logs/keeper_last.diff"

# run diff viewer
/opt/sanctuary_dev/bin/showdiff.sh "$PROD" "$DEV" | tee "$DIFF"

echo
# --- auto-approval control ---
# Set AUTO_APPROVE=true when you want Keeper to promote automatically
AUTO_APPROVE=${AUTO_APPROVE:-false}
if [ "$AUTO_APPROVE" = "true" ]; then
    echo "[keeper] AUTO_APPROVE is enabled — skipping prompt."
    reply="y"
else
    read -p "Approve changes to $1 ? (y/n): " reply
fi
LOG="/opt/sanctuary/shared/status.txt"
TS=$(date '+%Y-%m-%d %H:%M:%S')

case "$reply" in
  [Yy]* )
      echo "[keeper] Applying approved change to $1"
      /opt/sanctuary/scripts/promote_dev.sh
      echo "[keeper] Promotion complete."
      echo "$TS  [keeper] Approved: $1 promoted to prod" | sudo tee -a "$LOG" > /dev/null ;;
  * )
      echo "[keeper] Change rejected. Dev copy retained."
      echo "$TS  [keeper] Rejected: $1 kept in dev" | sudo tee -a "$LOG" > /dev/null ;;
esac
