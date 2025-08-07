# IT Courses web scraper

## Aim of the Project

The aim of this project is to provide a robust, containerized web scraping and data retrieval backend for collecting, processing, and serving course information from the online learning platforms **Udemy** and **Pluralsight**. The backend is built with FastAPI, uses Selenium with undected driver for scraping, and stores data in a PostgreSQL database. The project is designed for extensibility, maintainability, and ease of deployment using Docker. The sturcture allows for extensive scalability.

---

### Top-Level Files

- **docker-compose.yml**  
  Orchestrates multi-container Docker applications. Defines services for the backend, PostgreSQL database, and pgAdmin (database GUI).

- **.env**  
  Stores environment variables such as database credentials and secrets, used by Docker and the application. (I know that it must never be pushed to the repo, but if you don't congfigure it yourself is just easier.)

- **readme.md**  
  This documentation file.

---

### backend/

- **main.py**  
  The FastAPI application entry point. Initializes the app, includes routers, and sets up event handlers.

- **requirements.txt**  
  Lists all Python dependencies required for the backend, including FastAPI, SQLAlchemy, Selenium, Alembic, and others.

- **dockerfile.backend**  
  Dockerfile for building the backend image. Installs system and Python dependencies, copies the backend code, and sets up the entrypoint.

- **entrypoint.sh**  
  Shell script used as the container entrypoint. It starts the application using **exec uvicorn main:app --host 0.0.0.0 --port 8000 --reload**

---

#### backend/utils/

- **logger.py**  
    Provides a configuration for the logging.

- **web_scraper_scripts/**  
    Contains all web scraping scripts for different platforms.

- **pluralsight_web_scraper.py**  
- **udemy_web_scraper.py**  
    Both implements scraping logic for Udemy and Pluralsight, including functions to extract course data, handle pagination, and log scraping events.

- **multiple_pages_scraper.py**
    Scrapes multiple pages for either Udemy or Pluralsight. Th main function takes 3
    arguments **staring page** , **ending page** and the **websites's name** (udemy or pluralsight)

- **exceptions.py**
    Defines custom exceptions that are triggered is particular part from the
    web scraped data is missing or currupted

---

#### backend/schemas/

- **db_retrieval_schema.py**  
    Pydantic models for serializing and validating data retrieved from the database.  
    - `AuthorOut`: Represents a course author.
    - `DifficultyOut`: Represents course difficulty.
    - `CourseOut`: Represents a course with all related fields.

- **web_retrieval_schema.py**  
   Pydantic models for validating and serializing data scraped from the web before storage or further processing.  
   - `CourseInput`: Represents a single scraped course.
   - `CoursesInput`: Represents a batch of scraped courses.

---

#### backend/routers/

- **(router files)**  
    Define API endpoints for the FastAPI application. Each file typically corresponds to a resource (e.g., courses, authors) and organizes related endpoints.

- **get_data.py**
    Only GET requests

- **modify_data.py**
    A DELETE request

- **retrieve_data.py**
    A POST request from scraping data
    from both udemy and pluralsight

---

#### backend/db

- **db_config.py**
    Configuration for the database (connection to PostgreSQL and establishing engine and session)
- **db_params.py**
    Gets the database credentials which are then imported in **db_config.py**

---

## How It Works

1. **Scraping**  
    Web scraping scripts use Selenium to extract course data from online platforms. Decorators manage browser setup and teardown, and logging captures scraping events and errors.

2. **Data Validation**  
    Scraped data is validated using Pydantic schemas (`web_retrieval_schema.py`) before being processed or stored.

3. **Database Storage**  
    Validated data is stored in a PostgreSQL database. The data is checked again before insertion and if an error arires the trasaction will be rolled in order to prevent curropt data entering the database. SQLAlchemy models (not shown here) and Alembic are used for ORM and migrations.

4. **API**  
    FastAPI serves endpoints for retrieving and managing course data. (Each has its own
    extensive documentation)

5. **Containerization**  
    Docker and Docker Compose manage the backend, database, and admin interface, making development and deployment consistent and reproducible.

---

## How to run the project 

-Navigate to folder: **project_ws** and then run

```
docker-compose up --build
```

to start all containers.

Use this url for the FastAPI interface:
```
http://localhost:8000/docs
```

Use this url for the pg_admin:
```
http://localhost:5050/browser/
```
