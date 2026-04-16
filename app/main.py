from fastapi import FastAPI

# database
from app.database import create_tables

# routers
from app.routes.students import router as student_router
from app.routes.auth_routes import router as auth_router

app = FastAPI(
    title="EduAI - Student Intelligent Course Recommendation System"
)

# ==============================
# 🚀 STARTUP EVENT
# ==============================
@app.on_event("startup")
def startup_event():
    print("🚀 Creating database tables...")
    create_tables()

# ==============================
# ROUTES
# ==============================
app.include_router(student_router)
app.include_router(auth_router)

# ==============================
# HOME (FIXED)
# ==============================
@app.get("/")
def root():
    return {
        "message": "EduAI API is running 🚀",
        "docs": "/docs"
    }

# ==============================
# HEALTH CHECK
# ==============================
@app.get("/health")
def health_check():
    return {"status": "OK"}