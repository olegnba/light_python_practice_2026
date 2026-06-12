import os
from datetime import datetime

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

    for root, dirs, files in os.walk(folder_path):

        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

        for file_name in files:

            if file_name in IGNORE_FILES:
                continue

            full_path = os.path.join(root, file_name)

            relative_path = os.path.relpath(full_path, folder_path)

            size = os.path.getsize(full_path)

            modified_time = os.path.getmtime(full_path)

            modified_time = datetime.fromtimestamp(
                modified_time
            ).strftime("%Y-%m-%d %H:%M:%S")

            extension = os.path.splitext(file_name)[1]

            if extension_filter is not None:
                if extension != extension_filter:
                    continue

            files_data.append({
                "relative_path": relative_path,
                "size": size,
                "modified_time": modified_time,
                "extension": extension
            })

    return files_data