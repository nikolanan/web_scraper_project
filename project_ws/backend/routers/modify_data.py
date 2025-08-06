from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from db.db_config import SessionLocal
from typing import Annotated
from starlette import status
from schemas.web_retrieval_schema import CourseInput, CoursesInput
from models.authors import Authors, Authors_Courses
from models.courses import Courses, Course_difficulties

router = APIRouter(
    prefix="/modify_date",
    tags=["Modify data"]
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

@router.delete("/delete_course/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(db: db_dependancy, course_id: int = Path(gt=0)):
    """
    Deletes a course with the given ID.

    - **db**: The database dependency.
    
    ### Raises

    - **HTTPException(404, "Not Found")**: If no courses are found that match the provided criteria.
    """

    course_to_delete = db.query(Courses).filter(Courses.id == course_id).first()

    if course_to_delete is None:
        raise HTTPException(status_code=404, detail="Course not found.")

    db.delete(course_to_delete)
    db.commit()
