# Warp Settings Restoration Process

**Note**: This document outlines the successful method for restoring Warp settings after multiple attempts. The key is to completely remove the existing settings before copying the backup.

## Steps for Successful Restoration

1. Backup current .warp directory (safety measure)
   ```bash
   mv ~/.warp ~/.warp.old
   ```

2. Remove current .warp directory completely
   ```bash
   rm -rf ~/.warp
   ```

3. Copy the backup folder as the new .warp directory
   ```bash
   cp -R "/Users/cerinawithasea/Documents/shAIs stuff/warp_settings_backup" ~/.warp
   ```

4. Restart Warp
   - Completely close Warp application
   - Reopen Warp

## Important Notes
- Previous attempts to simply copy over existing settings were not successful
- This complete replacement method proved to be the working solution
- Always maintain a backup of your Warp settings in case you need to restore them again

Last successful restoration: May 20, 2024

