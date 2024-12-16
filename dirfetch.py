import os
import argparse
import fnmatch
import json
from datetime import datetime
from collections import defaultdict
from rich.console import Console
from rich.style import Style

# Function to read the configuration file and return relevant settings
def load_config(config_file):
    config = {}
    try:
        with open(config_file, "r", encoding="utf-8") as file:
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
    except UnicodeDecodeError:
        print(f"Error decoding the config file '{config_file}'. Please check the file encoding.")
    return config

# Function to load colors from pywal's colors.json
def load_pywal_colors():
    try:
        with open(os.path.expanduser("~/.cache/wal/colors.json"), "r") as file:
            colors = json.load(file)
            return colors['colors']  # Extract the 'colors' dictionary
    except FileNotFoundError:
        print("Pywal colors file not found. Using default colors.")
        return {f"color{i}": "#FFFFFF" for i in range(0, 16)}  # Fallback to white for all colors

# Format file size in a human-readable format
def format_size(size_in_bytes):
    units = ['B', 'KB', 'MB', 'GB', 'TB']
    for unit in units:
        if size_in_bytes < 1024.0:
            return f"{size_in_bytes:.2f} {unit}"
        size_in_bytes /= 1024.0
    return f"{size_in_bytes:.2f} PB"

# Count files and gather size information in the specified directory
def count_files_in_directory(directory, include_hidden=True, exclude_patterns=None, depth=None):
    total_files = 0
    file_sizes = defaultdict(lambda: {"count": 0, "size": 0})
    subdirectories = []
    last_changed_file = None
    last_changed_time = 0

    # Interpret depth correctly
    depth = 0 if depth is None else depth

    for root, dirs, files in os.walk(directory):
        # Calculate current depth relative to the base directory
        current_depth = root[len(directory):].count(os.sep)

        # Stop recursion if depth is exceeded
        if current_depth > depth:
            dirs[:] = []  # Prevent deeper traversal
            continue

        # List subdirectories if at the exact requested depth
        if current_depth == depth:
            subdirectories.extend([d for d in dirs if include_hidden or not d.startswith('.')])

        # Exclude hidden files and directories if configured
        if not include_hidden:
            files = [f for f in files if not f.startswith('.')]
            dirs[:] = [d for d in dirs if not d.startswith('.')]

        # Exclude files matching patterns
        if exclude_patterns:
            for pattern in exclude_patterns:
                files = [f for f in files if not fnmatch.fnmatch(f, pattern)]

        # Process files in the current directory
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
                continue

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

def print_ascii_art(config):
    # Read the path to the ASCII art file from the config
    ascii_art_file = config.get('ascii_art_file', 'assets/ascii/dir.txt')  # Default path if not specified
    
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

def apply_fstring(config_str, local_vars):
    # Make sure we're inserting colors in Rich's format
    for var_name, var_value in local_vars.items():
        if var_name.startswith('cl') and isinstance(var_value, str):
            # Used for colour variables
            config_str = config_str.replace(f"{{{var_name}}}", f"[{var_value}]")
        else:
            # Used for other variables
            config_str = config_str.replace(f"{{{var_name}}}", f"{var_value}")

    return config_str

def fetch_directory_info(directory, config, file_details=False, current_only=False, exclude_patterns=None, depth=None):
    include_hidden = config.get("include_hidden_files", "off") == "on"
    total_files, file_sizes, last_changed_file, last_changed_time, subdirectories = count_files_in_directory(
        directory, include_hidden=include_hidden, exclude_patterns=exclude_patterns, depth=depth
    )
    colors = load_pywal_colors()
    console = Console()

    # Map pywal colors to variables
    cl0 = f"{colors['color0']}"
    cl1 = f"{colors['color1']}"
    cl2 = f"{colors['color2']}"
    cl3 = f"{colors['color3']}"
    cl4 = f"{colors['color4']}"
    cl5 = f"{colors['color5']}"
    cl6 = f"{colors['color6']}"
    cl7 = f"{colors['color7']}"
    cl8 = f"{colors['color8']}"
    cl9 = f"{colors['color9']}"
    cl10 = f"{colors['color10']}"
    cl11 = f"{colors['color11']}"
    cl12 = f"{colors['color12']}"
    cl13 = f"{colors['color13']}"
    cl14 = f"{colors['color14']}"
    cl15 = f"{colors['color15']}"
    cl16 = "reset"
    clb = f"{Style(bold=True)}"

    directory_size = format_size(sum(data['size'] for data in file_sizes.values()))
    formatted_date = format_date(last_changed_time, config)

    ascii_art, ascii_width = print_ascii_art(config)

    if not ascii_art:
        return  # Exit if ASCII art could not be loaded

    directory_info = ""
    if config.get('enable_separators') == 'on': 
        directory_info += f"{config.get('separator_symbol') * 30}\n"
        
    directory_info += apply_fstring(config.get('total_files_message'), locals()) + "\n"
    directory_info += apply_fstring(config.get('directory_size_message'), locals()) + "\n"
    directory_info += apply_fstring(config.get('last_modified_file_message'), locals()) + "\n"
    directory_info += apply_fstring(config.get('last_modified_date_message'), locals()) + "\n"

    if not subdirectories and not file_details:
        if config.get('enable_separators') == 'on': 
            directory_info += f"{config.get('separator_symbol') * 30}\n"

    if subdirectories:
        if config.get('enable_separators') == 'on': 
            directory_info += f"{config.get('separator_symbol') * 30}\n"
        
        for sub in subdirectories:
            directory_info += apply_fstring(config.get('cd_subdirectory_message'), locals()) + "\n"
        
        if not file_details:
            if config.get('enable_separators') == 'on': 
                directory_info += f"{config.get('separator_symbol') * 30}\n"

    if file_details or config.get("file_details_enabled", "off") == "on":
        if config.get('enable_separators') == 'on': 
            directory_info += f"{config.get('separator_symbol') * 30}\n"

        for ext, data in file_sizes.items():
            extension = ext.lower()
            size = format_size(data['size'])
            count = data['count']

            directory_info += apply_fstring(config.get('fd_file_sizes_message'), locals()) + "\n"
        
        if config.get('enable_separators') == 'on': 
            directory_info += f"{config.get('separator_symbol') * 30}\n"

    lines = max(len(ascii_art.splitlines()), len(directory_info.splitlines()))
    
    for i in range(lines):
        ascii_line = (ascii_art.splitlines() + [''] * lines)[i]  # Ensure equal length
        info_line = (directory_info.splitlines() + [''] * lines)[i]  # Ensure equal length
        console.print(f"{ascii_line:<{ascii_width}} {info_line}")

# Main function to parse arguments and execute the program
def main():
    parser = argparse.ArgumentParser(description="Fetch directory information")
    parser.add_argument("directory", help="Directory to fetch information for")
    parser.add_argument("-c", "--config", default="config/dirfetch.conf", help="Path to config file")
    parser.add_argument("-fd", "--file-details", action="store_true", help="Display detailed file information")
    parser.add_argument("-e", "--exclude", nargs="*", help="Exclude files matching these patterns")
    parser.add_argument("-d", "--depth", type=int, help="Limit recursion depth")
    args = parser.parse_args()

    depth = args.depth
    
    config = load_config(args.config)
    fetch_directory_info(
        args.directory, config, 
        file_details=args.file_details, 
        exclude_patterns=args.exclude,
        depth=depth  # Pass the depth value
    )

if __name__ == "__main__":
    main()
