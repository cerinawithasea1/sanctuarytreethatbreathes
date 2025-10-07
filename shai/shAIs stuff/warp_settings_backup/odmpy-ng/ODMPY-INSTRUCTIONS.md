# ODMPY-NG Quick Reference Guide

## Basic Usage Instructions

### Running the Script
From any directory:
```bash
odmpy
```

This runs the script with the default config file.

### Step-by-Step Process
1. The script shows available libraries from your config
2. Select a library by entering its number
3. The script logs in to your Overdrive account
4. It displays your currently borrowed audiobooks
5. Select which book to download by entering its number
6. The script downloads and processes the audiobook
7. The finished M4B file is saved in your configured download directory

## Config File

### Location
```
~/.warp/odmpy-ng/config/config.json
```

### Format
```json
{
    "download-dir": "/Users/cerinawithasea/Downloads/audiobooks",
    "libraries": [
        {
            "name": "PPLD",
            "url": "https://ppld.overdrive.com",
            "card_number": "300112703",
            "pin": "0317"
        },
        {
            "name": "KCLS",
            "url": "https://kcls.overdrive.com",
            "card_number": "9340090691",
            "pin": "0084"
        }
    ]
}
```

### Adding More Libraries
To add another library, edit the config.json file and add a new entry to the "libraries" array:
```json
{
    "name": "New Library Name",
    "url": "https://newlibrary.overdrive.com",
    "card_number": "YOUR_CARD_NUMBER",
    "pin": "YOUR_PIN"
}
```

## Common Commands

### Run with Default Config
```bash
odmpy
```

### Run with a Different Config File
```bash
python3 ~/.warp/odmpy-ng/interactive.py /path/to/another/config.json
```

### Edit Your Config File
```bash
nano ~/.warp/odmpy-ng/config/config.json
```

### Update Script Dependencies
```bash
pip3 install -U selenium selenium-wire webdriver-manager requests
```

## Troubleshooting Tips

### FFmpeg Issues
If you see errors related to FFmpeg:
```bash
# Check if FFmpeg is installed
ffmpeg -version

# Install FFmpeg if missing
brew install ffmpeg
```

### Chrome/ChromeDriver Issues
If you see errors related to Chrome:
```bash
# Update Chrome to the latest version
# macOS: App Store or Chrome menu > About Google Chrome

# Clear cookies if login fails
rm ~/.warp/odmpy-ng/cookies
```

### Permission Issues
If you see permission errors:
```bash
# Fix permissions on the script directory
chmod -R u+rw ~/.warp/odmpy-ng

# Make sure download directory exists
mkdir -p ~/Downloads/audiobooks
```

### Downloaded File Issues
If the downloaded file has problems:
```bash
# Verify your M4B file
ls -la ~/Downloads/audiobooks

# Check file integrity
ffprobe ~/Downloads/audiobooks/Author/Title/Title.m4b
```

