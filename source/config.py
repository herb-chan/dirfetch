import os


def load_config(config_file):
    config = {}
    default_backup_config = {
        "include_hidden_files": "on",
        "show_title": "on",
        "title_message": "{cl10}󰉖 {cl16}: {directory}",
        "date_display_mode": "auto",
        "date_format": "%d.%m.%Y",
        "file_details_enabled": "off",
        "total_files_message": "{cl2} {clb}Files{cl16}: {total_files}",
        "directory_size_message": "{cl4}󰉖 {clb}Size{cl16}: {directory_size}",
        "last_modified_file_message": "{cl1}󱇨 {clb}Changed File{cl16}: {last_changed_file}",
        "last_modified_file_path_message": "{cl6}󱀱 {clb}Changed File Path{cl16}: {last_changed_file_path}",
        "last_modified_date_message": "{cl7}󱋢 {clb}Change Date{cl16}: {formatted_date}",
        "cd_subdirectory_message": "{cl5}󱧩 {clb}SUB{cl16}: {sub}",
        "fd_file_sizes_message": "{cl5}󰓼 {clb}EXT{cl16}: .{extension} {size} ({count})",
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
