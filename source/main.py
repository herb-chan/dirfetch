import argparse

from display import fetch_directory_info
from config import load_config


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
