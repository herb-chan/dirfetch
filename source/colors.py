import os
import json
import platform


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
