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