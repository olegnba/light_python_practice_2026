from pathlib import Path
from datetime import datetime

from hash_utils import calculate_file_hash


IGNORE_DIRS = {
    ".git",
    "__pycache__",
    "data"
}

IGNORE_FILES = {
    ".gitkeep"
}


def scan_folder(folder_path, extension_filter=None):

    files_data = []

    root_folder = Path(folder_path)

    scan_recursive(
        root_folder,
        root_folder,
        extension_filter,
        files_data
    )

    return files_data


def scan_recursive(
    current_folder,
    root_folder,
    extension_filter,
    files_data
):

    for item in current_folder.iterdir():

        if item.is_dir():

            if item.name in IGNORE_DIRS:
                continue

            scan_recursive(
                item,
                root_folder,
                extension_filter,
                files_data
            )

        elif item.is_file():

            if item.name in IGNORE_FILES:
                continue

            if extension_filter is not None:
                if item.suffix != extension_filter:
                    continue

            stat = item.stat()

            modified_time = datetime.fromtimestamp(
                stat.st_mtime
            ).strftime("%Y-%m-%d %H:%M:%S")

            files_data.append({
                "relative_path": str(item.relative_to(root_folder)),
                "size": stat.st_size,
                "modified_time": modified_time,
                "extension": item.suffix,
                "file_hash": calculate_file_hash(item)
            })