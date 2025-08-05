from pydantic import BaseModel, HttpUrl
from typing import List

class AuthorOut(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class DifficultyOut(BaseModel):
    id: int
    difficulty: str

    class Config:
        orm_mode = True

class CourseOut(BaseModel):
    id: int
    name: str
    url: str
    duration: float
    total_lectures: int
    rating: float
    total_students: int
    current_price: float
    original_price: float
    difficulty: DifficultyOut
    authors: List[AuthorOut]

    class Config:
        orm_mode = True
