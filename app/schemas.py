from pydantic import BaseModel, EmailStr

# signup
class UserSignup(BaseModel):
    username: str
    email: EmailStr
    password: str

# login
class UserLogin(BaseModel):
    username: str
    password: str

# token response
class Token(BaseModel):
    access_token: str
    token_type: str