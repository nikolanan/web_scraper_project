from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.db_config import SessionLocal
from utils.web_scraper_scripts.info_courses import retrieve_courses_info
from utils.web_scraper_scripts.multiple_courses import retrive_mulitiple_courses
from typing import Annotated
from starlette import status
from typing import List
from schemas.udemy_schema import CourseInput, CoursesInput
from models.authors import Authors, Authors_Courses
from models.courses import Courses, Course_difficulties
from sqlalchemy.orm import joinedload
from typing import List
from schemas.retrieval_schema import CourseOut

router = APIRouter(
    prefix="/get_data",
    tags=["get_data"]
)

def get_db():
    """
    Makes a local database session available for the duration of a request.
    Yield is used to ensure that the session is closed after use.
    If return was used instead of yield,
    the session would not be closed properly.

    :yield: Session
    :rtype: Session
    """

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependancy = Annotated[Session,Depends(get_db)]

@router.get("/get_all_courses_db", response_model=List[CourseOut])
async def get_all_courses(db: db_dependancy):
    courses = db.query(Courses).options(
        joinedload(Courses.difficulty),
        joinedload(Courses.authors)
    ).all()
    return courses


@router.get("/get_all_course_by_id/{course_id}", response_model=List[CourseOut])
async def get_course_by_id(db: db_dependancy, course_id: int):
    courses = db.query(Courses).filter(Courses.id == course_id).options(
        joinedload(Courses.difficulty),
        joinedload(Courses.authors)
    ).all()
    return courses
