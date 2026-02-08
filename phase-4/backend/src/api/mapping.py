"""
API endpoints for display index to task_id mapping operations.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import Annotated, Dict, Optional
from datetime import datetime
from ..database import get_session
from ..models.user import User
from ..models.task import Task
from ..schemas.auth import TokenData
from ..auth.middleware import get_current_user
from ..services.mapping_service import mapping_service
from ..services.task_service import (
    get_user_tasks,
    get_task_by_id,
    update_task,
    delete_task,
    update_task_status
)
from ..schemas.task import TaskRead, TaskUpdate, TaskUpdateStatus


router = APIRouter()


@router.post("/mapping/refresh")
def refresh_display_mapping(
    current_user: Annotated[TokenData, Depends(get_current_user)],
    session: Annotated[Session, Depends(get_session)]
):
    """
    Refresh the display index to task_id mapping after task list changes.
    """
    # Get the user from the database to ensure they exist
    user = session.exec(select(User).where(User.email == current_user.email)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Get all tasks for the user
    tasks = get_user_tasks(session, user.id)

    # Refresh the mapping
    result = mapping_service.refresh_mapping(tasks, str(user.id))

    return result


@router.post("/mapping/resolve")
def resolve_display_index(
    display_index: int,
    current_user: Annotated[TokenData, Depends(get_current_user)],
    session: Annotated[Session, Depends(get_session)]
):
    """
    Resolve a display index to its corresponding task ID.
    """
    # Get the user from the database to ensure they exist
    user = session.exec(select(User).where(User.email == current_user.email)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Get all tasks for the user to validate the mapping
    tasks = get_user_tasks(session, user.id)

    # Validate the display index
    is_valid, error_msg = mapping_service.validate_display_index(str(user.id), display_index, tasks)

    if not is_valid:
        return {
            "task_id": None,
            "display_index": display_index,
            "valid": False,
            "error": error_msg
        }

    # Resolve the display index to task_id
    task_id = mapping_service.resolve_display_index(str(user.id), display_index)

    return {
        "task_id": task_id,
        "display_index": display_index,
        "valid": task_id is not None,
        "error": None if task_id else "Task not found for display index"
    }


@router.get("/tasks/display/{display_index}")
def get_task_by_display_index(
    display_index: int,
    current_user: Annotated[TokenData, Depends(get_current_user)],
    session: Annotated[Session, Depends(get_session)]
):
    """
    Retrieve a specific task by its display index (1-based).
    """
    # Get the user from the database to ensure they exist
    user = session.exec(select(User).where(User.email == current_user.email)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Get all tasks for the user to validate the mapping
    tasks = get_user_tasks(session, user.id)

    # Validate the display index
    is_valid, error_msg = mapping_service.validate_display_index(str(user.id), display_index, tasks)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error_msg
        )

    # Resolve the display index to task_id
    task_id = mapping_service.resolve_display_index(str(user.id), display_index)
    if not task_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task not found at display index {display_index}"
        )

    # Get the specific task
    task = get_task_by_id(session, int(task_id), user.id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task not found at display index {display_index}"
        )

    # Add display_index to the response
    task_dict = task.dict()
    task_dict["display_index"] = display_index
    from ..schemas.task import TaskReadWithDisplayIndex
    return TaskReadWithDisplayIndex(**task_dict)


@router.put("/tasks/display/{display_index}")
def update_task_by_display_index(
    display_index: int,
    task_update: TaskUpdate,
    current_user: Annotated[TokenData, Depends(get_current_user)],
    session: Annotated[Session, Depends(get_session)]
):
    """
    Update an existing task using its display index.
    """
    # Get the user from the database to ensure they exist
    user = session.exec(select(User).where(User.email == current_user.email)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Get all tasks for the user to validate the mapping
    tasks = get_user_tasks(session, user.id)

    # Validate the display index
    is_valid, error_msg = mapping_service.validate_display_index(str(user.id), display_index, tasks)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error_msg
        )

    # Resolve the display index to task_id
    task_id = mapping_service.resolve_display_index(str(user.id), display_index)
    if not task_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task not found at display index {display_index}"
        )

    # Update the task
    updated_task = update_task(session, int(task_id), task_update, user.id)
    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task not found at display index {display_index}"
        )

    # Add display_index to the response
    task_dict = updated_task.dict()
    task_dict["display_index"] = display_index
    from ..schemas.task import TaskReadWithDisplayIndex
    return TaskReadWithDisplayIndex(**task_dict)


@router.delete("/tasks/display/{display_index}")
def delete_task_by_display_index(
    display_index: int,
    current_user: Annotated[TokenData, Depends(get_current_user)],
    session: Annotated[Session, Depends(get_session)]
):
    """
    Delete a specific task by its display index.
    """
    # Get the user from the database to ensure they exist
    user = session.exec(select(User).where(User.email == current_user.email)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Get all tasks for the user to validate the mapping
    tasks = get_user_tasks(session, user.id)

    # Validate the display index
    is_valid, error_msg = mapping_service.validate_display_index(str(user.id), display_index, tasks)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error_msg
        )

    # Resolve the display index to task_id
    task_id = mapping_service.resolve_display_index(str(user.id), display_index)
    if not task_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task not found at display index {display_index}"
        )

    # Delete the task
    deleted = delete_task(session, int(task_id), user.id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task not found at display index {display_index}"
        )

    # After deletion, refresh the mapping for this user
    mapping_service.refresh_mapping(get_user_tasks(session, user.id), str(user.id))

    return {"message": f"Task at display index {display_index} deleted successfully"}


@router.patch("/tasks/display/{display_index}/completion")
def toggle_task_completion_by_display_index(
    display_index: int,
    task_update: TaskUpdateStatus,
    current_user: Annotated[TokenData, Depends(get_current_user)],
    session: Annotated[Session, Depends(get_session)]
):
    """
    Toggle the completion status of a task using its display index.
    """
    # Get the user from the database to ensure they exist
    user = session.exec(select(User).where(User.email == current_user.email)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Get all tasks for the user to validate the mapping
    tasks = get_user_tasks(session, user.id)

    # Validate the display index
    is_valid, error_msg = mapping_service.validate_display_index(str(user.id), display_index, tasks)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error_msg
        )

    # Resolve the display index to task_id
    task_id = mapping_service.resolve_display_index(str(user.id), display_index)
    if not task_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task not found at display index {display_index}"
        )

    # Update the task status
    updated_task = update_task_status(session, int(task_id), task_update.completed, user.id)
    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task not found at display index {display_index}"
        )

    # Add display_index to the response
    task_dict = updated_task.dict()
    task_dict["display_index"] = display_index
    from ..schemas.task import TaskReadWithDisplayIndex
    return TaskReadWithDisplayIndex(**task_dict)