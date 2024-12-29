import sys
import av

def validate_stream(url):
    """Validate a single stream and return its resolution."""
    try:
        with av.open(url) as container:
            video_streams = [stream for stream in container.streams if stream.type == "video"]
            if not video_streams:
                print("No video streams found", file=sys.stderr)
                sys.exit(1)
            
            video_stream = video_streams[0]
            resolution = f"{video_stream.width}x{video_stream.height}"
            print(resolution)
            sys.exit(0)
    except Exception as e:
        print(f"Validation Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python validate_helper.py <stream_url>", file=sys.stderr)
        sys.exit(1)
    
    stream_url = sys.argv[1]
    validate_stream(stream_url)
