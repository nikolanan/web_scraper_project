from db.db_config import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, CheckConstraint
from sqlalchemy.sql import func

class Courses(Base):
    __tablename__ = "courses"

    id = Column(Integer,primary_key=True,index=True)
    name = Column(String)
    url = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    duration = Column(Integer)
    total_lectures = Column(Integer)
    rating = Column(Float)
    total_students = Column(Integer)
    difficulty_id = Column(Integer,ForeignKey("course_difficulties.id"))

    __table_args__ = (
        CheckConstraint('rating >= 1.0 AND rating <= 5.0', name='rating_range_check'),
        CheckConstraint('duration > 0', name='duration_check'),
        CheckConstraint('total_students > 0', name='students_number_check'),
        CheckConstraint(
            "url ~* '^https?://'",  # PostgreSQL regex to check http or https
            name="valid_url_check"
        ),
    )

class Course_difficulties(Base):
    __tablename__ = "course_difficulties"

    id = Column(Integer,primary_key=True,index=True)
    difficulty = Column(String)
