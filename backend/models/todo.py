from datetime import datetime, timezone
from typing import Optional

from sqlmodel import SQLModel, Field


class ToDoBase(SQLModel):
    title: str = Field(..., min_length=3, max_length=100, index=True)
    description: Optional[str] = None
    is_done: bool = False


class ToDo(ToDoBase, table=True):
    """SQLModel database table for todos"""
    __tablename__ = "todos"

    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def update_timestamp(self):
        self.updated_at = datetime.now(timezone.utc)
