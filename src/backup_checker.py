from scanner import scan_folder


def compare_folders(source_folder, backup_folder):

    source_files = scan_folder(source_folder)
    backup_files = scan_folder(backup_folder)

    source_paths = set()
    backup_paths = set()

    for file in source_files:
        source_paths.add(file["relative_path"])

    for file in backup_files:
        backup_paths.add(file["relative_path"])

    missing_files = source_paths - backup_paths
    extra_files = backup_paths - source_paths
    changed_files = []

    for source_file in source_files:

        for backup_file in backup_files:

            if source_file["relative_path"] == backup_file["relative_path"]:

                if source_file["file_hash"] != backup_file["file_hash"]:

                    changed_files.append(
                        source_file["relative_path"]
                    )

    print(f"Файлов в исходной папке: {len(source_files)}")
    print(f"Файлов в резервной копии: {len(backup_files)}")

    print()

    print("Отсутствуют в резервной копии:")

    if not missing_files:
        print("Нет")
    else:
        for file in missing_files:
            print(file)

    print()

    print("Лишние файлы в резервной копии:")

    if not extra_files:
        print("Нет")
    else:
        for file in extra_files:
            print(file)
    
    print()

    print("Изменённые файлы:")

    if not changed_files:
        print("Нет")
    else:
        for file in changed_files:
            print(file)

    return {
    "source_count": len(source_files),
    "backup_count": len(backup_files),
    "missing_count": len(missing_files),
    "extra_count": len(extra_files),
    "changed_count": len(changed_files)
    }