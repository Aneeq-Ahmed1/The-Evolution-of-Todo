from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
from .user import User


class TaskBase(SQLModel):
    title: str = Field(nullable=False, max_length=255)
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False)

    # Intermediate Level - Priority & Tags
    priority: str = Field(default="medium", max_length=20)  # low, medium, high
    tags: Optional[str] = Field(default=None, max_length=500)  # Comma-separated tags
    category: Optional[str] = Field(default=None, max_length=100)  # work, personal, etc.

    # Advanced Level - Due Dates & Recurring
    due_date: Optional[datetime] = Field(default=None)
    due_time: Optional[str] = Field(default=None, max_length=10)  # HH:MM format
    is_recurring: bool = Field(default=False)
    recurrence_pattern: Optional[str] = Field(default=None, max_length=50)  # daily, weekly, monthly
    recurrence_interval: Optional[int] = Field(default=1)  # Every N days/weeks/months
    next_occurrence: Optional[datetime] = Field(default=None)


class Task(TaskBase, table=True):
    """
    Represents a todo item owned by a user with advanced features.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(nullable=False, max_length=255)
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False)
    user_id: int = Field(foreign_key="user.id", nullable=False)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    # Intermediate Level
    priority: str = Field(default="medium", max_length=20)
    tags: Optional[str] = Field(default=None, max_length=500)
    category: Optional[str] = Field(default=None, max_length=100)

    # Advanced Level
    due_date: Optional[datetime] = Field(default=None)
    due_time: Optional[str] = Field(default=None, max_length=10)
    is_recurring: bool = Field(default=False)
    recurrence_pattern: Optional[str] = Field(default=None, max_length=50)
    recurrence_interval: Optional[int] = Field(default=1)
    next_occurrence: Optional[datetime] = Field(default=None)

    # Relationship to User - without back_populates to avoid circular dependency
    user: User = Relationship(sa_relationship_kwargs={"lazy": "selectin"})


class TaskCreate(TaskBase):
    """
    Schema for creating a new task.
    """
    title: str
    user_id: Optional[int] = None  # Will be set from JWT token
    priority: Optional[str] = "medium"
    tags: Optional[str] = None
    category: Optional[str] = None
    due_date: Optional[datetime] = None
    due_time: Optional[str] = None
    is_recurring: Optional[bool] = False
    recurrence_pattern: Optional[str] = None
    recurrence_interval: Optional[int] = 1


class TaskRead(TaskBase):
    """
    Schema for reading task data.
    """
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    priority: str
    tags: Optional[str] = None
    category: Optional[str] = None
    due_date: Optional[datetime] = None
    due_time: Optional[str] = None
    is_recurring: bool
    recurrence_pattern: Optional[str] = None
    recurrence_interval: Optional[int] = None
    next_occurrence: Optional[datetime] = None


class TaskUpdate(SQLModel):
    """
    Schema for updating task information.
    """
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[str] = None
    tags: Optional[str] = None
    category: Optional[str] = None
    due_date: Optional[datetime] = None
    due_time: Optional[str] = None
    is_recurring: Optional[bool] = None
    recurrence_pattern: Optional[str] = None
    recurrence_interval: Optional[int] = None


class TaskUpdateStatus(SQLModel):
    """
    Schema for updating task completion status only.
    """
    completed: bool
