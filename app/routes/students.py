from fastapi import APIRouter
import sqlite3

router = APIRouter(prefix="/students", tags=["Students"])


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