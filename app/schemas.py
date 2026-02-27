from pydantic import BaseModel


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