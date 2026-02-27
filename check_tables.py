import sqlite3

# Connect to your database file
conn = sqlite3.connect("students.db")
cursor = conn.cursor()

# Ask SQLite to show structure of students table
cursor.execute("PRAGMA table_info(students)")

columns = cursor.fetchall()

print("\nColumns in students table:\n")

for column in columns:
    print(column)

conn.close()