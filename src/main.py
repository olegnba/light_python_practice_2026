import sys
import os

from db import initialize_database, save_files, get_files_count
from scanner import scan_folder
from db import find_duplicates


def main():
    if len(sys.argv) < 2:
        print("Укажите путь к папке.")
        return

    folder_path = sys.argv[1]

    extension_filter = None

    if len(sys.argv) >= 3:
        extension_filter = sys.argv[2]

    if not os.path.exists(folder_path):
        print("Указанная папка не существует.")
        return

    if not os.path.isdir(folder_path):
        print("Указанный путь не является папкой.")
        return

    initialize_database()

    files = scan_folder(folder_path, extension_filter)

    save_files(files)

    count = get_files_count()

    duplicates = find_duplicates()

    print()
    print("Дубликаты:")

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

    print(f"В базе данных записей: {count}")

    print(f"Папка найдена: {folder_path}")
    print(f"Найдено файлов: {len(files)}")
    print("Данные успешно сохранены в базу данных.")

    for file in files:
        print(file)


if __name__ == "__main__":
    main()