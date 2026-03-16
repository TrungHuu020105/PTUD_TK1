from typing import Literal, Optional

from fastapi import APIRouter, Query, Depends, Header, status, HTTPException
from sqlalchemy.orm import Session

from core.database import get_session
from core.security import decode_access_token
from schemas.todo import ToDo, ToDoCreate, ToDoListResponse, ToDoUpdate, ToDoPatch
from services.todo_service import get_service

router = APIRouter(prefix="/todos", tags=["todos"])


def get_current_user_id(authorization: str = Header(None)) -> int:
    """Extract user_id from Authorization header (Bearer token)"""
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Extract token from "Bearer <token>"
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise ValueError
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    return user_id


@router.get("", response_model=ToDoListResponse)
def list_todos(
    is_done: Optional[bool] = None,
    q: Optional[str] = Query(default=None),
    sort: Literal["created_at", "-created_at"] = "created_at",
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    authorization: str = Header(None),
    db: Session = Depends(get_session),
):
    user_id = get_current_user_id(authorization)
    service = get_service(db)
    return service.list_todos(
        owner_id=user_id,
        is_done=is_done,
        q=q,
        sort=sort,
        limit=limit,
        offset=offset,
    )


@router.post("", response_model=ToDo)
def create_todo(
    payload: ToDoCreate,
    authorization: str = Header(None),
    db: Session = Depends(get_session),
):
    user_id = get_current_user_id(authorization)
    service = get_service(db)
    return service.create_todo(owner_id=user_id, payload=payload)


@router.get("/{todo_id}", response_model=ToDo)
def get_todo(
    todo_id: int,
    authorization: str = Header(None),
    db: Session = Depends(get_session),
):
    user_id = get_current_user_id(authorization)
    service = get_service(db)
    return service.get_todo(todo_id, user_id)


@router.put("/{todo_id}", response_model=ToDo)
def update_todo(
    todo_id: int,
    payload: ToDoUpdate,
    authorization: str = Header(None),
    db: Session = Depends(get_session),
):
    user_id = get_current_user_id(authorization)
    service = get_service(db)
    return service.update_todo(todo_id, user_id, payload)


@router.patch("/{todo_id}", response_model=ToDo)
def patch_todo(
    todo_id: int,
    payload: ToDoPatch,
    authorization: str = Header(None),
    db: Session = Depends(get_session),
):
    user_id = get_current_user_id(authorization)
    service = get_service(db)
    return service.patch_todo(todo_id, user_id, payload)


@router.post("/{todo_id}/complete", response_model=ToDo)
def complete_todo(
    todo_id: int,
    authorization: str = Header(None),
    db: Session = Depends(get_session),
):
    user_id = get_current_user_id(authorization)
    service = get_service(db)
    return service.complete_todo(todo_id, user_id)


@router.delete("/{todo_id}", response_model=ToDo)
def delete_todo(
    todo_id: int,
    authorization: str = Header(None),
    db: Session = Depends(get_session),
):
    user_id = get_current_user_id(authorization)
    service = get_service(db)
    return service.delete_todo(todo_id, user_id)


