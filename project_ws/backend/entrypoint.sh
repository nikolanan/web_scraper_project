#!/bin/sh
## Entrypoint script for the backend service
## Strat the FastAPI application using Uvicorn
exec uvicorn main:app --host 0.0.0.0 --port 8000 --reload