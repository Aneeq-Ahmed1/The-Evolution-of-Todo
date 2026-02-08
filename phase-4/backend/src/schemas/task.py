"""
Pydantic schemas for task requests and responses.
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TaskBase(BaseModel):
    """
    Base schema for task data.
    """
    title: str
    description: Optional[str] = None
    completed: bool = False


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


class TaskUpdate(BaseModel):
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


class TaskUpdateStatus(BaseModel):
    """
    Schema for updating task completion status only.
    """
    completed: bool

    class Config:
        json_schema_extra = {
            "example": {
                "completed": True
            }
        }


class TaskRead(TaskBase):
    """
    Schema for reading task data with additional fields.
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

    class Config:
        from_attributes = True


class TaskReadWithDisplayIndex(TaskRead):
    """
    Schema for reading task data with display index for ordinal references.
    """
    display_index: int


class TaskListResponse(BaseModel):
    """
    Schema for task list response.
    """
    tasks: list[TaskRead]
    total: int


class TaskListWithDisplayResponse(BaseModel):
    """
    Schema for task list response with display indices.
    """
    tasks: list[TaskReadWithDisplayIndex]
    display_mapping: list[dict]  # List of {display_index: int, task_id: int}