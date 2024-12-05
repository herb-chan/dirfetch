import os
import argparse
import time
from datetime import datetime
from collections import defaultdict

# Function to read config and return relevant settings
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

def format_size(size_in_bytes):
    """Format file size in a human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_in_bytes < 1024.0:
            return f"{size_in_bytes:.2f} {unit}"
        size_in_bytes /= 1024.0
    return f"{size_in_bytes:.2f} PB"

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
            subdirectories = dirs  # Only consider current-level subdirectories if non-recursive
        
        for file in files:
            file_path = os.path.join(root, file)
            try:
                file_size = os.path.getsize(file_path)
                file_extension = file.split('.')[-1] if '.' in file else 'no_extension'

                file_sizes[file_extension]["count"] += 1
                file_sizes[file_extension]["size"] += file_size

                file_mtime = os.path.getmtime(file_path)
                if file_mtime > last_changed_time:
                    last_changed_time = file_mtime
                    last_changed_file = file

                total_files += 1
            except FileNotFoundError:
                continue  # Skip files that no longer exist

        if not recursive:  # Stop processing deeper directories if -cd is used
            break

    return total_files, file_sizes, last_changed_file, last_changed_time, subdirectories

def format_date(last_changed_time, config):
    """Format the last modified date based on configuration."""
    if last_changed_time <= 0:
        return "N/A"

    current_time = datetime.now()
    last_changed_dt = datetime.fromtimestamp(last_changed_time)

    date_display_mode = config.get("date_display_mode", "auto")
    date_format = config.get("date_format", "%d.%m.%Y")
    
    time_diff = current_time - last_changed_dt
    days_diff = time_diff.days
    hours_diff = time_diff.seconds // 3600
    minutes_diff = (time_diff.seconds % 3600) // 60
    seconds_diff = time_diff.seconds % 60
    
    if date_display_mode == "auto":
        if days_diff == 0:
            if hours_diff > 0:
                return f"{hours_diff} hours ago"
            elif minutes_diff > 0:
                return f"{minutes_diff} minutes ago"
            else:
                return "Just now"
        elif days_diff <= 7:
            return f"{days_diff} day ago" if days_diff == 1 else f"{days_diff} days ago"
        else:
            return last_changed_dt.strftime(date_format)
    
    elif date_display_mode == "relative_only":
        if days_diff == 0:
            if hours_diff > 0:
                return f"{hours_diff} hours ago"
            elif minutes_diff > 0:
                return f"{minutes_diff} minutes ago"
            else:
                return "Just now"
        else:
            return f"{days_diff} day ago" if days_diff == 1 else f"{days_diff} days ago"
    
    elif date_display_mode == "absolute_only":
        return last_changed_dt.strftime(date_format)

def fetch_directory_info(directory, config, file_details=False, current_only=False):
    include_hidden = config.get("include_hidden_files", "off") == "on"
    total_files, file_sizes, last_changed_file, last_changed_time, subdirectories = count_files_in_directory(directory, recursive=not current_only, include_hidden=include_hidden)
    
    print(f"┌───────── Directory Information ─────────┐")
    
    if config.get("show_total_files", "on") == "on":
        message = config.get("total_files_message", "  Total Files: {}")
        print(message.format(total_files))
    
    if config.get("show_directory_size", "on") == "on":
        directory_size = sum(data["size"] for data in file_sizes.values())
        message = config.get("directory_size_message", "  Directory Size: {}")
        print(message.format(format_size(directory_size)))
    
    if config.get("show_last_modified", "on") == "on":
        message = config.get("last_modified_file_message", "  Last Modified File: {}")
        print(message.format(last_changed_file))
    
    if config.get("show_last_modified_date", "on") == "on":
        formatted_date = format_date(last_changed_time, config)
        message = config.get("last_modified_date_message", "  Last Modified Date: {}")
        print(message.format(formatted_date))
    
    if current_only and subdirectories:
        print("\nSubdirectories:")
        for sub in subdirectories:
            print(f"   {sub}")
    
    print(f"└─────────────────────────────────────────┘")
    
    # Detailed File Information Section
    if file_details or config.get("file_details_enabled", "off") == "on":
        print(f"┌───────── Detailed File Information ─────────┐")
        for ext, data in file_sizes.items():
            message = config.get("fd_file_sizes_message", "  .{}: {} ({} files)")
            print(message.format(ext.lower(), format_size(data['size']), data['count']))
        print(f"└─────────────────────────────────────────────┘")

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
