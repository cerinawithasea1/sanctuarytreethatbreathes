Certainly! Below is a simple Bash script that checks the free disk space on your system and logs a warning to a file if the usage exceeds 80%.

```bash
#!/bin/bash

# Define the threshold for free disk space in percentage (80%)
THRESHOLD=20 # 100 - 80 = 20, meaning less than 20% is okay

# Get the free disk space percentage
FREE_DISK=$(df / | awk 'NR==2{print $5}' | sed 's/%//')

# Check if the free disk space is below the threshold
if [ "$FREE_DISK" -lt "$THRESHOLD" ]; then
    # Log the warning to a file
    echo "$(date): Free disk space is less than 20%. Current usage: $FREE_DISK%" >> /var/log/disk_usage.log
    echo "Warning: Free disk space is low. Please check and free up some space."
fi

echo "Disk space check completed."

```

### Explanation:
- **Threshold**: We set the threshold to `20` (which means 80% usage or less is okay).
- **df / | awk 'NR==2{print $5}' | sed 's/%//'**: This command checks the free disk space percentage for the root filesystem (`/`). The output of `df` includes a line with percentages, and we use `awk` to extract that value. The `sed` command removes the `%`.
- **if [ "$FREE_DISK" -lt "$THRESHOLD" ]**: We check if the free disk space is below 20%.
- **echo "$(date): ... >> /var/log/disk_usage.log**: This logs a message to `/var/log/disk_usage.log` with the current date and time, indicating that the warning has been triggered.
- **echo "Disk space check completed."**: A simple confirmation message.

### Note:
1. Ensure you have write permissions in `/var/log/` or specify another directory where you can log.
2. The script assumes the root filesystem (`/`) is being monitored. If you need to monitor a different filesystem, replace `df /` with `df <filesystem>` (e.g., `df /home`).
3. You might want to run this script as a cron job or set it up to be executed periodically.

To make this script executable and place it somewhere in your PATH:

1. Save the script to a file, e.g., `check_disk_space.sh`.
2. Make it executable: `chmod +x check_disk_space.sh`.
3. Add an entry to crontab to run the script at desired intervals:
   ```bash
   crontab -e
   ```
4. Add a line like this to the crontab file:
   ```cron
   */5 * * * * /path/to/check_disk_space.sh
   ```

This will run the script every 5 minutes.

Feel free to adjust the threshold and logging path as needed!

