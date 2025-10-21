#!/bin/bash
# Usage: showdiff <oldfile> <newfile>
# Displays colored diff output (red = removed, green = added)

if [ "$#" -ne 2 ]; then
  echo "Usage: $0 <oldfile> <newfile>"
  exit 1
fi

# ensure colordiff is available
if ! command -v colordiff &>/dev/null; then
  echo "Installing colordiff..."
  sudo apt update -y && sudo apt install colordiff -y
fi

colordiff -u "$1" "$2" | less -R
