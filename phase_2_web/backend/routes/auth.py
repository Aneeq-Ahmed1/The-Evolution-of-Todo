from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from typing import Optional
import jwt
from datetime import datetime, timedelta
import uuid

from phase_2_web.backend import models, schemas
from phase_2_web.backend.db import get_session
from phase_2_web.backend.auth import verify_token
from phase_2_web.backend.settings import settings

# Create router instance
router = APIRouter()

@router.post("/auth/register", response_model=schemas.AuthResponse)
def register(
    email: str = Form(...),
    password: str = Form(...),
    name: Optional[str] = Form(None),
    session: Session = Depends(get_session)
):
    """
    Register a new user.
    """
    try:
        # Check if user already exists
        existing_user = session.exec(select(models.User).where(models.User.email == email)).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already exists"
            )

        # Validate email format
        if not email or '@' not in email or '.' not in email.split('@')[1]:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid email format"
            )

        # Validate password length
        if not password or len(password) < 6:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Password must be at least 6 characters long"
            )

        # Create new user with a unique ID
        user_id = str(uuid.uuid4())
        user = models.User(
            id=user_id,
            email=email,
            name=name or email.split('@')[0]  # Use part of email as name if not provided
        )
        user.set_password(password)  # Hash the password

        session.add(user)
        session.commit()
        session.refresh(user)

        # Create JWT token
        token_data = {
            "id": user.id,
            "email": user.email,
            "exp": datetime.utcnow() + timedelta(hours=24)  # Token expires in 24 hours
        }
        access_token = jwt.encode(token_data, settings.BETTER_AUTH_SECRET, algorithm="HS256")

        return schemas.AuthResponse(
            user=schemas.UserResponse(id=user.id, email=user.email, name=user.name),
            access_token=access_token
        )
    except HTTPException:
        raise
    except Exception as e:
        # Log the error for debugging
        import logging
        logging.error(f"Registration error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during registration"
        )


@router.post("/auth/login", response_model=schemas.AuthResponse)
def login(
    email: str = Form(...),
    password: str = Form(...),
    session: Session = Depends(get_session)
):
    """
    Login a user and return JWT token.
    """
    try:
        # Validate input
        if not email or not password:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Email and password are required"
            )

        # Find user by email
        user = session.exec(select(models.User).where(models.User.email == email)).first()
        if not user or not user.verify_password(password):  # Verify hashed password
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        # Create JWT token
        token_data = {
            "id": user.id,
            "email": user.email,
            "exp": datetime.utcnow() + timedelta(hours=24)  # Token expires in 24 hours
        }
        access_token = jwt.encode(token_data, settings.BETTER_AUTH_SECRET, algorithm="HS256")

        return schemas.AuthResponse(
            user=schemas.UserResponse(id=user.id, email=user.email, name=user.name),
            access_token=access_token
        )
    except HTTPException:
        raise
    except Exception as e:
        # Log the error for debugging
        import logging
        logging.error(f"Login error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during login"
        )


@router.post("/auth/logout")
def logout():
    """
    Logout endpoint (mainly for documentation purposes).
    """
    return {"message": "Logged out successfully"}


@router.get("/auth/me", response_model=schemas.UserResponse)
def get_current_user_info(current_user: schemas.TokenData = Depends(verify_token)):
    """
    Get current user information from JWT token.
    """
    return schemas.UserResponse(
        id=current_user.user_id,
        email=current_user.email,
        name=getattr(current_user, 'name', current_user.email.split('@')[0])
    )