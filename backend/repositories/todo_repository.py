from typing import Literal, Optional
from datetime import datetime, timezone, date, time, timedelta

from sqlalchemy.orm import Session
from sqlmodel import select

from models.todo import ToDo


class ToDoRepository:
    def __init__(self, session: Session) -> None:
        self._db = session

    def list_all(
        self,
        owner_id: int,
        is_done: Optional[bool] = None,
        search: Optional[str] = None,
        sort: Literal["created_at", "-created_at"] = "created_at",
        limit: int = 10,
        offset: int = 0,
    ) -> tuple[list[ToDo], int]:
        """List todos for owner with filtering, searching, sorting, and pagination"""
        query = select(ToDo).where(ToDo.owner_id == owner_id)

        if is_done is not None:
            query = query.where(ToDo.is_done == is_done)

        if search:
            keyword = f"%{search.lower()}%"
            query = query.where(
                (ToDo.title.ilike(keyword)) | (ToDo.description.ilike(keyword))
            )

        reverse = sort.startswith("-")
        query = query.order_by(ToDo.created_at.desc() if reverse else ToDo.created_at.asc())

        total = len(self._db.exec(query).all())
        
        items = self._db.exec(query.offset(offset).limit(limit)).all()
        return items, total

    def list_overdue(
        self,
        owner_id: int,
        search: Optional[str] = None,
        limit: int = 10,
        offset: int = 0,
    ) -> tuple[list[ToDo], int]:
        """List overdue todos (due_date < now, is_done=false)"""
        now = datetime.now(timezone.utc)
        query = select(ToDo).where(
            (ToDo.owner_id == owner_id)
            & (ToDo.due_date.isnot(None))
            & (ToDo.due_date < now)
            & (ToDo.is_done == False)
        )

        if search:
            keyword = f"%{search.lower()}%"
            query = query.where(
                (ToDo.title.ilike(keyword)) | (ToDo.description.ilike(keyword))
            )

        query = query.order_by(ToDo.due_date.asc())
        total = len(self._db.exec(query).all())
        
        items = self._db.exec(query.offset(offset).limit(limit)).all()
        return items, total

    def list_today(
        self,
        owner_id: int,
        search: Optional[str] = None,
        limit: int = 10,
        offset: int = 0,
    ) -> tuple[list[ToDo], int]:
        """List todos due today (is_done=false)"""
        today = date.today()
        query = select(ToDo).where(
            (ToDo.owner_id == owner_id)
            & (ToDo.due_date.isnot(None))
            & (ToDo.is_done == False)
        )

        if search:
            keyword = f"%{search.lower()}%"
            query = query.where(
                (ToDo.title.ilike(keyword)) | (ToDo.description.ilike(keyword))
            )

        # Filter by due_date matching today using BETWEEN approach
        today_start = datetime.combine(today, time.min).replace(tzinfo=timezone.utc)
        today_end = datetime.combine(today, time.max).replace(tzinfo=timezone.utc)
        
        query = query.where((ToDo.due_date >= today_start) & (ToDo.due_date <= today_end))
        query = query.order_by(ToDo.due_date.asc())
        
        total = len(self._db.exec(query).all())
        items = self._db.exec(query.offset(offset).limit(limit)).all()
        return items, total

    def get_by_id(self, todo_id: int, owner_id: int) -> Optional[ToDo]:
        """Get todo by id, verify owner"""
        query = select(ToDo).where(
            (ToDo.id == todo_id) & (ToDo.owner_id == owner_id)
        )
        return self._db.exec(query).first()

    def create(self, todo: ToDo) -> ToDo:
        """Create new todo"""
        self._db.add(todo)
        self._db.commit()
        self._db.refresh(todo)
        return todo

    def update(self, todo: ToDo) -> ToDo:
        """Update todo"""
        todo.update_timestamp()
        self._db.add(todo)
        self._db.commit()
        self._db.refresh(todo)
        return todo

    def delete(self, todo_id: int, owner_id: int) -> Optional[ToDo]:
        """Delete todo by id, verify owner"""
        todo = self.get_by_id(todo_id, owner_id)
        if todo:
            self._db.delete(todo)
            self._db.commit()
        return todo

