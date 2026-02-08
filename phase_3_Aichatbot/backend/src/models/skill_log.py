from datetime import datetime
from typing import Optional, Dict, Any
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import JSON
import uuid


class SkillExecutionLogBase(SQLModel):
    skill_name: str
    input_params: Optional[Dict[str, Any]] = Field(sa_type=JSON, default=None)
    output_result: Optional[Dict[str, Any]] = Field(sa_type=JSON, default=None)
    execution_time: Optional[float] = Field(default=None, nullable=True)


class SkillExecutionLog(SkillExecutionLogBase, table=True):
    """
    Logs all skill executions for debugging and analytics
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)  # Store as string to work with both SQLite and PostgreSQL
    conversation_id: str = Field(foreign_key="conversation.id")  # Reference conversation by string ID with foreign key
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    conversation: "Conversation" = Relationship(back_populates="skill_logs")


class SkillExecutionLogCreate(SkillExecutionLogBase):
    conversation_id: uuid.UUID


class SkillExecutionLogRead(SkillExecutionLogBase):
    id: str
    conversation_id: str
    timestamp: datetime