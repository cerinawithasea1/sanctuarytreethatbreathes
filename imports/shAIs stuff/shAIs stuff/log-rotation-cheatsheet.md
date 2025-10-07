# Log Rotation Status Cheat Sheet

## 1. Checking Service Status

Check if the logrotate service is running:
```bash
launchctl list | grep logrotate
```

If running, you'll see output like:
```
-	1	com.user.logrotate
```

Start the service if not running:
```bash
launchctl load ~/Library/LaunchAgents/com.user.logrotate.plist
```

Stop the service:
```bash
launchctl unload ~/Library/LaunchAgents/com.user.logrotate.plist
```

## 2. Checking Log Sizes

Check size of log files:
```bash
# Check all auto-m4b logs including rotated ones
du -sh ~/Music/auto-m4b/auto-m4b-tool.log*

# Check all logs in OrbStack container
du -sh ~/OrbStack/docker/containers/auto-m4b/config/auto-m4b-tool.log*
```

List all large log files on your system:
```bash
find ~ -name "*.log" -size +100M -exec du -sh {} \;
```

## 3. Verifying Configuration

View logrotate configuration:
```bash
cat /opt/homebrew/etc/logrotate.d/auto-m4b
```

Test configuration without making changes:
```bash
logrotate -d /opt/homebrew/etc/logrotate.d/auto-m4b
```

View main logrotate configuration:
```bash
cat /opt/homebrew/etc/logrotate.conf
```

## 4. Checking Rotation Activity

View logrotate log:
```bash
cat ~/Library/Logs/logrotate.log
# or to see most recent entries
tail -n 20 ~/Library/Logs/logrotate.log
```

Force a log rotation (for testing):
```bash
logrotate -f /opt/homebrew/etc/logrotate.d/auto-m4b
```

Check when log files were last modified:
```bash
ls -la ~/Music/auto-m4b/auto-m4b-tool.log*
```

## 5. Common Troubleshooting Commands

Check logrotate version:
```bash
logrotate --version
```

Fix permissions if there are errors:
```bash
# For auto-m4b logs
chmod 644 ~/Music/auto-m4b/auto-m4b-tool.log*

# For OrbStack container logs (may need sudo)
sudo chmod 644 ~/OrbStack/docker/containers/auto-m4b/config/auto-m4b-tool.log*
```

Clear error log:
```bash
true > ~/Library/Logs/logrotate.log
```

Reset logrotate status file:
```bash
sudo rm /opt/homebrew/var/lib/logrotate.status
```

Check disk space:
```bash
df -h
```

Full system scan for large files:
```bash
find ~ -type f -size +100M -exec du -sh {} \; | sort -hr | head -n 20
```

## Note on System Architecture

This configuration is tailored for an M1 Mac (Apple Silicon) with:
- Homebrew installed in `/opt/homebrew` (ARM64 path)
- M1-specific file paths and permissions
- Podman/OrbStack container management

Commands and paths may differ on Intel-based Macs where Homebrew installs to `/usr/local` instead.
