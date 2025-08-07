from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session
from db.db_config import SessionLocal
from utils.web_scraper_scripts.multiple_pages_scraper import retrive_mulitiple_courses
from typing import Annotated
from starlette import status
from typing import List
from schemas.web_retrieval_schema import CourseInput, CoursesInput
from models.authors import Authors, Authors_Courses
from models.courses import Courses, Course_difficulties
from utils.logger import logger_setup
import logging

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

@router.post("/insert_courses/{start_page}/{end_page}", status_code=status.HTTP_201_CREATED)
async def insert_courses(db: db_dependancy, 
                        web_platform:str = Query(description="Type udemy or pluralsight"),
                        start_page: int = Path(gt=0),
                        end_page: int = Path(gt=0)):
    """
    Inserts a batch of courses from an external web scraping source into the database.

    This endpoint fetches a specific page of course data, validates it, and then
    processes each course to ensure its associated difficulty and authors exist
    or are created before inserting the new course.

    ### Udemy's url scraped from:
    **https://www.udemy.com/courses/it-and-software/other-it-and-software/?p=1&sort=most-reviewed**
    
    ### Pluralsight's url scraped from:
    **https://www.pluralsight.com/browse?=&sort=newest&course-category=Software%20Development&page={1}&ratings=3.0%20and%20up&categories=course**
    
    - **db**: The database dependency.
    - **web_platform** either udemy or pluralsight
    - **start_page**: that starts the webscraping starts from
    - **end_page**: that is the last page the is webscraped (including)

    ### Returns

    A JSON object indicating success and the number of courses successfully processed as well as
    the inserted courses

    ### Raises

    - **HTTPException(404, "Not Found")**: If the external scraping process returns no courses for the given pages or platform.
    - **HTTPException(500, "Internal Server Error")**: If any error occurs during the processing of individual courses or a database operation.
    """
    try:
        if start_page > end_page:
            return {"Error":"starting page cannot be bigger tha ending page"}
        all_courses = retrive_mulitiple_courses(web_platform, start_page, end_page)

        logging.info(f"Retrieved coureses: {all_courses}")

        if not all_courses:
            raise HTTPException(status_code=404, detail="No courses retrieved from scraping")

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
                db.commit()
            except Exception:
                db.rollback()
                logging.info("Transaction cancelled")
                logging.error(f"Error processing course in: {course.target_url}")
                raise HTTPException(status_code=500, detail="Error while processing data")

        return {
                "Success":courses_counter,
                "Inserted_courses": all_courses_validated
        }

    except HTTPException:
        raise HTTPException(status_code=500, detail="Error on the incoming data")

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
        db.flush()

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
            db.flush()

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
        db.flush()

    return link

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
    def safe_cast_int(value):
        return int(value) if value is not None else None

    def safe_cast_float(value):
        return float(value) if value is not None else None

    def parse_price(price_str: str) -> float:
        if price_str is None:
            return None
        return float(price_str.replace("€", "").replace(",", "").strip())

    def parse_students(students: str | int) -> int:
        if isinstance(students, int):
            return students
        return int(students.replace(",", "").strip())

    course = Courses(
        name=course_input.title,
        url=str(course_input.target_url),
        duration=float(course_input.hours_required),
        total_lectures=safe_cast_int(course_input.lectures_count),
        rating=float(course_input.rating),
        total_students=parse_students(course_input.total_students),
        current_price=parse_price(course_input.current_price),
        original_price=parse_price(course_input.original_price),
        difficulty_id=difficulty_id
    )

    db.add(course)
    db.flush()

    return course