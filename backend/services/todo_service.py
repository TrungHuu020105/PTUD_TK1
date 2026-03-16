from typing import Literal, Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.todo import ToDo
from repositories.todo_repository import ToDoRepository
from schemas.todo import ToDo as ToDoSchema
from schemas.todo import ToDoCreate, ToDoListResponse, ToDoUpdate, ToDoPatch


class ToDoService:
    def __init__(self, repository: ToDoRepository) -> None:
        self._repository = repository

    def list_todos(
        self,
        owner_id: int,
        is_done: Optional[bool],
        q: Optional[str],
        sort: Literal["created_at", "-created_at"],
        limit: int,
        offset: int,
    ) -> ToDoListResponse:
        items, total = self._repository.list_all(
            owner_id=owner_id,
            is_done=is_done,
            search=q,
            sort=sort,
            limit=limit,
            offset=offset,
        )
        items_dto = [ToDoSchema.model_validate(item) for item in items]
        return ToDoListResponse(items=items_dto, total=total, limit=limit, offset=offset)

    def create_todo(self, owner_id: int, payload: ToDoCreate) -> ToDoSchema:
        todo = ToDo(
            owner_id=owner_id,
            title=payload.title,
            description=payload.description,
            is_done=payload.is_done,
        )
        saved_todo = self._repository.create(todo)
        return ToDoSchema.model_validate(saved_todo)

    def get_todo(self, todo_id: int, owner_id: int) -> ToDoSchema:
        todo = self._repository.get_by_id(todo_id, owner_id)
        if todo is None:
            raise HTTPException(status_code=404, detail="ToDo not found")
        return ToDoSchema.model_validate(todo)

    def update_todo(self, todo_id: int, owner_id: int, payload: ToDoUpdate) -> ToDoSchema:
        todo = self._repository.get_by_id(todo_id, owner_id)
        if todo is None:
            raise HTTPException(status_code=404, detail="ToDo not found")

        todo.title = payload.title
        todo.description = payload.description
        todo.is_done = payload.is_done
        updated_todo = self._repository.update(todo)
        return ToDoSchema.model_validate(updated_todo)

    def patch_todo(self, todo_id: int, owner_id: int, payload: ToDoPatch) -> ToDoSchema:
        """Partial update - only update provided fields"""
        todo = self._repository.get_by_id(todo_id, owner_id)
        if todo is None:
            raise HTTPException(status_code=404, detail="ToDo not found")

        if payload.title is not None:
            todo.title = payload.title
        if payload.description is not None:
            todo.description = payload.description
        if payload.is_done is not None:
            todo.is_done = payload.is_done

        updated_todo = self._repository.update(todo)
        return ToDoSchema.model_validate(updated_todo)

    def complete_todo(self, todo_id: int, owner_id: int) -> ToDoSchema:
        """Mark todo as completed"""
        todo = self._repository.get_by_id(todo_id, owner_id)
        if todo is None:
            raise HTTPException(status_code=404, detail="ToDo not found")

        todo.is_done = True
        updated_todo = self._repository.update(todo)
        return ToDoSchema.model_validate(updated_todo)

    def delete_todo(self, todo_id: int, owner_id: int) -> ToDoSchema:
        todo = self._repository.get_by_id(todo_id, owner_id)
        if todo is None:
            raise HTTPException(status_code=404, detail="ToDo not found")
        deleted_todo = self._repository.delete(todo_id, owner_id)
        return ToDoSchema.model_validate(deleted_todo)


def get_service(db: Session) -> ToDoService:
    repository = ToDoRepository(db)
    return ToDoService(repository)
