from datetime import datetime, timezone
from typing import Optional, List

from sqlmodel import SQLModel, Field, Relationship


class ToDoBase(SQLModel):
    title: str = Field(..., min_length=3, max_length=100, index=True)
    description: Optional[str] = None
    is_done: bool = False
    due_date: Optional[datetime] = None


class ToDo(ToDoBase, table=True):
    """SQLModel database table for todos"""
    __tablename__ = "todos"

    id: Optional[int] = Field(default=None, primary_key=True)
    owner_id: int = Field(foreign_key="users.id", index=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    # Relationship to tags
    tags: List["Tag"] = Relationship(back_populates="todos", link_model="TodoTag")

    def update_timestamp(self):
        self.updated_at = datetime.now(timezone.utc)
    
    def is_overdue(self) -> bool:
        """Check if todo is overdue (due_date in past and not done)"""
        if not self.due_date or self.is_done:
            return False
        return self.due_date < datetime.now(timezone.utc)
    
    def is_due_today(self) -> bool:
        """Check if todo is due today"""
        if not self.due_date:
            return False
        today = datetime.now(timezone.utc).date()
        return self.due_date.date() == today


class Tag(SQLModel, table=True):
    """SQLModel database table for tags"""
    __tablename__ = "tags"

    id: Optional[int] = Field(default=None, primary_key=True)
    owner_id: int = Field(foreign_key="users.id", index=True)
    name: str = Field(..., min_length=1, max_length=50)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    # Relationship to todos (via TodoTag)
    todos: List[ToDo] = Relationship(back_populates="tags", link_model="TodoTag")
    
    __table_args__ = (
        # Composite unique key: user can't have duplicate tag names
        # (This would be handled at service level for now)
    )


class TodoTag(SQLModel, table=True):
    """Join table for many-to-many relationship between todos and tags"""
    __tablename__ = "todo_tags"

    todo_id: int = Field(foreign_key="todos.id", primary_key=True)
    tag_id: int = Field(foreign_key="tags.id", primary_key=True)

