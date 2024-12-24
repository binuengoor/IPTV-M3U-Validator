# IPTV M3U Validator

IPTV M3U Validator is a Python-based utility that validates IPTV playlist URLs, extracts stream information such as resolution, and saves the results in an `m3u` format compatible with IPTV players.

## Features

- Validates stream URLs to ensure they are accessible.
- Extracts resolution information from valid streams.
- Includes channel icons in the output (if available).
- Logs detailed results in a log file.
- Provides a summary of active and inactive streams.

---

## Requirements

- Python 3.8+
- FFmpeg installed on your system.

---

## Installation and Usage

### 1. Clone the repository:

```bash
git clone https://github.com/your-username/iptv-validator.git
cd iptv-validator
```

### 2. Create a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies:

```bash
pip install -r requirements.txt
```

### 4. Edit the input file:

Add playlist URLs to `playlist_urls.txt`. Each line should contain a single URL.

Example:
```
https://example.com/playlist1.m3u8
https://example.com/playlist2.m3u8
```

### 5. Run the script:

```bash
python iptv_validator.py
```

The script will:
- Validate the streams.
- Save active streams in `valid_streams.m3u`.
- Log detailed results in `iptv_validator.log`.
- Show live processing updates in the terminal.

---

## Output Files

1. **`valid_streams.m3u`**: Contains valid streams with resolutions and channel icons.
2. **`iptv_validator.log`**: Detailed logs for debugging.

---

## Example Terminal Output

```
✅ - CBS News - 1920x1080
❌ - CNN
✅ - FS1 - 1280x720
❌ - Willow TV

Validation Summary:
  Total Streams: 50
  Active Streams: 25
  Inactive Streams: 25
```

---

## Dependencies

- Python 3.8+
- PyAV: `pip install av`
- Requests: `pip install requests`
- FFmpeg: Install via package manager (e.g., `sudo apt install ffmpeg` on Ubuntu).

---

## Development

### .gitignore

```
# Ignore Python cache files
__pycache__/
*.pyc

# Ignore virtual environment
venv/

# Ignore output files
valid_streams.m3u
iptv_validator.log
```

---

## License

This project is open-source and available under the MIT License.
