from db.db_config import Base
from sqlalchemy import Column, Integer, String, ForeignKey

class Authors(Base):
    """
    A model(table) that represents an Author
    
    :param Base: Base class for SQLAlchemy models.
    :type Base: sqlalchemy.ext.declarative.DeclarativeMeta
    """

    __tablename__ = "authors"

    id = Column(Integer,primary_key=True,index=True)
    name = Column(String)

class Authors_Courses(Base):
    """
    A model(association table) that represents the conncention
    beween an Author and Couse(M:M), in this case:
    Author - Authors_Courses (1:M)
    Courses - Authors_Courses (1:M)
    
    :param Base: Base class for SQLAlchemy models.
    :type Base: sqlalchemy.ext.declarative.DeclarativeMeta
    """

    __tablename__ = "authors_courses"

    id = Column(Integer,primary_key=True,index=True)
    author_id = Column(Integer, ForeignKey("authors.id", ondelete='SET NULL'), nullable=True)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete='CASCADE'))