from rich.console import Console
from rich.style import Style
from rich.table import Table

from files import count_files_in_directory
from colors import load_pywal_colors
from formatters import format_size, format_date
from ascii import print_ascii_art
from utils import apply_fstring


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
        last_changed_file_path,
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
    table = Table(
        show_header=False, box=None, padding=(0, 1)
    )  # Add padding to each column

    # Add columns for ASCII art and info with a space gap
    table.add_column(
        "", width=ascii_width - 1, justify="left"
    )  # Left padding for the first column
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
