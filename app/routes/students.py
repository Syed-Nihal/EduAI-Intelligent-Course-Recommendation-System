from fastapi import APIRouter, Depends
from pydantic import BaseModel
import sqlite3

# 🔐 AUTH
from app.oauth2 import oauth2_scheme

# 🤖 AI MODEL
from app.ml_model import train_model, predict_course

router = APIRouter(prefix="/students", tags=["Students"])


# ==============================
# 📦 Request Schema
# ==============================
class Student(BaseModel):
    age: int
    attendance: float
    marks: float
    interest_level: int


# ==============================
# 🤖 LOAD ML MODEL
# ==============================
model = train_model()


# ==============================
# 📊 Get All Students (PROTECTED)
# ==============================
@router.get("/all")
def get_all_students(token: str = Depends(oauth2_scheme)):
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
# ➕ Add Student (PROTECTED)
# ==============================
@router.post("/add")
def add_student(
    student: Student,
    token: str = Depends(oauth2_scheme)
):
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


# ==============================
# 🤖 RECOMMEND COURSE (AI + EXPLANATION)
# ==============================
@router.post("/recommend")
def recommend_course(
    student: Student,
    token: str = Depends(oauth2_scheme)
):
    try:
        student_data = {
            "age": student.age,
            "attendance": student.attendance,
            "marks": student.marks,
            "interest_level": student.interest_level
        }

        prediction = predict_course(model, student_data)

        # 🎯 Explainable AI logic
        reason = ""
        confidence = "Medium"

        if student.marks > 85 and student.interest_level >= 4:
            reason = "High marks and strong interest level"
            confidence = "High"

        elif student.marks > 75:
            reason = "Good academic performance"
            confidence = "Medium"

        elif student.interest_level >= 3:
            reason = "Moderate interest level"
            confidence = "Medium"

        else:
            reason = "Needs improvement in academics"
            confidence = "Low"

        return {
            "recommended_course": prediction,
            "reason": reason,
            "confidence": confidence
        }

    except Exception as e:
        return {"error": str(e)}