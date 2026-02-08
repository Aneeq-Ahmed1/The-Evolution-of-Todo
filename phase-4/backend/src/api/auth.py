from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import Annotated
from datetime import timedelta
from ..database import get_session
from ..models.user import User, UserCreate, UserRead
from ..schemas.auth import Token, TokenData, UserLogin
from ..services.user_service import create_user, authenticate_user
from ..auth.middleware import create_access_token, get_current_user

router = APIRouter()


@router.post("/auth/register", response_model=UserRead)
def register(user: UserCreate, session: Annotated[Session, Depends(get_session)]):
    """
    Register a new user.
    """
    # Check if user already exists
    from sqlmodel import select
    existing_user = session.exec(select(User).where(User.email == user.email)).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create new user
    db_user = create_user(session, user)

    return db_user


@router.post("/auth/login", response_model=Token)
def login(user_credentials: UserLogin, session: Annotated[Session, Depends(get_session)]):
    """
    Login user and return access token.
    """
    user = authenticate_user(session, user_credentials.email, user_credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token_expires = timedelta(minutes=30)  # 30 minutes for example
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/auth/logout")
def logout():
    """
    Logout user.
    """
    # In a real application, you might want to blacklist the token
    return {"message": "Successfully logged out"}