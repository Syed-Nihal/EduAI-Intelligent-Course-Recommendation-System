from fastapi import HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.ml.model import predict_recommendation


# ==============================
# CREATE STUDENT
# ==============================
def create_student(db: Session, student: schemas.StudentCreate):
    existing_student = db.query(models.Student).filter(
        models.Student.email == student.email
    ).first()

    if existing_student:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_student = models.Student(
        name=student.name,
        email=student.email,
        age=student.age,
        course=student.course
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student


# ==============================
# GET ALL STUDENTS
# ==============================
def get_all_students(
    db: Session,
    search: str = None,
    course: str = None,
    page: int = 1,
    limit: int = 5
):
    query = db.query(models.Student)

    if search:
        query = query.filter(models.Student.name.ilike(f"%{search}%"))

    if course:
        query = query.filter(models.Student.course.ilike(f"%{course}%"))

    offset = (page - 1) * limit
    students = query.offset(offset).limit(limit).all()

    return students


# ==============================
# GET STUDENT BY ID
# ==============================
def get_student_by_id(db: Session, student_id: int):
    student = db.query(models.Student).filter(
        models.Student.id == student_id
    ).first()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    return student


# ==============================
# UPDATE STUDENT
# ==============================
def update_student(db: Session, student_id: int, student: schemas.StudentCreate):
    db_student = db.query(models.Student).filter(
        models.Student.id == student_id
    ).first()

    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")

    existing_email = db.query(models.Student).filter(
        models.Student.email == student.email,
        models.Student.id != student_id
    ).first()

    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    db_student.name = student.name
    db_student.email = student.email
    db_student.age = student.age
    db_student.course = student.course

    db.commit()
    db.refresh(db_student)

    return db_student


# ==============================
# DELETE STUDENT
# ==============================
def delete_student(db: Session, student_id: int):
    db_student = db.query(models.Student).filter(
        models.Student.id == student_id
    ).first()

    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")

    db.delete(db_student)
    db.commit()

    return {"message": "Student deleted successfully"}


# ==============================
# 🤖 ML RECOMMENDATION
# ==============================
def recommend_courses(db: Session, student_id: int):
    student = db.query(models.Student).filter(
        models.Student.id == student_id
    ).first()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    # Call ML model
    recommended_course = predict_recommendation(
        age=student.age,
        current_course=student.course
    )

    return {
        "student_name": student.name,
        "current_course": student.course,
        "ml_recommended_course": recommended_course
    }