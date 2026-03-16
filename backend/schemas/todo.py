from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field, field_validator


class ToDoBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = None
    is_done: bool = False

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        normalized = value.strip()
        if len(normalized) < 3 or len(normalized) > 100:
            raise ValueError("title must be between 3 and 100 characters")
        return normalized


class ToDo(ToDoBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime


class ToDoCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = None
    is_done: bool = False

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        normalized = value.strip()
        if len(normalized) < 3 or len(normalized) > 100:
            raise ValueError("title must be between 3 and 100 characters")
        return normalized


class ToDoUpdate(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = None
    is_done: bool

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        normalized = value.strip()
        if len(normalized) < 3 or len(normalized) > 100:
            raise ValueError("title must be between 3 and 100 characters")
        return normalized


class ToDoPatch(BaseModel):
    """Partial update - all fields optional"""
    title: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = None
    is_done: Optional[bool] = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        normalized = value.strip()
        if len(normalized) < 3 or len(normalized) > 100:
            raise ValueError("title must be between 3 and 100 characters")
        return normalized


class ToDoListResponse(BaseModel):
    items: list[ToDo]
    total: int
    limit: int
    offset: int

