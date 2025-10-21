#!/bin/bash
# promote_dev.sh - copies dev changes into production after approval

if [ ! -f /opt/sanctuary_dev/APPROVED ]; then
    echo "[keeper] Promotion not approved or marker missing."
    exit 1
fi

SCRIPT_NAME="$1"
rsync -av "/opt/sanctuary_dev/scripts/$SCRIPT_NAME" "/opt/sanctuary/scripts/"

echo "[keeper] Promotion finished successfully."
