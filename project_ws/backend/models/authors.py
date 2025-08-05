from db.db_config import Base
from sqlalchemy import Column, Integer, String, ForeignKey

class Authors(Base):
    __tablename__ = "authors"

    id = Column(Integer,primary_key=True,index=True)
    name = Column(String)

class Authors_Courses(Base):
    __tablename__ = "authors_courses"

    id = Column(Integer,primary_key=True,index=True)
    author_id = Column(Integer, ForeignKey("authors.id", ondelete='SET NULL'), nullable=True)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete='CASCADE'))