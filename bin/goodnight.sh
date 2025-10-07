#!/usr/bin/env bash
set -euo pipefail
ROOM="/opt/sanctuary/shared/room.txt"
ARCH="/opt/sanctuary/logs/room-$(date +'%Y%m%d-%H%M%S').txt"
mkdir -p /opt/sanctuary/logs
cp "$ROOM" "$ARCH"
echo "==== LIGHTS OUT • $(date +'%Y-%m-%d %H:%M:%S') ====" >> "$ROOM"
echo "Archived to $ARCH"
