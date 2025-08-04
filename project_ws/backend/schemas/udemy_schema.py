from pydantic import BaseModel, HttpUrl, Field
from typing import List


class CourseInput(BaseModel):
    title: str
    target_url: HttpUrl
    author: List[str]
    rating: str
    total_students:str
    current_price: str
    original_price: str
    hours_required: str
    lectures_count: str
    difficulty: str

class CoursesInput(BaseModel):
    courses: List[CourseInput]