from sqlmodel import Session, select
from ..models.chat_task import ChatTask
from ..models.conversation import Conversation
from ..models.message import Message
from typing import List, Optional
from datetime import datetime


class MCPTaskTools:
    def __init__(self, session: Session):
        self.session = session

    def add_task(self, user_id: str, title: str, description: Optional[str] = None) -> dict:
        """
        Create a new task for the specified user.
        """
        # Validate required fields
        if not title or len(title.strip()) == 0:
            raise ValueError("Title is required and must be at least 1 character")

        if len(title) > 255:
            raise ValueError("Title must be 255 characters or less")

        # Create new task
        task = ChatTask(
            user_id=user_id,
            title=title.strip(),
            description=description,
            completed=False
        )

        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)

        return {
            "task_id": task.id,
            "status": "pending",
            "title": task.title
        }

    def list_tasks(self, user_id: str, status: Optional[str] = None) -> dict:
        """
        Retrieve a list of tasks for the specified user, with optional status filtering.
        """
        # Build query
        query = select(ChatTask).where(ChatTask.user_id == user_id).order_by(ChatTask.created_at)

        # Apply status filter if provided
        if status:
            if status == "completed":
                query = query.where(ChatTask.completed == True)
            elif status == "pending":
                query = query.where(ChatTask.completed == False)
            elif status != "all":
                raise ValueError(f"Invalid status filter: {status}. Must be 'all', 'pending', or 'completed'")

        tasks = self.session.exec(query).all()

        # Format tasks for response
        formatted_tasks = []
        for task in tasks:
            formatted_tasks.append({
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "created_at": task.created_at.isoformat()
            })

        return {
            "tasks": formatted_tasks
        }

    def complete_task(self, user_id: str, task_id: int) -> dict:
        """
        Mark a specific task as completed for the specified user.
        """
        # Find the task
        task = self.session.get(ChatTask, task_id)

        if not task:
            raise ValueError(f"Task with ID {task_id} not found")

        if task.user_id != user_id:
            raise ValueError(f"Task with ID {task_id} does not belong to user {user_id}")

        # Update completion status
        task.completed = True
        task.updated_at = datetime.now()
        self.session.add(task)
        self.session.commit()

        return {
            "task_id": task.id,
            "status": "completed",
            "title": task.title
        }

    def delete_task(self, user_id: str, task_id: int) -> dict:
        """
        Remove a specific task from the user's task list.
        """
        # Find the task
        task = self.session.get(ChatTask, task_id)

        if not task:
            raise ValueError(f"Task with ID {task_id} not found")

        if task.user_id != user_id:
            raise ValueError(f"Task with ID {task_id} does not belong to user {user_id}")

        # Delete the task
        self.session.delete(task)
        self.session.commit()

        return {
            "task_id": task.id,
            "status": "deleted",
            "title": task.title
        }

    def update_task(self, user_id: str, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> dict:
        """
        Modify the title and/or description of a specific task for the specified user.
        """
        # Find the task
        task = self.session.get(ChatTask, task_id)

        if not task:
            raise ValueError(f"Task with ID {task_id} not found")

        if task.user_id != user_id:
            raise ValueError(f"Task with ID {task_id} does not belong to user {user_id}")

        # Update fields if provided
        if title is not None:
            if len(title) == 0:
                raise ValueError("Title must be at least 1 character")
            if len(title) > 255:
                raise ValueError("Title must be 255 characters or less")
            task.title = title.strip()

        if description is not None:
            task.description = description

        task.updated_at = datetime.now()
        self.session.add(task)
        self.session.commit()

        return {
            "task_id": task.id,
            "status": "completed" if task.completed else "pending",
            "title": task.title
        }