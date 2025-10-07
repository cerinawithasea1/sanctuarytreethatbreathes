#!/usr/bin/env python3
import time
from datetime import datetime

LOG = "/Volumes/Sages Files/AI_Sanctuary/keeper_daemon/heartbeat.log"

def heartbeat():
    with open(LOG, "a") as f:
        f.write(f"Keeper heartbeat: {datetime.utcnow().isoformat()}Z\n")

if __name__ == "__main__":
    print("🌟 Keeper Daemon starting...")
    while True:
        heartbeat()
        print("✅ Keeper heartbeat written.")
        time.sleep(3600)  # once per hour