from typing import Optional

from sqlalchemy.orm import Session
from sqlmodel import select

from models.user import User


class UserRepository:
    def __init__(self, session: Session) -> None:
        self._db = session

    def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by id"""
        query = select(User).where(User.id == user_id)
        return self._db.exec(query).first()

    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        query = select(User).where(User.email == email)
        return self._db.exec(query).first()

    def create(self, user: User) -> User:
        """Create new user"""
        self._db.add(user)
        self._db.commit()
        self._db.refresh(user)
        return user
