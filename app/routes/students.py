from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
import joblib
import os
import numpy as np

router = APIRouter(prefix="/students", tags=["Students"])


# ==============================
# Load ML Model
# ==============================

MODEL_PATH = "app/ml/student_model.pkl"

if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)
else:
    model = None


# ==============================
# CREATE STUDENT
# ==============================

@router.post("/", response_model=schemas.StudentResponse)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    db_student = models.Student(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


# ==============================
# GET ALL STUDENTS
# ==============================

@router.get("/", response_model=list[schemas.StudentResponse])
def get_students(db: Session = Depends(get_db)):
    return db.query(models.Student).all()


# ==============================
# GET SINGLE STUDENT
# ==============================

@router.get("/{student_id}", response_model=schemas.StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


# ==============================
# PREDICT COURSE
# ==============================

@router.post("/predict", response_model=schemas.PredictionResponse)
def predict_course(data: schemas.StudentPredict):

    if model is None:
        raise HTTPException(status_code=500, detail="ML model not loaded")

    # Prepare input for model
    features = np.array([[data.age, data.attendance, data.marks]])

    prediction = model.predict(features)[0]

    # Optional: confidence (if using RandomForest)
    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(features)
        confidence = float(np.max(probabilities) * 100)
    else:
        confidence = 100.0

    return {
        "predicted_course": prediction,
        "confidence_percentage": round(confidence, 2)
    }