from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class UserBase(SQLModel):
    email: str = Field(unique=True, nullable=False, max_length=255)


class User(UserBase, table=True):
    """
    Represents an authenticated user in the system.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, nullable=False, max_length=255)
    password_hash: str = Field(nullable=False, max_length=255)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    is_active: bool = Field(default=True)

    # Removed relationship to avoid circular dependency - handled from Task side only


class UserCreate(UserBase):
    """
    Schema for creating a new user.
    """
    email: str
    password: str


class UserRead(UserBase):
    """
    Schema for reading user data (without sensitive information).
    """
    id: int
    created_at: datetime
    updated_at: datetime
    is_active: bool


class UserUpdate(SQLModel):
    """
    Schema for updating user information.
    """
    email: Optional[str] = None