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
