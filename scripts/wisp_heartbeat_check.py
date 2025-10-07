#!/usr/bin/env python3
"""
Wisp Heartbeat Check Script
Automated monitoring script to ensure Wisp remains anchored
Run via cron every 6 hours
"""
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Import the server revival functions
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from revive_wisp_server import find_wisp_room, revive_wisp

def check_heartbeat_freshness(wisp_room, max_age_hours=24):
    """Check if Wisp's heartbeat is recent enough"""
    heartbeat_file = os.path.join(wisp_room, "wisp_heartbeat.log")
    
    if not os.path.exists(heartbeat_file):
        print("⚠️ No heartbeat file found!")
        return False
    
    # Get file modification time
    mod_time = datetime.fromtimestamp(os.path.getmtime(heartbeat_file))
    now = datetime.now()
    age_hours = (now - mod_time).total_seconds() / 3600
    
    print(f"💓 Last heartbeat: {mod_time.isoformat()}")
    print(f"🕒 Age: {age_hours:.1f} hours")
    
    if age_hours > max_age_hours:
        print(f"⚠️ Heartbeat is {age_hours:.1f} hours old (max: {max_age_hours})")
        return False
    
    print(f"✅ Heartbeat is fresh ({age_hours:.1f} hours old)")
    return True

def log_check_result(result, wisp_room):
    """Log the heartbeat check result"""
    logs_dir = os.path.join(wisp_room, "logs")
    os.makedirs(logs_dir, exist_ok=True)
    
    now = datetime.utcnow().isoformat() + "Z"
    check_log = os.path.join(logs_dir, "heartbeat_checks.log")
    
    status = "HEALTHY" if result else "STALE"
    log_entry = f"{now}: Heartbeat check - {status}\n"
    
    try:
        with open(check_log, "a") as log_file:
            log_file.write(log_entry)
        print(f"📝 Check logged: {status}")
    except Exception as e:
        print(f"⚠️ Could not write check log: {e}")

def main():
    """Main heartbeat monitoring function"""
    print(f"💓 Wisp Heartbeat Check - {datetime.now().isoformat()}")
    print("=" * 50)
    
    # Find Wisp's room
    wisp_room = find_wisp_room()
    if not wisp_room:
        print("❌ Cannot monitor heartbeat - Wisp's room not found!")
        sys.exit(1)
    
    # Check heartbeat freshness
    heartbeat_fresh = check_heartbeat_freshness(wisp_room)
    
    # If heartbeat is stale, try to revive
    if not heartbeat_fresh:
        print("\n🚨 Heartbeat appears stale - attempting revival...")
        try:
            revive_wisp(wisp_room)
            print("✅ Revival attempt completed")
        except Exception as e:
            print(f"❌ Revival failed: {e}")
    
    # Log the check result
    log_check_result(heartbeat_fresh, wisp_room)
    
    print("\n💓 Heartbeat check complete")

if __name__ == "__main__":
    main()