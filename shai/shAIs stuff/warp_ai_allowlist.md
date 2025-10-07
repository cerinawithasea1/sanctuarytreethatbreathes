# Warp AI Command Allow List Configuration

This document provides a detailed allow list configuration for Warp AI, organized by priority and function with safety justifications.

## How to Implement

In Warp, you can add these commands to your AI allow list through the settings:

1. Open Warp
2. Go to Settings (⌘+, on macOS, Ctrl+, on Windows)
3. Navigate to AI Assistant section
4. Add these commands to the "AI Allow List"

## Cross-Platform Notes

This allow list includes both Unix/macOS commands and their Windows equivalents. Commands marked with:
- **[Unix/macOS]** are specific to Unix-based systems (macOS, Linux)
- **[Windows]** are specific to Windows Command Prompt or PowerShell
- Commands without specific marking work on both platforms

## Priority 1: Essential File System Navigation (Most Used)

### Directory Listing
- **Command Pattern [Unix/macOS]:** `ls [options] [file|directory]`
- **Command Pattern [Windows]:** `dir [options] [directory]`
- **PowerShell Equivalent:** `Get-ChildItem` or `ls` (PowerShell alias)
- **Safety Justification:** Read-only operation that only displays file listings, no modification risk
- **Common Use Cases:** Listing directory contents, checking file existence, viewing file permissions
- **Allowed Options [Unix/macOS]:** 
  - `-l` (long format)
  - `-a` (show hidden files)
  - `-h` (human-readable sizes)
  - `-R` (recursive listing)
- **Allowed Options [Windows]:** 
  - `/w` (wide format)
  - `/a` (attributes)
  - `/s` (recursive)

### Current Directory
- **Command Pattern [Unix/macOS]:** `pwd`
- **Command Pattern [Windows]:** `cd` (without arguments) or `echo %cd%`
- **PowerShell Equivalent:** `Get-Location` or `pwd` (PowerShell alias)
- **Safety Justification:** Purely informational, displays current directory with no modification capabilities
- **Common Use Cases:** Confirming current location, getting absolute path for reference
- **Allowed Options:** None needed

### File Search
- **Command Pattern [Unix/macOS]:** `find [path] [expression]`
- **Command Pattern [Windows]:** `where [options] [pattern]` or `dir /s /b [pattern]`
- **PowerShell Equivalent:** `Get-ChildItem -Recurse -Filter "*pattern*"` or `ls -r *pattern*`
- **Safety Justification:** Read-only search operation when used without actions
- **Common Use Cases:** Locating files, searching by name/type/date
- **Allowed Options [Unix/macOS]:**
  - `-name`, `-type`, `-size` (search parameters)
  - `-mtime`, `-ctime` (time filters)
- **Allowed Options [Windows]:**
  - `/r` (recursive)
  - wildcard patterns like `*.txt`

### File Contents Viewing
- **Command Pattern [Unix/macOS]:** `cat [file]`
- **Command Pattern [Windows]:** `type [file]`
- **PowerShell Equivalent:** `Get-Content [file]` or `cat [file]` (PowerShell alias)
- **Safety Justification:** Read-only file viewing, no modification risk
- **Common Use Cases:** Display file contents, check script contents before execution
- **Allowed Options [Unix/macOS]:** 
  - `-n` (number lines)
- **Allowed Options [Windows]:** None common

### Partial File Viewing
- **Command Pattern [Unix/macOS]:** `head [options] [file]` and `tail [options] [file]`
- **PowerShell Equivalent:** `Get-Content [file] -Head [number]` or `Get-Content [file] -Tail [number]`
- **Safety Justification:** Read-only operations that display partial file contents
- **Common Use Cases:** Checking log beginnings/endings, viewing file headers
- **Allowed Options [Unix/macOS]:**
  - `-n [NUMBER]` (lines to display)
- **Windows Alternative:** 
  - `findstr /n "^" [file] | findstr /b "[1-10]:"` (first 10 lines, similar to head)

## Priority 2: Development Tools

### Git Read Operations
- **Command Pattern:** `git status`, `git log`, `git branch`, `git diff`, `git remote -v`
- **Safety Justification:** Read-only operations that report repository status without modification
- **Common Use Cases:** Checking uncommitted changes, reviewing commit history, examining branches
- **Allowed Options:**
  - `git log --oneline` (compact view)
  - `git diff --name-only` (just show filenames)

### Version Checks
- **Command Pattern:** `[command] --version` or `[command] -v`
- **Safety Justification:** Purely informational, no system modification
- **Common Use Cases:** Confirming installed tools, checking compatibility
- **Examples:** 
  - `python --version`
  - `node --version`
  - `npm --version`
  - `ffmpeg -version`

### Package Information
- **Command Pattern:** `pip list`, `npm list`
- **Safety Justification:** Read-only lists of installed packages
- **Common Use Cases:** Checking dependencies, verifying installations
- **Allowed Options:**
  - `pip list --outdated` (check for updates)

## Priority 3: System Information

### Command Location
- **Command Pattern [Unix/macOS]:** `which [command]`, `whereis [command]`, `type [command]`
- **Command Pattern [Windows]:** `where [command]`
- **PowerShell Equivalent:** `Get-Command [command]` or `gcm [command]`
- **Safety Justification:** Read-only operations that locate executables
- **Common Use Cases:** Determining if tools are installed, finding executable paths
- **Examples:**
  - `which python` / `where python.exe`
  - `which ffmpeg` / `where ffmpeg.exe`

### System Status
- **Command Pattern [Unix/macOS]:** `df -h`, `du -h [directory]`
- **Command Pattern [Windows]:** `dir /s` (rough equivalent)
- **PowerShell Equivalent:** 
  - `Get-PSDrive` (for disk space)
  - `Get-ChildItem -Recurse | Measure-Object -Property Length -Sum` (for folder size)
- **Safety Justification:** Read-only operations that report system status
- **Common Use Cases:** Checking disk space, folder sizes
- **Allowed Options [Unix/macOS]:**
  - `-h` (human-readable sizes)

### Process Viewing
- **Command Pattern [Unix/macOS]:** `ps [options]`
- **Command Pattern [Windows]:** `tasklist`
- **PowerShell Equivalent:** `Get-Process`
- **Safety Justification:** Read-only process listing (without kill/stop options)
- **Common Use Cases:** Checking running processes, diagnosing issues
- **Allowed Options [Unix/macOS]:**
  - `ps aux` (all processes)
- **Allowed Options [Windows]:**
  - `/v` (verbose)
  - `/fi "filter"` (filtering)

## Priority 4: Network Diagnostics

### Connectivity Testing
- **Command Pattern:** `ping [options] [host]`
- **Safety Justification:** Standard diagnostic tool with no modification capabilities
- **Common Use Cases:** Testing network connectivity, checking latency
- **Allowed Options:**
  - `-c [count]` (number of packets)

### DNS Lookup
- **Command Pattern [Unix/macOS]:** `dig [domain]`, `nslookup [domain]`
- **Command Pattern [Windows]:** `nslookup [domain]`
- **PowerShell Equivalent:** `Resolve-DnsName [domain]`
- **Safety Justification:** Read-only DNS querying, informational only
- **Common Use Cases:** Resolving domains, checking DNS records
- **Allowed Options:** Basic options only

### HTTP Headers
- **Command Pattern:** `curl -I [URL]`, `curl --head [URL]`
- **Safety Justification:** Read-only request for HTTP headers
- **Common Use Cases:** Checking website status, examining response headers
- **Allowed Options:**
  - `-I` (head request)

## Priority 5: File & Text Operations

### File Compression Viewing
- **Command Pattern [Unix/macOS]:** `unzip -l [zipfile]`, `tar -tvf [tarfile]`
- **PowerShell Equivalent:** `Expand-Archive -Path [zipfile] -ListOnly`
- **Safety Justification:** Read-only listing of archive contents without extraction
- **Common Use Cases:** Checking archive contents before extraction
- **Allowed Options [Unix/macOS]:**
  - `-l` for unzip (list)
  - `-tvf` for tar (table, verbose, file)
- **Windows Alternative:**
  - `tar -tvf` works in newer Windows 10/11 versions
  - For older versions: `dir [zipfile]` (limited view)

### Text Processing
- **Command Pattern [Unix/macOS]:** `grep [pattern] [file]`, `wc [options] [file]`
- **Command Pattern [Windows]:** `findstr [options] [pattern] [file]`
- **PowerShell Equivalent:** 
  - `Select-String -Pattern [pattern] [file]` (grep equivalent)
  - `(Get-Content [file] | Measure-Object -Line -Word -Character).Words` (wc equivalent)
- **Safety Justification:** Read-only text analysis without file modification
- **Common Use Cases:** Searching file contents, counting lines/words
- **Allowed Options [Unix/macOS]:**
  - `-i` (case insensitive)
  - `-n` (line numbers)
  - `-r` (recursive)
- **Allowed Options [Windows]:**
  - `/i` (case insensitive)
  - `/n` (line numbers)
  - `/s` (recursive)

## PowerShell Specific Commands

These PowerShell cmdlets are useful additions for Windows environments:

### Information Gathering
- **Command Pattern:** `Get-ComputerInfo`
- **Safety Justification:** Read-only system information
- **Common Use Cases:** Checking Windows version, hardware details

### Windows Features
- **Command Pattern:** `Get-WindowsFeature`
- **Safety Justification:** Lists installed Windows features without modification
- **Common Use Cases:** Checking installed components

### Network Information
- **Command Pattern:** `Get-NetIPConfiguration`, `Test-NetConnection`
- **Safety Justification:** Read-only network diagnostics
- **Common Use Cases:** Checking IP configuration, testing connectivity

## Safety Notes

1. This allow list focuses on read-only operations to ensure safety
2. Commands that could modify the system are excluded
3. Any commands that accept file paths are intended to be used with existing files only
4. Network operations are limited to standard diagnostic tools
5. PowerShell commands use the Get-* or Test-* prefix which indicates read-only operations

