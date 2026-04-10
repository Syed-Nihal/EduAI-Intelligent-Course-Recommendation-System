import sqlite3

def create_tables():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        age INTEGER,
        attendance REAL,
        marks REAL,
        interest_level INTEGER
    )
    """)

    conn.commit()
    conn.close()