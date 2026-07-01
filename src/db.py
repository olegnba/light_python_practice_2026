import sqlite3
from datetime import datetime


def initialize_database():
    connection = sqlite3.connect("data/app.db")     
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            relative_path TEXT NOT NULL,
            size INTEGER,
            modified_time TEXT,
            extension TEXT,
            file_hash TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS backup_checks (      
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            check_time TEXT,
            source_count INTEGER,
            backup_count INTEGER,
            missing_count INTEGER,
            extra_count INTEGER,
            changed_count INTEGER
        )
    """)

    connection.commit()
    connection.close()


def save_files(files_data):                                                #очистили files и добавили новые данные
    connection = sqlite3.connect("data/app.db")
    cursor = connection.cursor()

    cursor.execute("DELETE FROM files")

    for file in files_data:
        cursor.execute("""
            INSERT INTO files (
                relative_path,
                size,
                modified_time,
                extension,
                file_hash
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            file["relative_path"],
            file["size"],
            file["modified_time"],
            file["extension"],
            file["file_hash"]
        ))

    connection.commit()
    connection.close()


def get_files_count():
    connection = sqlite3.connect("data/app.db")
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM files")   #считаем количество записей в files

    count = cursor.fetchone()[0]          #извлекаем результат

    connection.close()

    return count


def find_duplicates():
    connection = sqlite3.connect("data/app.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT file_hash      
        FROM files
        GROUP BY file_hash
        HAVING COUNT(*) > 1
    """)

    duplicate_hashes = cursor.fetchall()

    result = []

    for duplicate_hash in duplicate_hashes:
        cursor.execute("""
            SELECT relative_path
            FROM files
            WHERE file_hash = ?
        """, (duplicate_hash[0],))

        files = cursor.fetchall()

        result.append({
            "hash": duplicate_hash[0],
            "files": files
        })

    connection.close()

    return result


def save_backup_check(
    source_count,
    backup_count,
    missing_count,
    extra_count,
    changed_count
):
    connection = sqlite3.connect("data/app.db")
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO backup_checks (
            check_time,
            source_count,
            backup_count,
            missing_count,
            extra_count,
            changed_count
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        source_count,
        backup_count,
        missing_count,
        extra_count,
        changed_count
    ))

    connection.commit()
    connection.close()

def get_backup_checks_count():
    connection = sqlite3.connect("data/app.db")

    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM backup_checks
    """)

    count = cursor.fetchone()[0]

    connection.close()

    return count