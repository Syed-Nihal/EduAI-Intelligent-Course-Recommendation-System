from pydantic import BaseModel


# ==============================
# Student Create & Response
# ==============================

class StudentBase(BaseModel):
    name: str
    email: str
    age: int
    course: str


class StudentCreate(StudentBase):
    pass


class StudentResponse(StudentBase):
    id: int

    class Config:
        from_attributes = True


# ==============================
# Prediction Schema
# ==============================

class StudentPredict(BaseModel):
    age: int
    attendance: float
    marks: float


class PredictionResponse(BaseModel):
    predicted_course: str
    confidence_percentage: float