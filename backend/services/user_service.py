from datetime import timedelta

from fastapi import HTTPException
from sqlalchemy.orm import Session

from core.security import create_access_token, hash_password, verify_password
from models.user import User
from repositories.user_repository import UserRepository
from schemas.user import Token, User as UserSchema
from schemas.user import UserLogin, UserRegister


class UserService:
    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    def register(self, payload: UserRegister) -> UserSchema:
        """Register new user"""
        existing = self._repository.get_by_email(payload.email)
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")

        user = User(
            email=payload.email,
            hashed_password=hash_password(payload.password),
        )
        saved_user = self._repository.create(user)
        return UserSchema.model_validate(saved_user)

    def login(self, payload: UserLogin) -> Token:
        """Login user and return JWT token"""
        user = self._repository.get_by_email(payload.email)
        if not user or not verify_password(payload.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        if not user.is_active:
            raise HTTPException(status_code=403, detail="User is inactive")

        access_token = create_access_token(data={"sub": user.id})
        return Token(access_token=access_token)

    def get_current_user(self, user_id: int) -> UserSchema:
        """Get current user by id"""
        user = self._repository.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if not user.is_active:
            raise HTTPException(status_code=403, detail="User is inactive")
        return UserSchema.model_validate(user)


def get_user_service(db: Session) -> UserService:
    repository = UserRepository(db)
    return UserService(repository)
