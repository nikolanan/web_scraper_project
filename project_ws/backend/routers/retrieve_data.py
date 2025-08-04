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

router = APIRouter(
    prefix="/retrieve_data",
    tags=["retrieve_data"]
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

@router.get("/load_coarses")
async def load_coarses():
    """
    Endpoint to retrieve course information.
    Calls the `retrieve_courses_info` function to scrape data from Udemy.
    """
    try:
        URL = "https://www.udemy.com/courses/it-and-software/other-it-and-software/?p=1&sort=most-reviewed"
        courses_info = retrieve_courses_info(URL)
        return {"courses": courses_info}
    except Exception as e:
        return {"error": str(e)}

@router.get("/load_courses_page_number/{page_number}")
async def load_pages_by_pn(page_number: int):
    try:
        return retrive_mulitiple_courses(page_number)
    except Exception as e:
        return {"error": str(e)}

@router.post("/insert_courses/{page_number}")
async def insert_courses(db:db_dependancy,page_number:int):
    try:
        all_courses = retrive_mulitiple_courses(page_number)
        all_courses_validated = [CourseInput(**course) for course in all_courses]

        for course in all_courses_validated:
            try:
                difficulty = get_or_create_difficulty(db,course.difficulty)
                authors = get_or_create_author(db,course.author)
            except Exception as e:
                return {"error":"transaction failed"}
        
    except Exception as e:
        return {"error": str(e)}
    
def get_or_create_difficulty(db:db_dependancy, difficulty_str:str) -> Course_difficulties:
    """
    If the difficulty is not in
    the database it creates it and
    returns it.

    :param db: The db dependancy
    :type db: db_dependancy
    :param difficulty_str: The difficulty extracted from the web scraping
    :type difficulty_str: str
    :return: A model object 
    :rtype: Course_difficulties
    """

    difficulty = db.query(Course_difficulties).filter(Course_difficulties.difficulty == difficulty_str).first()
    if not difficulty:
        difficulty = Course_difficulties(difficulty=difficulty_str)
        db.add(difficulty)
        db.commit()
        db.refresh(difficulty)
    return difficulty
    
def get_or_create_author(db:db_dependancy, author_names:list):
    all_authors = []
    for author in author_names:
        author = db.query(Authors).filter(Authors.name == author).first()
        if not author:
            author = Authors(name=author)
            db.add(author)
            db.commit()
            db.refresh(author)
        all_authors.append(author)
    return all_authors

def link_author_to_course(db:db_dependancy,author_id:int,course_id:int):
    link = db.query(Authors_Courses).filter(Authors_Courses.author_id == author_id, Authors_Courses.course_id == course_id).first()
    if not link:
        db.add(link)
        db.commit()

def create_course(db:db_dependancy, course_input:CourseInput,difficulty_id:int):
    course = Courses(
        name=course_input.title,
        url=course_input.target_url,
        duration=course_input.hours_required,
        total_lectures=course_input.lectures_count,
        rating=course_input.rating,
        total_students=course_input.total_students,
        difficulty_id=difficulty_id
    )

    db.add(course)
    db.commit()
    db.refresh(course)

    return course