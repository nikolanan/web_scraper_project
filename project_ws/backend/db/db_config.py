from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from .db_params import DB_USER, DB_PASSWORD, DB_NAME, DB_PORT, DB_HOST

##This defines the location of the Postgre database file
SQLALCHEMY_DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

## Creates a database engine, which is how SQLAlchemy communicates with your actual database.
engine = create_engine(SQLALCHEMY_DATABASE_URL)

## A factory that will create new Session objects, which are used to interact with the database
## (e.g., insert, query, update).
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

## Used to create a base class for ORM models (tables).
Base = declarative_base()
