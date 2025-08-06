from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional


class CourseInput(BaseModel):
    """
    Represents the input data for a single course scraped from the web.

    This schema is used to validate and serialize course data received from web scraping operations
    before it is processed or stored. It includes fields for the course title, URL, author(s), rating,
    student count, pricing, duration, lecture count, and difficulty.
    """
    title: str
    target_url: HttpUrl
    author: List[str]
    rating: str
    total_students:str
    current_price: Optional[str] = None
    original_price: Optional[str] = None
    hours_required: str
    lectures_count: Optional[str] = None
    difficulty: str

class CoursesInput(BaseModel):
    """
    Represents a collection of courses scraped from the web.

    This schema is used to validate and serialize a batch of course data received from web scraping,
    typically for bulk processing or storage. It contains a list of CourseInput objects.
    """

    courses: List[CourseInput]