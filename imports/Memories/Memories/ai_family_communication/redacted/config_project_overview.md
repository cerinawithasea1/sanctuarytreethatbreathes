# Config Project Purpose & Structure

## Project Purpose
This is Cerina's personal configuration management system located at `/Users/cerinawithasea/config`. It serves as a centralized location for:
- Warp terminal MCP (Model Context Protocol) integration with Serena
- System configuration files and templates
- Database and migration management
- Backup and logging systems

## Directory Structure
- **warp/**: Warp MCP configuration files and setup scripts
  - `README.md`: Setup and usage instructions
  - `mcp.json.template`: Template for Warp MCP settings
  - `setup-mcp.sh`: Deployment script for MCP configuration
- **migrations/**: Database migration files
- **cache/**: Cached data and temporary files
- **streams/**: Stream configuration or data
- **logs/**: Log files from various systems
- **backups/**: System and configuration backups
- **.serena/**: Serena project configuration (auto-generated)
- **absdatabase.sqlite**: SQLite database file

## Key Features
- **MCP Integration**: Seamless Serena integration with Warp terminal
- **Template System**: Environment variable substitution for secure config management
- **Version Control Ready**: Designed to be git-managed without exposing secrets
- **Cross-Machine Deployment**: Portable setup across different machines