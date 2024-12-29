import os

def sort_m3u():
    # Ask user for input file name
    user_input = input("Enter the input file name (with or without extension): ").strip()
    base_name, ext = os.path.splitext(user_input)
    
    # Normalize the extension to .m3u or .m3u8
    if ext.lower() not in ['.m3u', '.m3u8']:
        ext = '.m3u'  # Default to .m3u if no valid extension is provided
    
    input_file = f"{base_name}{ext}"
    
    # Check if the file exists
    if not os.path.exists(input_file):
        print(f"Error: File '{input_file}' not found.")
        return

    output_file = f"sorted_{base_name}{ext}"  # Output file in the same format as input

    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Parse the file into pairs of #EXTINF and URLs
    entries = []
    current_entry = []
    for line in lines:
        if line.startswith("#EXTINF"):
            if current_entry:  # If there's already an entry being built, store it
                entries.append(current_entry)
            current_entry = [line.strip()]
        elif line.strip() and current_entry:  # Append the URL to the current entry
            current_entry.append(line.strip())
    
    if current_entry:  # Add the last entry
        entries.append(current_entry)

    # Sort entries alphabetically by channel name in #EXTINF
    sorted_entries = sorted(entries, key=lambda x: x[0].lower())

    # Write the sorted entries back to the file
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write("#EXTM3U\n")
        for entry in sorted_entries:
            file.write(f"{entry[0]}\n")
            if len(entry) > 1:
                file.write(f"{entry[1]}\n")
    
    print(f"Sorted M3U file created: {output_file}")

# Run the script
sort_m3u()
