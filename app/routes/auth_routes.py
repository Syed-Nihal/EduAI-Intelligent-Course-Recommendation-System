from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
import sqlite3

from app.utils import hash_password, verify_password
from app.jwt_handler import create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])


# ==============================
# 📦 SCHEMA
# ==============================
class UserSignup(BaseModel):
    username: str
    email: str
    password: str


# ==============================
# 📝 SIGNUP
# ==============================
@router.post("/signup")
def signup(user: UserSignup):
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    hashed_pwd = hash_password(user.password)

    try:
        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            (user.username, user.email, hashed_pwd)
        )
        conn.commit()

        return {"message": "User created successfully"}

    except Exception as e:
        return {"error": str(e)}

    finally:
        conn.close()


# ==============================
# 🔐 LOGIN (OAUTH2 FIXED)
# ==============================
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username = ?",
        (form_data.username,)
    )
    user = cursor.fetchone()

    conn.close()

    if not user:
        return {"error": "User not found"}

    # user[3] = password column
    if not verify_password(form_data.password, user[3]):
        return {"error": "Invalid password"}

    token = create_access_token({"sub": user[1]})

    return {
        "access_token": token,
        "token_type": "bearer"
    }