# Task Completion Workflow

## After Configuration Changes
1. **Test the configuration**:
   - Verify template processing works
   - Check that environment variables are properly substituted
   - Test on a fresh terminal session

2. **Validation Steps**:
   ```bash
   # For MCP changes
   ~/config/warp/setup-mcp.sh
   # Restart Warp and test MCP connectivity
   
   # For other configs
   # Test the specific service/tool affected
   ```

3. **Documentation Updates**:
   - Update README.md if setup process changes
   - Document any new environment variables needed
   - Add troubleshooting steps for common issues

4. **Version Control**:
   ```bash
   cd ~/config
   git add .
   git commit -m "Descriptive commit message"
   ```

5. **Backup Important Changes**:
   ```bash
   # Create timestamped backup
   cp -r warp/ backups/warp-$(date +%Y%m%d-%H%M)/
   ```

## Quality Checklist
- [ ] Configuration templates process correctly
- [ ] No hardcoded secrets in files
- [ ] Documentation is updated
- [ ] Cross-machine portability maintained
- [ ] Backup created for significant changes
- [ ] Changes tested in fresh environment