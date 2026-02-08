from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class MessageBase(SQLModel):
    user_id: str  # Using string for user_id from authentication
    conversation_id: int
    role: str = Field(regex="^(user|assistant)$")  # Either 'user' or 'assistant'
    content: str


class Message(MessageBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(nullable=False)  # User association
    conversation_id: int = Field(nullable=False)  # Conversation association
    role: str = Field(regex="^(user|assistant)$", nullable=False)  # Either 'user' or 'assistant'
    content: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.now)