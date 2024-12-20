import os


def print_ascii_art(config):
    # Expand the ASCII art file path
    ascii_art_file = os.path.expanduser(
        config.get("ascii_art_file", "~/.config/dirfetch/dir.txt")
    )

    try:
        # Read the ASCII art from the file
        with open(ascii_art_file, "r", encoding="utf-8") as file:
            ascii_art = file.read()

    except FileNotFoundError:
        if config.get("enable_ascii_not_found_error") == "on":
            print(
                f"Error: The ASCII art file '{ascii_art_file}' was not found. "
                f"Trying to use the default ASCII art file."
            )

            # Expand the default path as well
            default_ascii_art_file = os.path.expanduser("~/.config/dirfetch/dir.txt")
            if ascii_art_file != default_ascii_art_file:
                try:
                    with open(default_ascii_art_file, "r", encoding="utf-8") as file:
                        ascii_art = file.read()
                except FileNotFoundError:
                    print("Error: Default ASCII art file not found.")
                    return "", 0  # Return empty art and width on failure
        else:
            return "", 0  # Return empty art and width on failure

    # Calculate the width of the ASCII art (longest line + 1)
    ascii_lines = ascii_art.splitlines()
    ascii_width = max(len(line) for line in ascii_lines) + 1

    # Apply bold formatting if needed
    ascii_lines = [f"[bold]{line}" for line in ascii_lines]
    ascii_art = "\n".join(ascii_lines)

    return ascii_art, ascii_width
