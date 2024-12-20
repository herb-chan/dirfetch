import os
import fnmatch
from collections import defaultdict


def count_files_in_directory(
    directory, config, include_hidden=True, exclude_patterns=None, depth=None
):
    total_files = 0
    file_sizes = defaultdict(lambda: {"count": 0, "size": 0})
    subdirectories = []
    last_changed_file = None
    last_changed_file_path = None
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
                    last_changed_file_path = file_path

                total_files += 1

            except FileNotFoundError as e:
                if config.get("enable_file_not_found_error"):
                    print(f"File not found: {file_path}.\nError: {str(e)}")

                continue

    return (
        total_files,
        file_sizes,
        last_changed_file,
        last_changed_file_path,
        last_changed_time,
        subdirectories,
    )
