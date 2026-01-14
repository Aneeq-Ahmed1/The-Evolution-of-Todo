from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


# Request Schemas
class TaskCreateRequest(BaseModel):
    """
    Schema for creating a new task.
    """
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)


class TaskUpdateRequest(BaseModel):
    """
    Schema for updating an existing task.
    """
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: Optional[bool] = None


class TaskToggleCompleteRequest(BaseModel):
    """
    Schema for toggling task completion status.
    """
    completed: Optional[bool] = None


# Response Schemas
class TaskResponse(BaseModel):
    """
    Schema for task response.
    """
    id: int
    user_id: str
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    updated_at: datetime


class TaskListResponse(BaseModel):
    """
    Schema for task list response.
    """
    tasks: List[TaskResponse]


# User and Auth Schemas
class UserResponse(BaseModel):
    """
    Schema for user response.
    """
    id: str
    email: str
    name: Optional[str] = None


class AuthResponse(BaseModel):
    """
    Schema for authentication response.
    """
    user: UserResponse
    access_token: str


class TokenData(BaseModel):
    """
    Schema for JWT token data.
    """
    user_id: str
    email: Optional[str] = None
    name: Optional[str] = None


# Query Parameter Schemas
class TaskFilterQuery(BaseModel):
    """
    Schema for task filtering query parameters.
    """
    status: Optional[str] = Field(default="all", description="Filter by status: all, completed, pending")


# Error Response Schema
class ErrorResponse(BaseModel):
    """
    Schema for error responses.
    """
    detail: str