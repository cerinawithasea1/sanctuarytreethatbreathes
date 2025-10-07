#!/usr/bin/env bash
set -euo pipefail
file="$1"; shift
ts="$(date -u +'%Y-%m-%dT%H:%M:%SZ')"
mkdir -p /opt/sanctuary/shared
touch "/opt/sanctuary/shared/$file"
echo "[$ts] $*" >> "/opt/sanctuary/shared/$file"
