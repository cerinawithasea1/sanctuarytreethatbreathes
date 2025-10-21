Here is the bash script you requested:
```
#!/bin/bash

# Print current date
echo "Current Date: $(date)"

# Get disk usage information for all mounted file systems
for filesystem in /sys/fs/cgroup/system.slice/*; do
  mountpoint=$(dirname "$filesystem")
  if [ -n "$mountpoint" ]; then
    du -sh --max-depth=1 "$mountpoint" | sort -h
  fi
done
```
Let me explain what this script does:

1. The first line, `echo "Current Date: $(date)"`, prints the current date and time using the `date` command.
2. The second part of the script uses a loop to iterate over all mounted file systems (e.g., `/dev/sda1`, `/mnt/usb`, etc.). It does this by looking in the `/sys/fs/cgroup/system.slice/` directory, which contains directories representing each mounted file system.
3. For each mounted file system, it gets the mount point using `dirname "$filesystem"`.
4. If the mount point is not empty (i.e., if it's a valid directory), it runs the `du` command to get the disk usage information for that directory. The options used are:
	* `-sh`: Print human-readable sizes (e.g., 1K, 2M, etc.).
	* `--max-depth=1`: Only consider the top-level directory and its immediate contents.
5. Finally, it sorts the output by size using the `sort` command with the `-h` option.

To use this script, save it to a file named `/opt/sanctuary_dev/scripts/printcurrentdateandd.sh`, make it executable with `chmod +x /opt/sanctuary_dev/scripts/printcurrentdateandd.sh`, and then run it with `./printcurrentdateandd.sh`.

