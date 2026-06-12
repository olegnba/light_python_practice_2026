import sys
import os

from db import initialize_database


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

    print(f"Папка найдена: {folder_path}")
    print("База данных успешно создана.")


if __name__ == "__main__":
    main()