from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class ConversationBase(SQLModel):
    user_id: str  # Using string for user_id from authentication


class Conversation(ConversationBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(nullable=False)  # User association
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)