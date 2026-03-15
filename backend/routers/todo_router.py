from typing import Literal, Optional

from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session

from core.database import get_session
from schemas.todo import ToDo, ToDoCreate, ToDoListResponse, ToDoUpdate, ToDoPatch
from services.todo_service import get_service

router = APIRouter(prefix="/todos", tags=["todos"])


@router.get("", response_model=ToDoListResponse)
def list_todos(
    is_done: Optional[bool] = None,
    q: Optional[str] = Query(default=None),
    sort: Literal["created_at", "-created_at"] = "created_at",
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_session),
):
    service = get_service(db)
    return service.list_todos(
        is_done=is_done,
        q=q,
        sort=sort,
        limit=limit,
        offset=offset,
    )


@router.post("", response_model=ToDo)
def create_todo(payload: ToDoCreate, db: Session = Depends(get_session)):
    service = get_service(db)
    return service.create_todo(payload)


@router.get("/{todo_id}", response_model=ToDo)
def get_todo(todo_id: int, db: Session = Depends(get_session)):
    service = get_service(db)
    return service.get_todo(todo_id)


@router.put("/{todo_id}", response_model=ToDo)
def update_todo(todo_id: int, payload: ToDoUpdate, db: Session = Depends(get_session)):
    service = get_service(db)
    return service.update_todo(todo_id, payload)


@router.patch("/{todo_id}", response_model=ToDo)
def patch_todo(todo_id: int, payload: ToDoPatch, db: Session = Depends(get_session)):
    service = get_service(db)
    return service.patch_todo(todo_id, payload)


@router.post("/{todo_id}/complete", response_model=ToDo)
def complete_todo(todo_id: int, db: Session = Depends(get_session)):
    service = get_service(db)
    return service.complete_todo(todo_id)


@router.delete("/{todo_id}", response_model=ToDo)
def delete_todo(todo_id: int, db: Session = Depends(get_session)):
    service = get_service(db)
    return service.delete_todo(todo_id)

