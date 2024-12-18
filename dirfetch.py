import os
import argparse
import fnmatch
import json
import platform
from datetime import datetime
from collections import defaultdict
from rich.console import Console
from rich.style import Style
from rich.table import Table


# Function to read the configuration file and return relevant settings
def load_config(config_file):
    config = {}
    default_backup_config = {
        "include_hidden_files": "on",
        "show_title": "on",
        "title_message": "{cl10}U000f0256 {cl16}: {directory}",
        "date_display_mode": "auto",
        "date_format": "%d.%m.%Y",
        "file_details_enabled": "off",
        "total_files_message": "{cl2}\uf0c5 {clb}Files{cl16}: {total_files}",
        "directory_size_message": "{cl4}U000f0256 {clb}Size{cl16}: {directory_size}",
        "last_modified_file_message": "{cl1}U000f11e8 {clb}Changed File{cl16}: {last_changed_file}",
        "last_modified_file_path_message": "{cl6}U000f1031 {clb}Changed File Path{cl16}: {file_path}",
        "last_modified_date_message": "{cl7}U000f12e2 {clb}Change Date{cl16}:  {formatted_date}",
        "cd_subdirectory_message": "{cl5}U000f19e9 {clb}SUB{cl16}: {sub}",
        "fd_file_sizes_message": "{cl5}U000f04fc {clb}EXT{cl16}: .{extension} {size} ({count})",
        "ascii_art_file": "assets/ascii/dir_small.txt",
        "enable_separators": "on",
        "separator_symbol": "─",
        "separator_length": "35",
        "enable_pywal_not_found_error": "off",
        "enable_json_decode_error": "off",
        "enable_file_not_found_error": "off",
        "enable_ascii_not_found_error": "off",
    }

    try:
        with open(config_file, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                # Skip blank lines and comments
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, value = line.split("=", 1)
                    config[key.strip()] = value.split("#", 1)[0].strip().strip('"')

    except FileNotFoundError:
        print(f"Config file '{config_file}' not found. Using default settings.")
        config = default_backup_config

    except UnicodeDecodeError:
        print(
            f"Error decoding the config file '{config_file}'. Please check the file encoding."
        )

    return config


# Function to load colors from pywal's colors.json
def load_pywal_colors(config):
    os_name = platform.system()

    if os_name == "Windows":
        user = os.getlogin()
        colors_path = os.path.expanduser(f"C:\\Users\\{user}\\.cache\\wal\\colors.json")
    else:
        colors_path = os.path.expanduser("~/.cache/wal/colors.json")

    try:
        with open(colors_path, "r", encoding="utf-8") as file:
            colors = json.load(file)
            return colors["colors"]  # Extract the 'colors' dictionary

    except FileNotFoundError:
        if config.get("enable_pywal_not_found_error") == "on":
            print("Pywal colors file not found. Using default colors.")

        return {
            f"color{i}": "#FFFFFF" for i in range(0, 16)
        }  # Fallback to white for all colors

    except json.JSONDecodeError as e:
        if config.get("enable_json_decode_error") == "on":
            print(f"JSONDecodeError: {e.msg} at line {e.lineno} column {e.colno}")

        return {
            f"color{i}": "#FFFFFF" for i in range(0, 16)
        }  # Fallback to white for all colors


# Format file size in a human-readable format
def format_size(size_in_bytes):
    units = ["B", "KB", "MB", "GB", "TB"]
    for unit in units:
        if size_in_bytes < 1024.0:
            return f"{size_in_bytes:.2f} {unit}"
        size_in_bytes /= 1024.0
    return f"{size_in_bytes:.2f} PB"


# Count files and gather size information in the specified directory
def count_files_in_directory(
    directory, config, include_hidden=True, exclude_patterns=None, depth=None
):
    total_files = 0
    file_sizes = defaultdict(lambda: {"count": 0, "size": 0})
    subdirectories = []
    last_changed_file = None
    last_changed_time = 0

    # Interpret depth correctly
    depth = 0 if depth is None else depth

    for root, dirs, files in os.walk(directory):
        # Calculate current depth relative to the base directory
        current_depth = root[len(directory) :].count(os.sep)

        # Stop recursion if depth is exceeded
        if current_depth > depth:
            dirs[:] = []  # Prevent deeper traversal
            continue

        # List subdirectories if at the exact requested depth
        if current_depth == depth:
            subdirectories.extend(
                [d for d in dirs if include_hidden or not d.startswith(".")]
            )

        # Exclude hidden files and directories if configured
        if not include_hidden:
            files = [f for f in files if not f.startswith(".")]
            dirs[:] = [d for d in dirs if not d.startswith(".")]

        # Exclude files matching patterns
        if exclude_patterns:
            for pattern in exclude_patterns:
                files = [f for f in files if not fnmatch.fnmatch(f, pattern)]

        # Process files in the current directory
        for file in files:
            file_path = os.path.join(root, file)
            try:
                file_size = os.path.getsize(file_path)
                file_extension = (
                    file.rsplit(".", 1)[-1] if "." in file else "no_extension"
                )

                file_sizes[file_extension]["count"] += 1
                file_sizes[file_extension]["size"] += file_size

                file_mtime = os.path.getmtime(file_path)
                if file_mtime > last_changed_time:
                    last_changed_time = file_mtime
                    last_changed_file = file

                total_files += 1

            except FileNotFoundError as e:
                if config.get("enable_file_not_found_error"):
                    print(f"File not found: {file_path}.\nError: {str(e)}")

                continue

    return (
        total_files,
        file_sizes,
        last_changed_file,
        file_path,
        last_changed_time,
        subdirectories,
    )


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
    ascii_art_file = config.get(
        "ascii_art_file", "assets/ascii/dir.txt"
    )  # Default path if not specified

    # Read the ASCII art from the file
    try:
        with open(ascii_art_file, "r") as file:
            ascii_art = file.read()

    except FileNotFoundError:
        if config.get("enable_ascii_not_found_error") == "on":
            print(
                f"Error: The ASCII art file '{ascii_art_file}' was not found. Trying to use the default ASCII art file."
            )

            if ascii_art_file != "assets/ascii/dir.txt":
                try:
                    with open("assets/ascii/dir.txt", "r") as file:
                        ascii_art = file.read()

                except FileNotFoundError:
                    print(f"Error: Default ASCII art file not found.")

        return "", 0  # Return empty art and 0 width in case of error

    # Calculate the width of the ASCII art (longest line + 1)
    ascii_lines = ascii_art.splitlines()
    ascii_width = max(len(line) for line in ascii_lines) + 1

    ascii_lines = [f"[bold]{line}" for line in ascii_lines]
    ascii_art = "\n".join(ascii_lines)

    return ascii_art, ascii_width


def apply_fstring(config_str, local_vars):
    # Make sure we're inserting colors in Rich's format
    for var_name, var_value in local_vars.items():
        if var_name.startswith("cl") and isinstance(var_value, str):
            # Used for colour variables
            config_str = config_str.replace(f"{{{var_name}}}", f"[{var_value}]")
        else:
            # Used for other variables
            config_str = config_str.replace(f"{{{var_name}}}", f"{var_value}")

    return config_str



def fetch_directory_info(
    directory,
    config,
    file_details=False,
    exclude_patterns=None,
    depth=None,
):
    include_hidden = config.get("include_hidden_files", "off") == "on"
    (
        total_files,
        file_sizes,
        last_changed_file,
        file_path,
        last_changed_time,
        subdirectories,
    ) = count_files_in_directory(
        directory,
        config,
        include_hidden=include_hidden,
        exclude_patterns=exclude_patterns,
        depth=depth,
    )
    colors = load_pywal_colors(config)
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

    directory_size = format_size(sum(data["size"] for data in file_sizes.values()))
    formatted_date = format_date(last_changed_time, config)

    ascii_art, ascii_width = print_ascii_art(config)

    if not ascii_art:
        return  # Exit if ASCII art could not be loaded

    directory_info = ""

    if config.get("show_title") == "on":
        directory_info += apply_fstring(config.get("title_message"), locals()) + "\n"

    if config.get("enable_separators") == "on":
        directory_info += (
            f"{config.get('separator_symbol') * int(config.get('separator_length'))}\n"
        )

    directory_info += apply_fstring(config.get("total_files_message"), locals()) + "\n"
    directory_info += (
        apply_fstring(config.get("directory_size_message"), locals()) + "\n"
    )
    directory_info += (
        apply_fstring(config.get("last_modified_file_message"), locals()) + "\n"
    )
    directory_info += (
        apply_fstring(config.get("last_modified_file_path_message"), locals()) + "\n"
    )
    directory_info += (
        apply_fstring(config.get("last_modified_date_message"), locals()) + "\n"
    )

    if not subdirectories and not file_details:
        if config.get("enable_separators") == "on":
            directory_info += f"{config.get('separator_symbol') * int(config.get('separator_length'))}\n"

    if subdirectories:
        if config.get("enable_separators") == "on":
            directory_info += f"{config.get('separator_symbol') * int(config.get('separator_length'))}\n"

        for sub in subdirectories:
            directory_info += (
                apply_fstring(config.get("cd_subdirectory_message"), locals()) + "\n"
            )

        if not file_details:
            if config.get("enable_separators") == "on":
                directory_info += f"{config.get('separator_symbol') * int(config.get('separator_length'))}\n"

    if file_details or config.get("file_details_enabled", "off") == "on":
        if config.get("enable_separators") == "on":
            directory_info += f"{config.get('separator_symbol') * int(config.get('separator_length'))}\n"

        for ext, data in file_sizes.items():
            extension = ext.lower()
            size = format_size(data["size"])
            count = data["count"]

            directory_info += (
                apply_fstring(config.get("fd_file_sizes_message"), locals()) + "\n"
            )

        if config.get("enable_separators") == "on":
            directory_info += f"{config.get('separator_symbol') * int(config.get('separator_length'))}\n"

    # Create a Table for better presentation
    table = Table(show_header=False, box=None, padding=(0, 1))  # Add padding to each column

    # Add columns for ASCII art and info with a space gap
    table.add_column("", width=ascii_width, justify="left")  # Left padding for the first column
    table.add_column("", width=60, justify="left")  # Left padding for the second column

    
    ascii_lines = ascii_art.splitlines()
    directory_info_lines = directory_info.splitlines()
    
    # Add rows with ASCII art and info side by side
    for i in range(max(len(ascii_lines), len(directory_info_lines))):
        ascii_line = (ascii_lines + [""] * len(directory_info_lines))[i]
        info_line = (directory_info_lines + [""] * len(ascii_lines))[i]

        table.add_row(ascii_line, info_line)
    
    # Print the table
    console.print(table)


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Fetch directory information with customizable options.\n\n"
            "Example usage:\n"
            "  python dirfetch.py /path/to/dir -fd -c custom.conf -e '*.log' -d 2"
        ),
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "directory", help="The target directory to fetch information from."
    )

    # Configuration Group
    config_group = parser.add_argument_group("Configuration")
    config_group.add_argument(
        "-c",
        "--config",
        default="config/dirfetch.conf",
        help="Path to the config file (default: config/dirfetch.conf).",
    )

    # Display Options
    display_group = parser.add_argument_group("Display Options")
    display_group.add_argument(
        "-fd",
        "--file-details",
        action="store_true",
        help="Show detailed file information.",
    )
    display_group.add_argument(
        "-e",
        "--exclude",
        nargs="*",
        metavar="PATTERN",
        help="Exclude files matching these patterns (e.g., '*.tmp' '*.log').",
    )
    display_group.add_argument(
        "-d",
        "--depth",
        type=int,
        metavar="LEVEL",
        help="Limit recursion depth when fetching directory contents.",
    )

    args = parser.parse_args()

    depth = args.depth
    config = load_config(args.config)
    fetch_directory_info(
        args.directory,
        config,
        file_details=args.file_details,
        exclude_patterns=args.exclude,
        depth=depth,
    )


if __name__ == "__main__":
    main()
