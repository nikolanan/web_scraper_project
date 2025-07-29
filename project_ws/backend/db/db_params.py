from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

## User credentials for PostgreSQL database
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")

## Database configuration
DB_NAME = os.getenv("POSTGRES_DB")
DB_PORT = os.getenv("DB_PORT", "5432")  # Default to 5432
DB_HOST = os.getenv("DB_HOST", "db")  # Default to 'db' for the docker setup