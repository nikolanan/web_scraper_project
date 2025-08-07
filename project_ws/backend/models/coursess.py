from db.db_config import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, CheckConstraint, Numeric
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class Courses(Base):
    """
    A model (table) that represents a course
    
    :param Base: Base class for SQLAlchemy models.
    :type Base: sqlalchemy.ext.declarative.DeclarativeMeta
    """

    __tablename__ = "courses"

    id = Column(Integer,primary_key=True,index=True)
    name = Column(String)
    url = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    duration = Column(Float)
    total_lectures = Column(Integer, nullable=True)
    rating = Column(Float)
    total_students = Column(Integer, nullable=True)
    current_price = Column(Numeric(precision=10, scale=2), nullable=True)
    original_price = Column(Numeric(precision=10, scale=2), nullable=True)
    difficulty_id = Column(Integer, ForeignKey("course_difficulties.id", ondelete='SET NULL'), nullable=True)

    difficulty = relationship("Course_difficulties", backref="courses")
    authors = relationship("Authors", secondary="authors_courses", backref="courses")

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
    """
    A model(table) that contains the different
    types of difficulties for a given course. 
    Used since few difficulty types are present
    (helps with normalization).

    :param Base: Base class for SQLAlchemy models.
    :type Base: sqlalchemy.ext.declarative.DeclarativeMeta
    """

    __tablename__ = "course_difficulties"

    id = Column(Integer,primary_key=True,index=True)
    difficulty = Column(String)
