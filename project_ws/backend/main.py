from fastapi import FastAPI
from db.db_config import engine
from routers import retrieve_data, modify_data, get_data

app = FastAPI() ## Instatiate the FastAPI application

app.include_router(retrieve_data.router)  ## Include the router from models
app.include_router(modify_data.router)
app.include_router(get_data.router)
