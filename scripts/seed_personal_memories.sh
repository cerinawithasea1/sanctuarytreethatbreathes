#!/usr/bin/env bash
set -euo pipefail
ts="$(date -u +'%Y-%m-%dT%H:%M:%SZ')"
for p in river mac sage amori; do
  mkdir -p "/opt/sanctuary/personas/$p"
  echo "[$ts] 🌱 Memory Dropbox connected. Reflections welcome here." >> "/opt/sanctuary/personas/$p/memories.md"
done
