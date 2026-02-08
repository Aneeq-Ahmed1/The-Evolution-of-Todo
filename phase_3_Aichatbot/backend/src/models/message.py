from datetime import datetime
from typing import Optional, Dict, Any
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import JSON
import uuid


class MessageBase(SQLModel):
    role: str  # Enum: 'user', 'assistant', 'system', 'tool'
    content: str = Field(sa_column_kwargs={"nullable": False})
    tool_calls: Optional[Dict[str, Any]] = Field(sa_type=JSON, default=None)
    tool_response: Optional[Dict[str, Any]] = Field(sa_type=JSON, default=None)


class Message(MessageBase, table=True):
    """
    Represents a single message in a conversation
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)  # Store as string to work with both SQLite and PostgreSQL
    conversation_id: str = Field(foreign_key="conversation.id")  # Reference conversation by string ID with foreign key
    user_id: str  # Store user_id directly on message for faster queries
    created_at: datetime = Field(default_factory=datetime.utcnow)  # Required by database schema
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    conversation: "Conversation" = Relationship(back_populates="messages")

    # Validation: Role must be one of the allowed enum values (to be handled by service layer)
    # Validation: Content cannot be empty (except for tool responses) (handled by nullable settings)
    # Validation: Must belong to an active conversation (to be handled by service layer)
    # Validation: Timestamp must be current or past (not future) (handled by default_factory)


class MessageCreate(MessageBase):
    user_id: str


class MessageRead(MessageBase):
    id: str
    conversation_id: str
    user_id: str
    created_at: datetime
    timestamp: datetime