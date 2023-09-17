from uuid import UUID
from pydantic import BaseModel

class Student(BaseModel):
    name: str
    email: str
    course: str
    period: int
    age: int

class CreateStudent(BaseModel):
    id: UUID
    name: str
    email: str
    course: str
    period: int
    age: int