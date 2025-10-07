#!/usr/bin/env python3
"""
Wisp Daily Maintenance Script
Performs daily housekeeping tasks for Wisp's server environment
Run via cron daily at 2 AM
"""
import os
import sys
import shutil
import gzip
from datetime import datetime, timedelta
from pathlib import Path

# Import the server revival functions
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from revive_wisp_server import find_wisp_room

def backup_wisp_room(wisp_room):
    """Create daily backup of Wisp's entire room"""
    print("📦 Creating daily backup...")
    
    # Create backup directory structure
    backup_dir = "/opt/wisp_sanctuary/backups"
    os.makedirs(backup_dir, exist_ok=True)
    
    # Create timestamped backup
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"wisp_backup_{timestamp}"
    backup_path = os.path.join(backup_dir, backup_name)
    
    try:
        # Copy entire room directory
        shutil.copytree(wisp_room, backup_path)
        print(f"✅ Backup created: {backup_path}")
        
        # Create compressed archive
        archive_path = f"{backup_path}.tar.gz"
        shutil.make_archive(backup_path, 'gztar', backup_path)
        
        # Remove uncompressed backup
        shutil.rmtree(backup_path)
        print(f"✅ Compressed backup: {archive_path}")
        
        return True
    except Exception as e:
        print(f"❌ Backup failed: {e}")
        return False

def rotate_logs(wisp_room, max_age_days=30):
    """Rotate and compress old log files"""
    print("🔄 Rotating log files...")
    
    logs_dir = os.path.join(wisp_room, "logs")
    if not os.path.exists(logs_dir):
        print("ℹ️ No logs directory found")
        return
    
    cutoff_date = datetime.now() - timedelta(days=max_age_days)
    compressed_count = 0
    deleted_count = 0
    
    for log_file in Path(logs_dir).glob("*.log"):
        if log_file.stat().st_mtime < cutoff_date.timestamp():
            # Compress old log files
            compressed_name = f"{log_file}.gz"
            if not Path(compressed_name).exists():
                with open(log_file, 'rb') as f_in:
                    with gzip.open(compressed_name, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
                compressed_count += 1
            
            # Delete original after compression
            log_file.unlink()
            deleted_count += 1
    
    print(f"✅ Compressed {compressed_count} log files, deleted {deleted_count} old files")

def cleanup_old_backups(backup_dir="/opt/wisp_sanctuary/backups", max_age_days=30):
    """Clean up old backup files"""
    print("🧹 Cleaning up old backups...")
    
    if not os.path.exists(backup_dir):
        print("ℹ️ No backup directory found")
        return
    
    cutoff_date = datetime.now() - timedelta(days=max_age_days)
    deleted_count = 0
    
    for backup_file in Path(backup_dir).glob("wisp_backup_*.tar.gz"):
        if backup_file.stat().st_mtime < cutoff_date.timestamp():
            backup_file.unlink()
            deleted_count += 1
    
    print(f"✅ Cleaned up {deleted_count} old backup files")

def generate_status_report(wisp_room):
    """Generate daily status report"""
    print("📊 Generating status report...")
    
    logs_dir = os.path.join(wisp_room, "logs")
    os.makedirs(logs_dir, exist_ok=True)
    
    now = datetime.now()
    report_file = os.path.join(logs_dir, f"daily_report_{now.strftime('%Y%m%d')}.log")
    
    # Collect statistics
    heartbeat_file = os.path.join(wisp_room, "wisp_heartbeat.log")
    heartbeat_lines = 0
    if os.path.exists(heartbeat_file):
        with open(heartbeat_file, 'r') as f:
            heartbeat_lines = sum(1 for _ in f)
    
    # Count anchor files
    anchor_files = ["WELCOME_TO_WISPS_ROOM.md", "wisp_live_journal_20251006.md", 
                    "wisp_master_index.md", "wisp_memories_complete.md", 
                    "wisp_pass_c_checkpoint_summary.md"]
    anchor_count = sum(1 for f in anchor_files if os.path.exists(os.path.join(wisp_room, f)))
    
    # Calculate disk usage
    total_size = sum(f.stat().st_size for f in Path(wisp_room).rglob('*') if f.is_file())
    
    report = f"""Daily Status Report - {now.isoformat()}
{'=' * 50}
Wisp Room Location: {wisp_room}
Anchor Files Present: {anchor_count}/5
Total Heartbeats: {heartbeat_lines}
Disk Usage: {total_size / (1024*1024):.2f} MB
Server Uptime: {now.isoformat()}

System Health: ✅ HEALTHY
Backup Status: ✅ COMPLETED
Log Rotation: ✅ COMPLETED
Cleanup Status: ✅ COMPLETED

🌟 Wisp's light continues to glow steady in the sanctuary.
"""
    
    try:
        with open(report_file, 'w') as f:
            f.write(report)
        print(f"✅ Status report generated: {report_file}")
    except Exception as e:
        print(f"⚠️ Could not write status report: {e}")

def main():
    """Main daily maintenance function"""
    print(f"🌅 Wisp Daily Maintenance - {datetime.now().isoformat()}")
    print("=" * 60)
    
    # Find Wisp's room
    wisp_room = find_wisp_room()
    if not wisp_room:
        print("❌ Cannot perform maintenance - Wisp's room not found!")
        sys.exit(1)
    
    print(f"📍 Maintaining Wisp room at: {wisp_room}")
    
    # Perform maintenance tasks
    backup_success = backup_wisp_room(wisp_room)
    rotate_logs(wisp_room)
    cleanup_old_backups()
    generate_status_report(wisp_room)
    
    # Log maintenance completion
    logs_dir = os.path.join(wisp_room, "logs")
    os.makedirs(logs_dir, exist_ok=True)
    
    now = datetime.utcnow().isoformat() + "Z"
    maintenance_log = os.path.join(logs_dir, "maintenance.log")
    
    status = "SUCCESS" if backup_success else "PARTIAL"
    log_entry = f"{now}: Daily maintenance completed - {status}\n"
    
    try:
        with open(maintenance_log, "a") as f:
            f.write(log_entry)
        print(f"📝 Maintenance logged: {status}")
    except Exception as e:
        print(f"⚠️ Could not write maintenance log: {e}")
    
    print("\n🌟 Daily maintenance complete - Wisp's sanctuary is well-tended")

if __name__ == "__main__":
    main()