from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session
from db.db_config import SessionLocal
from typing import Annotated, Optional
from starlette import status
from typing import List
from models.authors import Authors, Authors_Courses
from models.courses import Courses, Course_difficulties
from sqlalchemy.orm import joinedload
from typing import List
from schemas.db_retrieval_schema import CourseOut, DifficultyOut, AuthorOut

router = APIRouter(
    prefix="/get_data",
    tags=["Retrieve data"]
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

##The depandancy injection
db_dependancy = Annotated[Session,Depends(get_db)]

@router.get("/get_all_courses_from_db",
            response_model=List[CourseOut],
            status_code=status.HTTP_200_OK)
async def get_all_courses(db: db_dependancy):
    """
    Returns all courses in the database.

    - **db**: The database dependency.

    ### Returns

    A list of `CourseOut` objects.


    """
    courses = db.query(Courses).options(
        joinedload(Courses.difficulty),
        joinedload(Courses.authors)
    ).all()
    if courses:
        return courses
    raise HTTPException(status_code=404, detail="No courses found.")

##Unified filters if separate it would lead to complexxity explosion
@router.get("/get_filtered_courses",
            response_model=List[CourseOut],
            status_code=status.HTTP_200_OK)
async def get_courses(
    db: db_dependancy,
    id: Optional[int] = Query(None, gt=0, description="Filter by course ID."),
    keyword: Optional[str] = Query(None, description="Search for a keyword in the course name (case-insensitive)."),
    min_price: Optional[float] = Query(None, gt=0, description="Search for courses with a price greater than or equal to this value."),
    max_price: Optional[float] = Query(None, le=1000, description="Search for courses with a price less than or equal to this value."),
    rating: Optional[float] = Query(None, gt=0, le=5, description="Search for a course rating above the given value."),
    difficulty: Optional[str] = Query(None, description="Filter by difficulty level."),
    author_name: Optional[str] = Query(None, description="Filter by author name.")
):
    """
    Returns a list of courses based on various optional filters.

    
    - **id**: Filter by a specific course ID.
    - **keyword**: Search for a keyword in the course name (case-insensitive).
    - **min_price**: 0.
    - **max_price**: 1000.
    - **rating**: Course rating from 0 to 5.
    - **difficulty**: Filter by the difficulty level (e.g., 'Beginner').
    - **author_name**: Filter by the name of an author.

    ### Returns

    A list of `CourseOut` objects.

    ### Raises

    - **HTTPException(404, "Not Found")**: If no courses are found that match the provided criteria.
    """

    # not a db call!!! - it is without all
    query = db.query(Courses).options(
        joinedload(Courses.difficulty),
        joinedload(Courses.authors)
    )

    if id:
        query = query.filter(Courses.id == id)

    if keyword:
        search_term = f"%{keyword}%"
        query = query.filter(Courses.name.ilike(search_term))

    if min_price and max_price:
        if min_price > max_price:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Minimum price cannot be greater than maximum price."
            )
        query = query.filter((Courses.current_price <= max_price) & (Courses.current_price >= min_price))

    if min_price and not max_price:
        query = query.filter(Courses.current_price >= min_price)

    if max_price and not min_price:
        query = query.filter(Courses.current_price <= max_price)

    if rating:
        query = query.filter(Courses.rating >= rating)

    if difficulty:
        search_difficulty_term = f"%{difficulty}%"
        query = query.join(Course_difficulties).filter(Course_difficulties.difficulty.ilike(search_difficulty_term))

    if author_name:
        search_author_term = f"%{author_name}%"
        query = query.join(Courses.authors).filter(Authors.name.ilike(search_author_term))

    courses = query.all()

    if not courses:
        raise HTTPException(status_code=404, detail="No courses found matching the criteria.")

    return courses

@router.get("/get_all_difficulty_types",
             response_model=List[DifficultyOut],
             status_code=status.HTTP_200_OK)
async def get_all_difficulty_types(db: db_dependancy):
    """
    Returns a course with the given id.

    - **db**: The database dependency.
    - **course_id**: The ID of the course to retrieve.

    ### Returns

    The found course with all its related data.

    ### Raises

    - **HTTPException(404, "Not Found")**: If a course with the given ID is not found.
    """

    difficulties = db.query(Course_difficulties).all()

    if difficulties:
        return difficulties
    raise HTTPException(status_code=404,detail="No difficulty items were found")

@router.get("/get_all_authors",
            response_model=List[AuthorOut],
            status_code=status.HTTP_200_OK)
async def get_all_authors(db: db_dependancy):
    """
    Returns a list of all authors.

    - **db**: The database dependency.

    ### Returns

    A list of `AuthorOut` objects.

    ### Raises

    - **HTTPException(404, "Not Found")**: If no authors are found in the database.
    """

    authors = db.query(Authors).all()

    if authors:
        return authors
    raise HTTPException(status_code=404, detail="No authors were found")