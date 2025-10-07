# ODMPY-NG: Overdrive Audiobook Downloader

An improved tool for downloading and converting Overdrive/Libby audiobooks to M4B format with proper chapters and metadata.

## Requirements

### For All Platforms
- Python 3.7 or later
- FFmpeg (required for audio conversion)
- Chrome browser (for web automation)
- Python packages:
  - selenium
  - selenium-wire
  - webdriver-manager
  - requests

### macOS Specific
- Homebrew (recommended for installing FFmpeg)

### Windows Specific
- FFmpeg added to system PATH

## Installation

### macOS

1. Install Python from python.org or using Homebrew:
   ```
   brew install python
   ```

2. Install FFmpeg using Homebrew:
   ```
   brew install ffmpeg
   ```

3. Install required Python packages:
   ```
   pip3 install selenium selenium-wire webdriver-manager requests
   ```

### Windows

1. Install Python from [python.org](https://www.python.org/downloads/windows/)
   - Make sure to check "Add Python to PATH" during installation

2. Download FFmpeg from [ffmpeg.org](https://ffmpeg.org/download.html#build-windows)
   - Extract to a folder (e.g., C:\ffmpeg)
   - Add the bin folder to your system PATH:
     1. Open System Properties > Advanced > Environment Variables
     2. Edit the PATH variable
     3. Add a new entry: C:\ffmpeg\bin (or your extraction path)

3. Install required Python packages:
   ```
   pip install selenium selenium-wire webdriver-manager requests
   ```

## Configuration

Create a `config/config.json` file with your library information:

### Single Library
```json
{
    "download-dir": "/path/to/your/audiobooks",
    "libraries": [
        {
            "name": "My Library",
            "url": "https://yourlibrary.overdrive.com",
            "card_number": "YOUR_CARD_NUMBER",
            "pin": "YOUR_PIN"
        }
    ]
}
```

### Multiple Libraries
```json
{
    "download-dir": "/path/to/your/audiobooks",
    "libraries": [
        {
            "name": "Library 1",
            "url": "https://library1.overdrive.com",
            "card_number": "CARD_NUMBER_1",
            "pin": "PIN_1"
        },
        {
            "name": "Library 2",
            "url": "https://library2.overdrive.com",
            "card_number": "CARD_NUMBER_2",
            "pin": "PIN_2"
        }
    ]
}
```

Replace the placeholders with your actual information.

## Usage

Run the interactive script:

```
python interactive.py config/config.json
```

The script will:
1. Ask you to select a library (if you have multiple configured)
2. Log in to your Overdrive account
3. Show your currently borrowed audiobooks
4. Let you select which book to download
5. Download and process the audiobook
6. Convert it to M4B format with chapters and metadata
7. Save it to your configured download directory

## Components

- **interactive.py**: The main script you'll run
- **scraper.py**: Extracts book data including audio URLs, cover art and chapter info
- **overdrive_download.py**: Downloads the audiobook parts
- **ffmetadata.py**: Creates metadata files for chapter information
- **file_conversions.py**: Converts MP3s to M4B with proper metadata

## Troubleshooting

### FFmpeg Issues
- Make sure FFmpeg is correctly installed and in your PATH
- On Windows, you may need to restart your computer after adding FFmpeg to PATH
- Test FFmpeg installation by running `ffmpeg -version` in a terminal

### Chrome/ChromeDriver Issues
- The script uses webdriver-manager to handle ChromeDriver installation automatically
- If you encounter issues, try updating Chrome to the latest version

### Permissions Issues
- Make sure you have write permissions for the download directory
- On Windows, you might need to run the script as Administrator if installing in protected folders

## Example Commands

### Basic Usage
```
python interactive.py config/config.json
```

### Using a Different Config File
```
python interactive.py path/to/another-config.json
```

## Notes

- Downloaded audiobooks are saved as M4B files with proper chapters, metadata, and cover art
- Temporary files are automatically cleaned up after successful conversion
- A cookies file is created to enable quicker logins in future sessions
- The download process may take some time, especially for books with many chapters
