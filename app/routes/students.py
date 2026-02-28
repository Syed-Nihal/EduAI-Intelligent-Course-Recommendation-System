from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import joblib
import os
import numpy as np

router = APIRouter(prefix="/students", tags=["Students"])

# =========================
# Load ML Model
# =========================

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "ml", "student_model.pkl")
MODEL_PATH = os.path.abspath(MODEL_PATH)

if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)
else:
    model = None


# =========================
# Request Schema
# =========================

class PredictionRequest(BaseModel):
    age: int
    attendance: float
    marks: float


# =========================
# Prediction Route
# =========================

@router.post("/predict")
def predict_course(data: PredictionRequest):
    if model is None:
        raise HTTPException(status_code=500, detail="ML model not loaded")

    try:
        features = np.array([[data.age, data.attendance, data.marks]])
        prediction = model.predict(features)
        probabilities = model.predict_proba(features)

        predicted_course = prediction[0]
        confidence = round(float(np.max(probabilities)) * 100, 2)

        return {
            "predicted_course": predicted_course,
            "confidence": confidence
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))