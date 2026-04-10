import sqlite3
from fastapi import APIRouter

router = APIRouter(prefix="/students", tags=["Students"])


# ==============================
# 📊 Get All Students
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
            "id": row[0],
            "name": row[1],
            "email": row[2],
            "age": row[3],
            "course": row[4]
        })

    return {"students": students}