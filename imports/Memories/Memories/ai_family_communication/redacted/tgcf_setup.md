# TGCF (Telegram Chat Forwarder) Setup

## Configuration
- **Location**: `/Users/cerinawithasea/services/tgcf/`
- **Web Interface**: `[REDACTED_URL] (via OrbStack)
- **Container**: Docker container named `tgcf` running on OrbStack
- **Persistence**: Fixed session persistence issue by mounting:
  - `./data/sessions:/root/.local/share/pyrogram` (Telegram session files)
  - `./data/config:/app/.tgcf` (TGCF config and state)
  - `./data:/app/data` (runtime data)

## Key Files
- `docker-compose.yml`: Main container configuration
- `tgcf.config.yml`: Static config file with API credentials
- `data/`: Persistent data directory for sessions and runtime config

## Issue Resolution
- **Problem**: Configuration reset after reboot due to missing volume mounts for session files
- **Solution**: Added proper volume mounts for Telegram session persistence
- **Result**: Configuration now persists across reboots and container restarts