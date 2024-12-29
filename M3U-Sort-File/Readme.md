# M3U Playlist Sorter

This script sorts the entries in an M3U playlist file alphabetically by the channel name specified in `#EXTINF` metadata lines. It is useful for organizing IPTV playlists or audio/media playlists.

## Features

- Reads M3U or M3U8 playlist files
- Sorts entries alphabetically based on `#EXTINF` lines
- Preserves the `#EXTM3U` header
- Outputs the sorted playlist as a new file with the prefix `sorted_`

## How to Use

1. Clone or download this repository
2. Place your `.m3u` or `.m3u8` file in the same directory as the script
3. Run the script:

```bash
python sort_m3u.py
```

Enter the name of the input file when prompted (with or without extension).
The sorted playlist will be created in the same directory as `sorted_<original_filename>.m3u`.

## Example

Input file: `playlist.m3u`

```plaintext
#EXTM3U
#EXTINF:-1, Channel B
http://example.com/stream_b
#EXTINF:-1, Channel A
http://example.com/stream_a
```

Output file: `sorted_playlist.m3u`

```plaintext
#EXTM3U
#EXTINF:-1, Channel A
http://example.com/stream_a
#EXTINF:-1, Channel B
http://example.com/stream_b
```

## Requirements

- Python 3.x
- UTF-8 encoded M3U file

## Notes

- The script checks if the file exists before processing
- Handles .m3u and .m3u8 extensions automatically