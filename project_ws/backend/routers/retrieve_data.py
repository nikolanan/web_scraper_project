from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.db_config import SessionLocal
from utils.web_scraper_scripts.info_courses import retrieve_courses_info

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

@router.get("/load_coarses")
async def load_coarses():
    """
    Endpoint to retrieve course information.
    Calls the `retrieve_courses_info` function to scrape data from Udemy.
    """
    try:
        courses_info = retrieve_courses_info()
        return {"courses": courses_info}
    except Exception as e:
        return {"error": str(e)}