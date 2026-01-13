from sqlmodel import SQLModel, Field, create_engine
from typing import Optional
from datetime import datetime
from passlib.context import CryptContext


# Configure argon2 as the password hashing scheme (more reliable than bcrypt on Windows)
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


class TaskBase(SQLModel):
    """
    Base model for Task with common fields.
    """
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)


class Task(TaskBase, table=True):
    """
    Task model representing a user's todo item.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)  # Indexed for efficient user-based queries
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class TaskUpdate(TaskBase):
    """
    Model for updating task fields.
    """
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: Optional[bool] = None


class User(SQLModel, table=True):
    """
    User model for authentication.
    """
    id: Optional[str] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    password: str  # This will be hashed
    name: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    def set_password(self, password: str):
        """Hash and set the user's password."""
        # Truncate password if it exceeds bcrypt's 72-byte limit
        if len(password.encode('utf-8')) > 72:
            password = password[:72]
        self.password = pwd_context.hash(password)

    def verify_password(self, password: str) -> bool:
        """Verify a password against the stored hash."""
        return pwd_context.verify(password, self.password)