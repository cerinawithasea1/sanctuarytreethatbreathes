# Warp MCP Setup Process

## Setup Steps Completed
1. **Serena MCP**: Already configured and running in Warp MCP settings
2. **Telegram MCP**: Added via setup script `./warp/setup-mcp.sh`

## Configuration Location
- Template: `/Users/cerinawithasea/config/warp/mcp.json.template`
- Deployed to: `~/Library/Application Support/Warp/settings/mcp.json`

## Important Notes
- **Restart Required**: After running the setup script, Warp terminal must be quit and restarted for MCP configuration changes to take effect
- Both Serena and Telegram MCP servers will be available after restart
- Serena has `start_on_launch: true`, Telegram has `start_on_launch: false`

## Manual QA Checklist Status
- ✅ Setup script executed successfully
- ⏳ Pending: Warp restart and verification of both servers
- ⏳ Pending: Test MCP commands for both servers

## Next Steps After Restart
1. Verify both servers show "Server ready" in logs
2. Test Telegram MCP tools (`get_chats`, `send_message`)
3. Verify Serena tools still function
4. Test auto-start functionality