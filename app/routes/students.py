from fastapi import Request


# ==============================
# ➕ Add Student
# ==============================
@router.post("/add")
async def add_student(request: Request):
    data = await request.json()

    age = data.get("age")
    attendance = data.get("attendance")
    marks = data.get("marks")
    interest_level = data.get("interest_level")

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO students (age, attendance, marks, interest_level)
        VALUES (?, ?, ?, ?)
    """, (age, attendance, marks, interest_level))

    conn.commit()
    conn.close()

    return {"message": "Student added successfully ✅"}