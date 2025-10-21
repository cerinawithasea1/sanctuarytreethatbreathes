#!/bin/bash
# Launch Keeper dev environment
cd /opt/sanctuary_dev/mcp/telegram-mcp
source .venv/bin/activate
python main.py 2>&1 | tee /opt/sanctuary_dev/mcp/telegram-mcp/keeper_dev.log
deactivate

