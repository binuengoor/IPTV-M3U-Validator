import os
import requests
import av  # PyAV library
from datetime import datetime

# File paths
INPUT_FILE = "playlist_urls.txt"
VALID_OUTPUT_FILE = "valid_streams.m3u"
LOG_FILE = "iptv_validator.log"

# Timeout settings
TIMEOUT = 30


def initialize_log():
    """Clear and initialize the log file."""
    with open(LOG_FILE, "w") as log:
        log.write(f"IPTV Validator Log - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        log.write("=" * 50 + "\n")


def log_result(status_icon, channel_name, url, error=None, resolution=None):
    """Log a result in a clean, informative format."""
    with open(LOG_FILE, "a") as log:
        log_line = f"{status_icon} - {channel_name} - {url} - "
        if error:
            log_line += f"Error: {error}"
        if resolution:
            log_line += f" - Resolution: {resolution}"
        log.write(log_line.strip() + "\n")


def fetch_playlist(url):
    """Fetch and return the content of a playlist from a URL."""
    try:
        response = requests.get(url, timeout=TIMEOUT)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        log_result("❌", "Playlist Fetch", url, error=str(e))
        return None


def parse_m3u(content):
    """Parse M3U content to extract channel names, URLs, and optional icons."""
    lines = content.splitlines()
    streams = []
    current_channel_name = "Unknown Channel"
    current_icon_url = None

    for line in lines:
        line = line.strip()
        if line.startswith("#EXTINF"):
            parts = line.split(",", 1)
            if len(parts) > 1:
                current_channel_name = parts[1].strip()
            # Extract icon URL if available
            if "tvg-logo=" in line:
                start = line.find('tvg-logo="') + len('tvg-logo="')
                end = line.find('"', start)
                current_icon_url = line[start:end]
        elif line and not line.startswith("#"):
            streams.append((current_channel_name, line, current_icon_url))
            current_icon_url = None  # Reset icon URL for next channel
    return streams


def validate_stream(channel_name, url):
    """Validate a stream using PyAV."""
    try:
        with av.open(url, timeout=TIMEOUT) as container:
            # Check if video streams exist
            video_streams = [stream for stream in container.streams if stream.type == "video"]
            if not video_streams:
                return False, "No video streams found"

            # Check resolution
            video_stream = video_streams[0]  # Assume first video stream
            resolution = f"{video_stream.width}x{video_stream.height}"
            return True, resolution
    except OSError as e:  # Covers HTTP errors like 403 or inaccessible streams
        return False, f"OSError: {e}"
    except Exception as e:
        return False, f"Error: {e}"


def process_playlist_file(file_path):
    """Process URLs from the input file, fetch playlists, and validate streams."""
    if not os.path.exists(file_path):
        print(f"Input file not found: {file_path}")
        return

    initialize_log()
    valid_streams = []
    total_streams = 0
    active_streams = 0
    inactive_streams = 0

    with open(file_path, "r") as file:
        playlist_urls = [line.strip() for line in file if line.strip()]

    for playlist_url in playlist_urls:
        playlist_content = fetch_playlist(playlist_url)
        if not playlist_content:
            continue

        streams = parse_m3u(playlist_content)
        for channel_name, stream_url, icon_url in streams:
            total_streams += 1
            is_valid, result = validate_stream(channel_name, stream_url)
            if is_valid:
                active_streams += 1
                print(f"✅ - {channel_name} - {result}")
                log_result("✅", channel_name, stream_url, resolution=result)

                # Add channel icon if available
                icon_tag = f'tvg-logo="{icon_url}"' if icon_url else ""
                valid_streams.append(f'#EXTINF:-1 {icon_tag},{channel_name} ({result})\n{stream_url}')
            else:
                inactive_streams += 1
                print(f"❌ - {channel_name}")
                log_result("❌", channel_name, stream_url, error=result)

    # Save valid streams to file
    with open(VALID_OUTPUT_FILE, "w") as valid_file:
        valid_file.write("#EXTM3U\n")
        valid_file.write("\n".join(valid_streams))

    # Display summary
    print("\nValidation Summary:")
    print(f"  Total Streams: {total_streams}")
    print(f"  Active Streams: {active_streams}")
    print(f"  Inactive Streams: {inactive_streams}")
    print(f"Results saved to: {LOG_FILE}")
    print(f"Valid streams saved to: {VALID_OUTPUT_FILE}")


if __name__ == "__main__":
    process_playlist_file(INPUT_FILE)
