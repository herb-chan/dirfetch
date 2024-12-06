import os
import argparse
from datetime import datetime
from collections import defaultdict

# Function to read the configuration file and return relevant settings
def load_config(config_file):
    config = {}
    try:
        with open(config_file, "r") as file:
            for line in file:
                line = line.strip()
                # Skip blank lines and comments
                if not line or line.startswith("#"):
                    continue
                if '=' in line:
                    key, value = line.split("=", 1)
                    config[key.strip()] = value.split("#", 1)[0].strip().strip('"')
    except FileNotFoundError:
        print(f"Config file '{config_file}' not found. Using default settings.")
    return config

# Format file size in a human-readable format
def format_size(size_in_bytes):
    units = ['B', 'KB', 'MB', 'GB', 'TB']
    for unit in units:
        if size_in_bytes < 1024.0:
            return f"{size_in_bytes:.2f} {unit}"
        size_in_bytes /= 1024.0
    return f"{size_in_bytes:.2f} PB"

# Count files and gather size information in the specified directory
def count_files_in_directory(directory, recursive=True, include_hidden=True):
    total_files = 0
    file_sizes = defaultdict(lambda: {"count": 0, "size": 0})
    subdirectories = []
    last_changed_file = None
    last_changed_time = 0

    for root, dirs, files in os.walk(directory):
        if not include_hidden:
            files = [f for f in files if not f.startswith('.')]
            dirs[:] = [d for d in dirs if not d.startswith('.')]

        if not recursive:
            subdirectories = dirs  # Consider only current-level subdirectories if non-recursive
        
        for file in files:
            file_path = os.path.join(root, file)
            try:
                file_size = os.path.getsize(file_path)
                file_extension = file.rsplit('.', 1)[-1] if '.' in file else 'no_extension'

                file_sizes[file_extension]["count"] += 1
                file_sizes[file_extension]["size"] += file_size

                file_mtime = os.path.getmtime(file_path)
                if file_mtime > last_changed_time:
                    last_changed_time = file_mtime
                    last_changed_file = file

                total_files += 1
            except FileNotFoundError:
                continue  # Skip files that no longer exist

        if not recursive:
            break  # Stop processing deeper directories if non-recursive mode

    return total_files, file_sizes, last_changed_file, last_changed_time, subdirectories

# Format the last modified date based on configuration
def format_date(last_changed_time, config):
    if last_changed_time <= 0:
        return "N/A"

    current_time = datetime.now()
    last_changed_dt = datetime.fromtimestamp(last_changed_time)

    date_display_mode = config.get("date_display_mode", "auto")
    date_format = config.get("date_format", "%d.%m.%Y")

    time_diff = current_time - last_changed_dt
    days_diff, seconds_diff = divmod(time_diff.total_seconds(), 86400)
    hours_diff, remainder = divmod(seconds_diff, 3600)
    minutes_diff, _ = divmod(remainder, 60)

    if date_display_mode == "auto":
        if days_diff == 0:
            if hours_diff > 0:
                return f"{int(hours_diff)} hours ago"
            elif minutes_diff > 0:
                return f"{int(minutes_diff)} minutes ago"
            else:
                return "Just now"
        elif days_diff <= 7:
            return f"{int(days_diff)} day{'s' if days_diff > 1 else ''} ago"
        else:
            return last_changed_dt.strftime(date_format)

    if date_display_mode == "relative_only":
        if days_diff == 0:
            if hours_diff > 0:
                return f"{int(hours_diff)} hours ago"
            elif minutes_diff > 0:
                return f"{int(minutes_diff)} minutes ago"
            return "Just now"
        return f"{int(days_diff)} day{'s' if days_diff > 1 else ''} ago"

    return last_changed_dt.strftime(date_format)  # Absolute mode by default

# Function to print ASCII art
def print_ascii_art():
    ascii_art = """
                   -`
                  .o+`
                 `ooo/
                `+oooo:
               `+oooooo:
               -+oooooo+:
             `/:-:++oooo+:
            `/++++/+++++++:
           `/++++++++++++++:
          `/+++ooooooooooooo/`
         ./ooosssso++osssssso+`
        .oossssso-````/ossssss+`
       -osssssso.      :ssssssso.
      :osssssss/        osssso+++
     /ossssssss/        +ssssooo/-
   `/ossssso+/:-        -:/+osssso+-
  `+sso+:-`                 `.-/+oso:
 `++:.                           `-/+/
 .`                                 `
    """
    print(ascii_art)

# Display directory information based on the configuration
# Function to display ASCII art next to directory information
def print_ascii_art():
    ascii_art = """
                   -`
                  .o+`
                 `ooo/
                `+oooo:
               `+oooooo:
               -+oooooo+:
             `/:-:++oooo+:
            `/++++/+++++++:
           `/++++++++++++++:
          `/+++ooooooooooooo/`
         ./ooosssso++osssssso+`
        .oossssso-````/ossssss+`
       -osssssso.      :ssssssso.
      :osssssss/        osssso+++
     /ossssssss/        +ssssooo/-
   `/ossssso+/:-        -:/+osssso+-
  `+sso+:-`                 `.-/+oso:
 `++:.                           `-/+/
 .`                                 `
    """
    return ascii_art

# Display directory information aligned next to ASCII art
def print_ascii_art():
    # Your ASCII art
    ascii_art = """
                   -`
                  .o+`
                 `ooo/
                `+oooo:
               `+oooooo:
               -+oooooo+:
             `/:-:++oooo+:
            `/++++/+++++++:
           `/++++++++++++++:
          `/+++ooooooooooooo/`
         ./ooosssso++osssssso+`
        .oossssso-````/ossssss+`
       -osssssso.      :ssssssso.
      :osssssss/        osssso+++
     /ossssssss/        +ssssooo/-
   `/ossssso+/:-        -:/+osssso+-
  `+sso+:-`                 `.-/+oso:
 `++:.                           `-/+/
 .`                                 `
    """
    return ascii_art


def print_ascii_art(config):
    # Read the path to the ASCII art file from the config
    ascii_art_file = config.get('ascii_art_file', 'config/ascii_art.txt')  # Default path if not specified
    
    # Read the ASCII art from the file
    try:
        with open(ascii_art_file, 'r') as file:
            ascii_art = file.read()
    except FileNotFoundError:
        print(f"Error: The ASCII art file '{ascii_art_file}' was not found.")
        return '', 0  # Return empty art and 0 width in case of error
    
    # Calculate the width of the ASCII art (longest line + 1)
    ascii_lines = ascii_art.splitlines()
    ascii_width = max(len(line) for line in ascii_lines) + 1
    
    return ascii_art, ascii_width

def fetch_directory_info(directory, config, file_details=False, current_only=False):
    # Assume count_files_in_directory and other necessary functions are defined elsewhere
    include_hidden = config.get("include_hidden_files", "off") == "on"
    total_files, file_sizes, last_changed_file, last_changed_time, subdirectories = count_files_in_directory(
        directory, recursive=not current_only, include_hidden=include_hidden
    )

    # Get the ASCII art and its width
    ascii_art, ascii_width = print_ascii_art(config)

    if not ascii_art:
        return  # Exit if ASCII art could not be loaded

    # Prepare the directory info (right side)
    directory_info = ""
    directory_info += "┌─────────── Directory Information ───────────┐\n"
    directory_info += f"{config.get('total_files_message', '    Total Files: {}').format(total_files)}\n"
    directory_info += f"{config.get('directory_size_message', '󰉖    Directory Size: {}').format(format_size(sum(data['size'] for data in file_sizes.values())))}\n"
    directory_info += f"{config.get('last_modified_file_message', '󱇨    Last Modified File: {}').format(last_changed_file)}\n"
    directory_info += f"{config.get('last_modified_date_message', '󱋢    Last Modified Date: {}').format(format_date(last_changed_time, config))}\n"

    # Only add a closing divider if there's no subdirectories and not current_only
    if not subdirectories and not file_details:
        directory_info += "└─────────────────────────────────────────────┘\n"

    # If subdirectories exist, add a section for subdirectories
    if subdirectories:
        directory_info += "├─────────────── Subdirectories ──────────────┤\n"
        
        for sub in subdirectories:
            directory_info += f"{config.get('cd_subdirectory_message', '󱧩    {}').format(sub)}\n"
        
        if not file_details:
            directory_info += "└─────────────────────────────────────────────┘\n"

    # Handle file details section if required
    if file_details or config.get("file_details_enabled", "off") == "on":
        directory_info += "├───────── Detailed File Information ─────────┤\n"
        for ext, data in file_sizes.items():
            directory_info += f"{config.get('fd_file_sizes_message', '󰓼    .{}: {} ({} files)').format(ext.lower(), format_size(data['size']), data['count'])}\n"
        directory_info += "└─────────────────────────────────────────────┘\n"

    # Now, print ASCII art and directory info side by side
    lines = max(len(ascii_art.splitlines()), len(directory_info.splitlines()))
    
    for i in range(lines):
        ascii_line = (ascii_art.splitlines() + [''] * lines)[i]  # Ensure equal length
        info_line = (directory_info.splitlines() + [''] * lines)[i]  # Ensure equal length
        print(f"{ascii_line:<{ascii_width}} {info_line}")


# Main function to parse arguments and execute the program
def main():
    parser = argparse.ArgumentParser(description="Fetch directory information")
    parser.add_argument("directory", help="Directory to fetch information for")
    parser.add_argument("-c", "--config", default="config/dirfetch.conf", help="Path to config file")
    parser.add_argument("-fd", "--file-details", action="store_true", help="Show detailed file information")
    parser.add_argument("-cd", "--current-directory", action="store_true", help="Limit to current directory (non-recursive)")

    args = parser.parse_args()
    config = load_config(args.config)
    
    current_directory_mode = args.current_directory or config.get("current_directory_mode", "off") == "on"
    fetch_directory_info(args.directory, config, file_details=args.file_details, current_only=current_directory_mode)

if __name__ == "__main__":
    main()
