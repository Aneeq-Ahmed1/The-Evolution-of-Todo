from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class ChatTaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False)
    user_id: str  # Using string for user_id from authentication


class ChatTask(ChatTaskBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(nullable=False)  # User association
    title: str = Field(min_length=1, max_length=255, nullable=False)
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)