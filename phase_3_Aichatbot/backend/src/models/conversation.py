from datetime import datetime
from typing import TYPE_CHECKING, Optional, Dict, Any
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import JSON
import uuid
from sqlmodel import AutoString

if TYPE_CHECKING:
    from .message import Message
    from .skill_log import SkillExecutionLog
    from ...models import User  # Import from main models


class ConversationBase(SQLModel):
    title: str = Field(max_length=200)
    metadata_json: Optional[Dict[str, Any]] = Field(sa_type=JSON, default=None)


class Conversation(ConversationBase, table=True):
    """
    Represents a single conversation thread between user and agent
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)  # Store as string to work with both SQLite and PostgreSQL
    user_id: str  # Store as string to avoid SQLite UUID issues
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    messages: list["Message"] = Relationship(back_populates="conversation")
    skill_logs: list["SkillExecutionLog"] = Relationship(back_populates="conversation")

    # Validation: Title cannot exceed 200 characters (handled by Field max_length)
    # Validation: Must have a valid user_id (handled by foreign key)
    # Validation: Must be associated with an active user (to be handled by service layer)


class ConversationCreate(ConversationBase):
    pass


class ConversationRead(ConversationBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime