# Suggested Commands for Config Project

## MCP/Warp Setup Commands
```bash
# Deploy MCP configuration to Warp
~/config/warp/setup-mcp.sh

# Check MCP configuration
cat "~/Library/Application Support/Warp/settings/mcp.json"

# Verify environment variables
echo $SERENA_API_KEY
```

## Development Commands
```bash
# Navigate to config directory
cd ~/config

# List project structure
ls -la
tree (if available)

# Check database
sqlite3 absdatabase.sqlite ".tables"
```

## Version Control Commands
```bash
# Initialize git repo (if not already done)
git init
git add warp/
git commit -m "Add Warp MCP configuration"

# Check status
git status
git log --oneline
```

## System Utilities (macOS/Darwin)
```bash
# File operations
ls -la          # List files with permissions
find . -name    # Find files by name
grep -r         # Recursive text search

# Process management
ps aux | grep   # Find processes
killall         # Kill processes by name

# System info
system_profiler SPHardwareDataType  # Hardware info
uname -a        # System information
```

## Backup & Maintenance
```bash
# Create backups
cp -r warp/ backups/warp-$(date +%Y%m%d)/

# Check logs
tail -f logs/*.log

# Clean cache
rm -rf cache/*
```