from fastapi import APIRouter

from routers.todo_router import router as todo_router

api_router = APIRouter()
api_router.include_router(todo_router)
