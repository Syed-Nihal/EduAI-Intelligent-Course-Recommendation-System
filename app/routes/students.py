from fastapi import APIRouter
import sqlite3

router = APIRouter(prefix="/students", tags=["Students"])


# ==============================
# 📊 Get All Students (SAFE)
# ==============================
@router.get("/all")
def get_all_students():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()

    conn.close()

    students = []
    for row in rows:
        students.append({
            "data": row
        })

    return {
        "total_students": len(students),
        "students": students
    }