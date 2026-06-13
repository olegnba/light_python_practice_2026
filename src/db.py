import sqlite3


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

    connection.commit()
    connection.close()


def save_files(files_data):
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

    cursor.execute("SELECT COUNT(*) FROM files")

    count = cursor.fetchone()[0]

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