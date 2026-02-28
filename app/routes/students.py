from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import joblib
import os
import numpy as np

router = APIRouter(prefix="/students", tags=["Students"])

# =========================
# Load ML Model
# =========================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "ml", "student_model.pkl")

if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)
    print("✅ ML Model Loaded Successfully")
else:
    model = None
    print("❌ ML Model Not Found")


# =========================
# Request Schema (4 FEATURES)
# =========================

class PredictionRequest(BaseModel):
    age: int
    attendance: float
    marks: float
    interest_level: float


# =========================
# Prediction Endpoint
# =========================

@router.post("/predict")
def predict_course(data: PredictionRequest):

    if model is None:
        raise HTTPException(status_code=500, detail="ML model not loaded")

    try:
        # Model expects 4 features
        features = np.array([[
            data.age,
            data.attendance,
            data.marks,
            data.interest_level
        ]])

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