"""
Task data model for the In-Memory Todo Console Application
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Task:
    """
    Represents a single todo item with id, title, description, and completion status
    """
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False
    created_at: datetime = None
    last_accessed: datetime = None

    def __post_init__(self):
        """Initialize datetime fields if not provided"""
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.last_accessed is None:
            self.last_accessed = datetime.now()

    def validate(self) -> bool:
        """
        Validate the task attributes
        Returns True if valid, False otherwise
        """
        # Validate title: non-empty, max 200 characters
        if not self.title or len(self.title) == 0:
            raise ValueError("Task title cannot be empty")
        if len(self.title) > 200:
            raise ValueError(f"Task title exceeds 200 characters: {len(self.title)}")

        # Validate description: max 1000 characters
        if self.description and len(self.description) > 1000:
            raise ValueError(f"Task description exceeds 1000 characters: {len(self.description)}")

        return True