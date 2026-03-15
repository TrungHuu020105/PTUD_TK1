from fastapi import FastAPI

from core.config import settings
from core.database import create_db_and_tables
from routers import api_router

app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


app.include_router(api_router, prefix=settings.API_V1_PREFIX)


@app.get("/")
def root():
    return {"message": "Chào mừng bạn đến vưới To-Do List API!"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


