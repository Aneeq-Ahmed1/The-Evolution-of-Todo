import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import Optional

# Import using absolute imports for compatibility
from phase_2_web.backend import models, schemas
from phase_2_web.backend.db import get_session
from phase_2_web.backend.auth import get_current_user, verify_user_id_match
from phase_2_web.backend.services.task_service import TaskService

# Get logger
logger = logging.getLogger(__name__)


# Create router instance
router = APIRouter()


@router.post("/{user_id}/tasks", response_model=schemas.TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    user_id: str,
    task_data: schemas.TaskCreateRequest,
    current_user=Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Create a new task for the specified user.
    """
    logger.info(f"Creating task for user {user_id}")

    # Verify that the user_id in the JWT matches the user_id in the URL
    verify_user_id_match(current_user.user_id, user_id)

    # Create the task using the service
    task = TaskService.create_task(session, user_id, task_data)

    logger.info(f"Task created successfully with ID {task.id} for user {user_id}")
    return task


@router.get("/{user_id}/tasks", response_model=list[schemas.TaskResponse])
def get_tasks(
    user_id: str,
    status_filter: Optional[str] = "all",
    current_user=Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get all tasks for the specified user with optional status filtering.
    """
    logger.info(f"Fetching tasks for user {user_id} with status filter: {status_filter}")

    # Verify that the user_id in the JWT matches the user_id in the URL
    verify_user_id_match(current_user.user_id, user_id)

    # Validate status filter parameter
    if status_filter not in ["all", "completed", "pending"]:
        logger.warning(f"Invalid status filter: {status_filter}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Status filter must be 'all', 'completed', or 'pending'"
        )

    # Get tasks using the service
    tasks = TaskService.get_tasks_by_user(session, user_id, status_filter)

    logger.info(f"Retrieved {len(tasks)} tasks for user {user_id}")
    return tasks


@router.get("/{user_id}/tasks/{id}", response_model=schemas.TaskResponse)
def get_task(
    user_id: str,
    id: int,
    current_user=Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get a specific task by ID for the specified user.
    """
    logger.info(f"Fetching task {id} for user {user_id}")

    # Verify that the user_id in the JWT matches the user_id in the URL
    verify_user_id_match(current_user.user_id, user_id)

    # Get task using the service
    task = TaskService.get_task_by_id_and_user(session, id, user_id)

    if not task:
        logger.warning(f"Task {id} not found for user {user_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    logger.info(f"Task {id} retrieved successfully for user {user_id}")
    return task


@router.put("/{user_id}/tasks/{id}", response_model=schemas.TaskResponse)
def update_task(
    user_id: str,
    id: int,
    task_update: schemas.TaskUpdateRequest,
    current_user=Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Update a specific task by ID for the specified user.
    """
    logger.info(f"Updating task {id} for user {user_id}")

    # Verify that the user_id in the JWT matches the user_id in the URL
    verify_user_id_match(current_user.user_id, user_id)

    # Update task using the service
    task = TaskService.update_task(session, id, user_id, models.TaskUpdate(**task_update.dict(exclude_unset=True)))

    if not task:
        logger.warning(f"Task {id} not found for user {user_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    logger.info(f"Task {id} updated successfully for user {user_id}")
    return task


@router.delete("/{user_id}/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    user_id: str,
    id: int,
    current_user=Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Delete a specific task by ID for the specified user.
    """
    logger.info(f"Deleting task {id} for user {user_id}")

    # Verify that the user_id in the JWT matches the user_id in the URL
    verify_user_id_match(current_user.user_id, user_id)

    # Delete task using the service
    success = TaskService.delete_task(session, id, user_id)

    if not success:
        logger.warning(f"Task {id} not found for user {user_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    logger.info(f"Task {id} deleted successfully for user {user_id}")
    # Return 204 No Content on successful deletion
    return


@router.patch("/{user_id}/tasks/{id}/complete", response_model=schemas.TaskResponse)
def toggle_task_completion(
    user_id: str,
    id: int,
    task_toggle: schemas.TaskToggleCompleteRequest,
    current_user=Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Toggle the completion status of a specific task by ID for the specified user.
    """
    logger.info(f"Toggling completion status for task {id} for user {user_id}")

    # Verify that the user_id in the JWT matches the user_id in the URL
    verify_user_id_match(current_user.user_id, user_id)

    # Toggle task completion using the service
    task = TaskService.toggle_task_completion(session, id, user_id)

    if not task:
        logger.warning(f"Task {id} not found for user {user_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    logger.info(f"Task {id} completion status toggled successfully for user {user_id}")
    return task