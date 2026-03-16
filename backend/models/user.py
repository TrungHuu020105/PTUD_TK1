from datetime import datetime, timezone
from typing import Optional

from sqlmodel import SQLModel, Field


class UserBase(SQLModel):
    email: str = Field(..., unique=True, index=True)
    is_active: bool = True


class User(UserBase, table=True):
    """SQLModel database table for users"""
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email})>"
