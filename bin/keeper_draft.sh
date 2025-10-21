#!/bin/bash
# keeper_draft.sh — Generate and review a new script in the dev sandbox
# Usage: sudo /opt/sanctuary_dev/bin/keeper_draft.sh "describe the script you want"

if [ -z "$1" ]; then
  echo "Usage: $0 \"describe the script you want\""
  exit 1
fi

DESC="$1"
# create a simple filename from the first few words of the description
NAME=$(echo "$DESC" | tr '[:upper:]' '[:lower:]' | tr -cd 'a-z0-9_' | cut -c1-20)
TARGET="/opt/sanctuary_dev/scripts/${NAME}.sh"

echo "[keeper] Drafting $TARGET"
echo "Description: $DESC"
echo

# use your chosen Ollama model (qwen2.5:4.7-instruct or dolphin-llama3)
MODEL="qwen2.5:7b-instruct"

# generate the draft with the local model
ollama run "$MODEL" "Write a bash script that will: $DESC" > "$TARGET"

sudo chmod +x "$TARGET"

# trigger Keeper’s normal review and approval loop
/opt/sanctuary_dev/bin/keeper_review.sh "$(basename "$TARGET")"
