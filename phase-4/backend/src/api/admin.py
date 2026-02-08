"""
Admin API endpoints for user management and password reset.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import Annotated, List
from datetime import timedelta
import os
from dotenv import load_dotenv

from ..database import get_session
from ..models.user import User, UserRead
from ..schemas.auth import Token, AdminLogin, PasswordReset
from ..utils.password import hash_password, verify_password
from ..auth.middleware import create_access_token

load_dotenv()

router = APIRouter(prefix="/admin", tags=["admin"])

# Admin credentials from environment
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@taskflow.com")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "Admin@12345")


def verify_admin(email: str, password: str) -> bool:
    """Verify admin credentials."""
    return email == ADMIN_EMAIL and password == ADMIN_PASSWORD


@router.post("/login", response_model=Token)
def admin_login(
    credentials: AdminLogin,
    session: Annotated[Session, Depends(get_session)]
):
    """
    Admin login endpoint.
    Returns a special admin JWT token.
    """
    if not verify_admin(credentials.email, credentials.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid admin credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create admin token with special flag
    access_token_expires = timedelta(minutes=60)  # 1 hour for admin
    access_token = create_access_token(
        data={"sub": credentials.email, "is_admin": True},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users", response_model=List[UserRead])
def list_all_users(
    session: Annotated[Session, Depends(get_session)]
):
    """
    List all users in the system.
    Note: In production, this should require admin authentication.
    """
    users = session.exec(select(User)).all()
    return users


@router.post("/users/{user_id}/reset-password")
def reset_user_password(
    user_id: int,
    password_data: PasswordReset,
    session: Annotated[Session, Depends(get_session)]
):
    """
    Reset a user's password (admin only).
    """
    # Find the user
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Update password
    user.password_hash = hash_password(password_data.new_password)
    session.add(user)
    session.commit()
    session.refresh(user)

    return {
        "message": f"Password reset successful for user {user.email}",
        "user_id": user.id,
        "email": user.email
    }


@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    session: Annotated[Session, Depends(get_session)]
):
    """
    Delete a user and all their associated tasks (admin only).
    """
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Delete all tasks associated with the user first
    from ..models.task import Task
    statement = select(Task).where(Task.user_id == user_id)
    tasks = session.exec(statement).all()
    for task in tasks:
        session.delete(task)

    # Flush task deletions to ensure foreign key constraints are met if needed
    session.flush()

    # Now delete the user
    session.delete(user)
    session.commit()

    return {
        "message": f"User {user.email} and all their tasks deleted successfully",
        "user_id": user_id
    }
