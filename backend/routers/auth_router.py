from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.database import get_session
from core.security import decode_access_token
from schemas.user import Token, User, UserLogin, UserRegister
from services.user_service import get_user_service


router = APIRouter(prefix="/auth", tags=["auth"])


def get_current_user_id(token: str = None) -> int:
    """Extract user_id from JWT token (Bearer token)"""
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Remove "Bearer " prefix if present
    if token.startswith("Bearer "):
        token = token[7:]
    
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    return user_id


@router.post("/register", response_model=User)
def register(payload: UserRegister, db: Session = Depends(get_session)):
    """Register a new user"""
    service = get_user_service(db)
    return service.register(payload)


@router.post("/login", response_model=Token)
def login(payload: UserLogin, db: Session = Depends(get_session)):
    """Login with email and password, return JWT token"""
    service = get_user_service(db)
    return service.login(payload)


@router.get("/me", response_model=User)
def get_me(
    authorization: str = None,
    db: Session = Depends(get_session),
):
    """Get current authenticated user"""
    user_id = get_current_user_id(authorization)
    service = get_user_service(db)
    return service.get_current_user(user_id)
