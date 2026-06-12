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
            extension TEXT
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
                extension
            )
            VALUES (?, ?, ?, ?)
        """, (
            file["relative_path"],
            file["size"],
            file["modified_time"],
            file["extension"]
        ))

def get_files_count():
    connection = sqlite3.connect("data/app.db")

    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM files")

    count = cursor.fetchone()[0]

    connection.close()

    return count

    connection.commit()
    connection.close()