import sys
import os

from db import (
    initialize_database,
    save_files,
    get_files_count,
    find_duplicates,
    save_backup_check
)

from scanner import scan_folder
from backup_checker import compare_folders
from db import get_backup_checks_count


def main():

    if len(sys.argv) < 2:
        print("Укажите путь к папке.")
        return

    folder_path = sys.argv[1]

    if not os.path.exists(folder_path):
        print("Указанная папка не существует.")
        return

    if not os.path.isdir(folder_path):
        print("Указанный путь не является папкой.")
        return

    initialize_database()

    files = scan_folder(folder_path)

    save_files(files)

    count = get_files_count()

    print(f"В базе данных записей: {count}")
    print(f"Папка найдена: {folder_path}")
    print(f"Найдено файлов: {len(files)}")
    print("Данные успешно сохранены в базу данных.")

    print()
    print("Дубликаты:")

    duplicates = find_duplicates()

    if not duplicates:
        print("Дубликаты не найдены.")
    else:
        for duplicate in duplicates:

            print()
            print("Хэш:")
            print(duplicate["hash"])

            print("Файлы:")

            for file in duplicate["files"]:
                print(file[0])

    if len(sys.argv) >= 3:

        backup_folder = sys.argv[2]

        if not os.path.exists(backup_folder):
            print("Папка резервной копии не существует.")
        else:
            print()
            print("Проверка резервной копии:")

            result = compare_folders(
                folder_path,
                backup_folder
            )

            save_backup_check(
                result["source_count"],
                result["backup_count"],
                result["missing_count"],
                result["extra_count"],
                result["changed_count"]
            )

            print()
    print(
        f"Записей о проверках: "
        f"{get_backup_checks_count()}"
    )

    print()

    for file in files:
        print(file)


if __name__ == "__main__":
    main()