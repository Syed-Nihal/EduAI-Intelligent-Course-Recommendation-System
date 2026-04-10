from fastapi import APIRouter
from pydantic import BaseModel
import sqlite3

router = APIRouter(prefix="/students", tags=["Students"])


# ==============================
# 📦 Request Schema (IMPORTANT)
# ==============================
class Student(BaseModel):
    age: int
    attendance: float
    marks: float
    interest_level: int


# ==============================
# 📊 Get All Students
# ==============================
@router.get("/all")
def get_all_students():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM students")
        rows = cursor.fetchall()

        students = []
        for row in rows:
            students.append({
                "id": row[0],
                "age": row[1],
                "attendance": row[2],
                "marks": row[3],
                "interest_level": row[4]
            })

        return {
            "total_students": len(students),
            "students": students
        }

    except Exception as e:
        return {"error": str(e)}

    finally:
        conn.close()


# ==============================
# ➕ Add Student (FIXED)
# ==============================
@router.post("/add")
def add_student(student: Student):
    try:
        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO students (age, attendance, marks, interest_level)
            VALUES (?, ?, ?, ?)
        """, (student.age, student.attendance, student.marks, student.interest_level))

        conn.commit()
        conn.close()

        return {"message": "Student added successfully ✅"}

    except Exception as e:
        return {"error": str(e)}