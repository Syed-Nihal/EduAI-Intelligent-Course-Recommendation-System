from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
import joblib
import os
import numpy as np

from app.database import get_db
from app import models, schemas

# Router
router = APIRouter(prefix="/students", tags=["Students"])

# ============================
# CRUD ENDPOINTS
# ============================

@router.post("/")
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    db_student = models.Student(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return {"message": "Student created successfully"}


@router.get("/")
def get_all_students(db: Session = Depends(get_db)):
    students = db.query(models.Student).all()
    return students


@router.get("/{student_id}")
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


# ============================
# REAL-TIME ML PREDICTION
# ============================

MODEL_PATH = "app/ml/student_model.pkl"


class PredictionInput(BaseModel):
    age: int
    attendance: float
    marks: float
    interest_level: int


@router.post("/predict")
def predict_course(data: PredictionInput):

    if not os.path.exists(MODEL_PATH):
        raise HTTPException(status_code=400, detail="Model not trained yet")

    model = joblib.load(MODEL_PATH)

    features = np.array([[data.age, data.attendance, data.marks, data.interest_level]])

    prediction = model.predict(features)[0]
    probabilities = model.predict_proba(features)[0]
    confidence = round(max(probabilities) * 100, 2)

    return {
        "predicted_course": prediction,
        "confidence_percentage": confidence
    }