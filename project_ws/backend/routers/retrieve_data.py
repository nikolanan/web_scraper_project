from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.db_config import SessionLocal
from utils.web_scraper_scripts.info_courses import retrieve_courses_info
from utils.web_scraper_scripts.multiple_courses import retrive_mulitiple_courses
from utils.web_scraper_scripts.pl_multiple_courses import retrive_mulitiple_courses_pl
from typing import Annotated
from starlette import status
from typing import List
from schemas.web_retrieval_schema import CourseInput, CoursesInput
from models.authors import Authors, Authors_Courses
from models.courses import Courses, Course_difficulties

router = APIRouter(
    prefix="/save_data",
    tags=["Scrape data"]
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

db_dependancy = Annotated[Session, Depends(get_db)]

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
    
@router.get("/load_courses_page_number_pl/{page_number}")
async def pl_load_pages_by_pn(page_number: int):
    try:
        return retrive_mulitiple_courses_pl(page_number)
    except Exception as e:
        return {"error": str(e)}

@router.post("/insert_courses/{page_number}")
async def insert_courses(db: db_dependancy,page_number: int):
    try:
        all_courses = retrive_mulitiple_courses(page_number)
        all_courses_validated = [CourseInput(**course) for course in all_courses]

        courses_counter = 0
        for course in all_courses_validated:
            try:
                courses_counter+=1
                difficulty = get_or_create_difficulty(db, course.difficulty)
                created_course = create_course(db, course, difficulty.id)
                authors = get_or_create_author(db, course.author)
                for author in authors:
                    link_author_to_course(db, author.id, created_course.id)                
            except Exception as e:
                return {"error":"transaction failed"}
        return {"Success":courses_counter}
    except Exception as e:
        return {"error": str(e)}

def get_or_create_difficulty(db: db_dependancy, difficulty_str: str) -> Course_difficulties:
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

def get_or_create_author(db: db_dependancy, author_names: list) -> list[Authors]:
    """
    Return a list of the author objects.
    If an author doesnt exits in the database
    it creates it

    :param db: The db dependancy
    :type db: db_dependancy
    :param author_names: Authors extracted from the webscraping
    :type author_names: list
    :return: a list of authors object
    :rtype: list[Authors]
    """
    all_authors = []
    for author in author_names:
        cleaned = author.strip()
        author_obj = db.query(Authors).filter(Authors.name == cleaned).first()
        if not author_obj:
            author_obj = Authors(name=cleaned)
            db.add(author_obj)
            db.commit()
            db.refresh(author_obj)
        all_authors.append(author_obj)
    return all_authors

def link_author_to_course(db: db_dependancy, author_id: int, course_id: int):
    """
    Creates a link between author and course
    if it doenst exist

    :param db: The db dependancy
    :type db: db_dependancy
    :param author_id: The id of the author from the object
    :type author_id: int
    :param course_id: The id of the course fro the object
    :type course_id: int
    """
    link = db.query(Authors_Courses).filter(Authors_Courses.author_id == author_id, Authors_Courses.course_id == course_id).first()
    if not link:
        link = Authors_Courses(author_id=author_id, course_id=course_id)
        db.add(link)
        db.commit()

def create_course(db: db_dependancy, course_input: CourseInput, difficulty_id: int) -> Courses:
    """
    Creates a course

    :param db: The db depandancy
    :type db: db_dependancy
    :param course_input: The course object that has validated the data from the json
    :type course_input: CourseInput
    :param difficulty_id: The id of the difficulty (since it is a foreign key)
    :type difficulty_id: int
    :return: A model of type Courses
    :rtype: Courses
    """

    def parse_price(price_str: str) -> float:
        return float(price_str.replace("€", "").replace(",", "").strip())

    def parse_students(students_str: str) -> int:
        return int(students_str.replace(",", "").strip())

    course = Courses(
        name=course_input.title,
        url=str(course_input.target_url),
        duration=float(course_input.hours_required),
        total_lectures=int(course_input.lectures_count),
        rating=float(course_input.rating),
        total_students=parse_students(course_input.total_students),
        current_price=parse_price(course_input.current_price),
        original_price=parse_price(course_input.original_price),
        difficulty_id=difficulty_id
    )

    db.add(course)
    db.commit()
    db.refresh(course)

    return course