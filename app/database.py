import sqlite3


# ==============================
# 📦 CREATE DATABASE TABLES
# ==============================
def create_tables():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    print("📦 Creating tables...")

    # ==============================
    # 🎓 STUDENTS TABLE
    # ==============================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        age INTEGER,
        attendance REAL,
        marks REAL,
        interest_level INTEGER
    )
    """)

    # ==============================
    # 👤 USERS TABLE
    # ==============================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        email TEXT,
        password TEXT
    )
    """)

    conn.commit()
    conn.close()

    print("✅ Tables created successfully!")