from pydantic import BaseModel, HttpUrl
from typing import List

class AuthorOut(BaseModel):
    """
    Represents an author of a course.

    This schema is used to serialize and validate author data when retrieving course information
    from the database or serving it via API responses. It ensures that each author has an ID and a name.
    """

    id: int
    name: str

    class Config:
        """
        Enables ORM mode for compatibility with ORM objects.
        """
        orm_mode = True

class DifficultyOut(BaseModel):
    """
    Represents the difficulty level of a course.

    This schema is used to serialize and validate the difficulty information associated with a course.
    It is typically included as a nested object in course responses to indicate the course's level.
    """

    id: int
    difficulty: str

    class Config:
        """
        Enables ORM mode for compatibility with ORM objects.
        """
        orm_mode = True

class CourseOut(BaseModel):
    """
    Represents a course with detailed information.

    This schema is used to serialize and validate all relevant data about a course when retrieving
    from the database or serving via API responses. It includes fields for course metadata, pricing,
    difficulty, and associated authors. Used as the main output model for course-related endpoints.
    """

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
        """
        Enables ORM mode for compatibility with ORM objects.
        """
        orm_mode = True
