from sqlmodel import Session, select
from typing import List, Optional
from fastapi import HTTPException
from fastapi import status
from ..models import Task, TaskUpdate
from ..schemas import TaskCreateRequest


class TaskService:
    """
    Service class for handling task-related operations.
    """

    @staticmethod
    def create_task(session: Session, user_id: str, task_data: TaskCreateRequest) -> Task:
        """
        Create a new task for a user.
        """
        try:
            # Validate input data
            if not task_data.title or len(task_data.title.strip()) == 0:
                raise ValueError("Task title cannot be empty")

            if task_data.description and len(task_data.description) > 1000:
                raise ValueError("Task description exceeds 1000 characters")

            # Create task instance with user_id from JWT
            task = Task(
                user_id=user_id,
                title=task_data.title.strip(),
                description=task_data.description,
                completed=False  # Default to not completed
            )

            # Add to session and commit
            session.add(task)
            session.commit()
            session.refresh(task)

            return task
        except ValueError as ve:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=str(ve)
            )
        except Exception as e:
            # Log the error for debugging
            import logging
            logging.error(f"Error creating task: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error during task creation"
            )

    @staticmethod
    def get_tasks_by_user(
        session: Session,
        user_id: str,
        status_filter: Optional[str] = "all"
    ) -> List[Task]:
        """
        Get all tasks for a specific user with optional status filtering.
        """
        query = select(Task).where(Task.user_id == user_id)

        if status_filter == "completed":
            query = query.where(Task.completed == True)
        elif status_filter == "pending":
            query = query.where(Task.completed == False)
        # If status_filter is "all", include both completed and pending tasks

        tasks = session.exec(query).all()
        return tasks

    @staticmethod
    def get_task_by_id_and_user(session: Session, task_id: int, user_id: str) -> Optional[Task]:
        """
        Get a specific task by ID and user ID to ensure ownership.
        """
        query = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        task = session.exec(query).first()
        return task

    @staticmethod
    def update_task(
        session: Session,
        task_id: int,
        user_id: str,
        task_update: TaskUpdate
    ) -> Optional[Task]:
        """
        Update a task if it belongs to the user.
        """
        try:
            task = TaskService.get_task_by_id_and_user(session, task_id, user_id)

            if not task:
                return None

            # Validate input data if title is being updated
            if task_update.title is not None:
                if len(task_update.title.strip()) == 0:
                    raise ValueError("Task title cannot be empty")
                if len(task_update.title) > 200:
                    raise ValueError("Task title exceeds 200 characters")

            if task_update.description is not None and len(task_update.description) > 1000:
                raise ValueError("Task description exceeds 1000 characters")

            # Update only the fields that are provided
            for field, value in task_update.dict(exclude_unset=True).items():
                setattr(task, field, value)

            # Update the updated_at timestamp
            from datetime import datetime
            task.updated_at = datetime.utcnow()

            session.add(task)
            session.commit()
            session.refresh(task)

            return task
        except ValueError as ve:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=str(ve)
            )
        except Exception as e:
            # Log the error for debugging
            import logging
            logging.error(f"Error updating task: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error during task update"
            )

    @staticmethod
    def delete_task(session: Session, task_id: int, user_id: str) -> bool:
        """
        Delete a task if it belongs to the user.
        """
        task = TaskService.get_task_by_id_and_user(session, task_id, user_id)

        if not task:
            return False

        session.delete(task)
        session.commit()

        return True

    @staticmethod
    def toggle_task_completion(session: Session, task_id: int, user_id: str) -> Optional[Task]:
        """
        Toggle the completion status of a task.
        """
        task = TaskService.get_task_by_id_and_user(session, task_id, user_id)

        if not task:
            return None

        # Toggle the completion status
        task.completed = not task.completed

        # Update the updated_at timestamp
        from datetime import datetime
        task.updated_at = datetime.utcnow()

        session.add(task)
        session.commit()
        session.refresh(task)

        return task