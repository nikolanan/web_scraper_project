from fastapi import FastAPI
from db.db_config import engine
from routers import retrieve_data

app = FastAPI() ## Instatiate the FastAPI application

app.include_router(retrieve_data.router)  ## Include the router from models

