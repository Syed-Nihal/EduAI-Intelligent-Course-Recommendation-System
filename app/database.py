import sqlite3

# ==============================
# 📦 CREATE DATABASE TABLES
# ==============================
def create_tables():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    print("📦 Creating tables...")

    # ==============================
    # ❌ DROP OLD TABLES (IMPORTANT FIX)
    # ==============================
    cursor.execute("DROP TABLE IF EXISTS users")
    cursor.execute("DROP TABLE IF EXISTS students")

    # ==============================
    # 🎓 STUDENTS TABLE
    # ==============================
    cursor.execute("""
    CREATE TABLE students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        age INTEGER,
        attendance REAL,
        marks REAL,
        interest_level INTEGER
    )
    """)

    # ==============================
    # 👤 USERS TABLE (FIXED)
    # ==============================
    cursor.execute("""
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()

    print("✅ Tables recreated successfully!")