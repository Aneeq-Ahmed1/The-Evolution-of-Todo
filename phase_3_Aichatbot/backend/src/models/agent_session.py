from datetime import datetime
from typing import Optional, Dict, Any
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import JSON
import uuid


class AgentSessionBase(SQLModel):
    current_agent: str
    context_state: Optional[Dict[str, Any]] = Field(sa_type=JSON, default=None)
    expires_at: datetime


class AgentSession(AgentSessionBase, table=True):
    """
    Tracks active agent sessions for state management
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)  # Store as string to work with both SQLite and PostgreSQL
    user_id: str = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Validation: Cannot have overlapping sessions for the same user (to be handled by service layer)
    # Validation: Expiration time must be in the future (to be handled by service layer)
    # Validation: Current agent must be a valid registered agent type (to be handled by service layer)
    # Validation: Context state size limited to 1MB (to be handled by service layer)


class AgentSessionCreate(AgentSessionBase):
    user_id: str  # Changed from uuid.UUID to str to match the field definition


class AgentSessionRead(AgentSessionBase):
    id: str
    user_id: str
    created_at: datetime