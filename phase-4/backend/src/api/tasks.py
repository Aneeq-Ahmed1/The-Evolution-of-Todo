"""
Task API endpoints for managing user tasks.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlmodel import Session, select
from typing import Annotated, Dict, Optional
from datetime import datetime
from ..database import get_session
from ..models.user import User
from ..models.task import Task
from ..schemas.task import TaskCreate, TaskUpdate, TaskRead, TaskListResponse, TaskUpdateStatus, TaskListWithDisplayResponse, TaskReadWithDisplayIndex
from ..auth.middleware import get_current_user
from ..schemas.auth import TokenData
from ..services.task_service import (
    get_user_tasks,
    get_task_by_id,
    create_task,
    update_task,
    delete_task,
    update_task_status,
    get_upcoming_tasks,
    get_overdue_tasks,
    get_user_tasks_with_display_index
)


router = APIRouter()


@router.get("/tasks", response_model=list[TaskRead])
def get_tasks(
    current_user: Annotated[TokenData, Depends(get_current_user)],
    session: Annotated[Session, Depends(get_session)],
    search: Optional[str] = None,
    priority: Optional[str] = None,
    category: Optional[str] = None,
    completed: Optional[bool] = None,
    sort_by: Optional[str] = "created_at",
    sort_order: Optional[str] = "desc"
):
    """
    Retrieve all tasks for the authenticated user with search, filter, and sort.

    Query Parameters:
    - search: Search in title and description
    - priority: Filter by priority (low, medium, high)
    - category: Filter by category
    - completed: Filter by completion status
    - sort_by: Sort field (created_at, due_date, priority, title)
    - sort_order: asc or desc
    """
    import logging
    logger = logging.getLogger(__name__)

    logger.info(f"Fetching tasks for user: {current_user.email}")

    # Get the user from the database to ensure they exist
    user = session.exec(select(User).where(User.email == current_user.email)).first()
    if not user:
        logger.error(f"User not found in database: {current_user.email}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    logger.info(f"Found user {user.email} with ID {user.id}")

    # Retrieve tasks for the authenticated user with filters and sorting
    tasks = get_user_tasks(
        session=session,
        user_id=user.id,
        search=search,
        priority=priority,
        category=category,
        completed=completed,
        sort_by=sort_by,
        sort_order=sort_order
    )
    logger.info(f"Retrieved {len(tasks)} tasks for user {user.email}")
    return tasks


@router.get("/tasks-with-display")
def get_tasks_with_display_index(
    current_user: Annotated[TokenData, Depends(get_current_user)],
    session: Annotated[Session, Depends(get_session)],
    search: Optional[str] = None,
    priority: Optional[str] = None,
    category: Optional[str] = None,
    completed: Optional[bool] = None,
    sort_by: Optional[str] = "created_at",
    sort_order: Optional[str] = "desc"
):
    """
    Retrieve all tasks for the authenticated user with display indices for ordinal reference mapping.

    Query Parameters:
    - search: Search in title and description
    - priority: Filter by priority (low, medium, high)
    - category: Filter by category
    - completed: Filter by completion status
    - sort_by: Sort field (created_at, due_date, priority, title)
    - sort_order: asc or desc

    Response includes:
    - tasks: List of tasks with display_index field
    - display_mapping: List of {display_index, task_id} mappings for ordinal references
    """
    import logging
    logger = logging.getLogger(__name__)

    logger.info(f"Fetching tasks with display indices for user: {current_user.email}")

    # Get the user from the database to ensure they exist
    user = session.exec(select(User).where(User.email == current_user.email)).first()
    if not user:
        logger.error(f"User not found in database: {current_user.email}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    logger.info(f"Found user {user.email} with ID {user.id}")

    # Retrieve tasks with display indices for the authenticated user with filters and sorting
    try:
        result = get_user_tasks_with_display_index(
            session=session,
            user_id=user.id,
            search=search,
            priority=priority,
            category=category,
            completed=completed,
            sort_by=sort_by,
            sort_order=sort_order
        )
        logger.info(f"Retrieved {len(result['tasks'])} tasks with display indices for user {user.email}")
        return result
    except Exception as e:
        logger.error(f"Error in get_tasks_with_display_index: {e}")
        import traceback
        traceback.print_exc()
        raise


@router.post("/tasks", response_model=TaskRead)
def create_task_endpoint(
    task: TaskCreate,
    current_user: Annotated[TokenData, Depends(get_current_user)],
    session: Annotated[Session, Depends(get_session)]
):
    """
    Create a new task for the authenticated user.
    """
    import logging
    logger = logging.getLogger(__name__)

    logger.info(f"Creating task for user: {current_user.email}")

    # Get the user from the database to ensure they exist
    user = session.exec(select(User).where(User.email == current_user.email)).first()
    if not user:
        logger.error(f"User not found in database: {current_user.email}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    logger.info(f"Found user {user.email} with ID {user.id}")

    # Create the task using the service
    db_task = create_task(session, task, user.id)
    logger.info(f"Created task with ID {db_task.id} for user {user.email}")
    return db_task


@router.get("/tasks/{task_id}", response_model=TaskRead)
def get_task(
    task_id: int,
    current_user: Annotated[TokenData, Depends(get_current_user)],
    session: Annotated[Session, Depends(get_session)]
):
    """
    Retrieve a specific task by ID for the authenticated user.
    """
    # Get the user from the database to ensure they exist
    user = session.exec(select(User).where(User.email == current_user.email)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Retrieve the specific task for the authenticated user using the service
    task = get_task_by_id(session, task_id, user.id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task


@router.put("/tasks/{task_id}", response_model=TaskRead)
def update_task_endpoint(
    task_id: int,
    task_update: TaskUpdate,
    current_user: Annotated[TokenData, Depends(get_current_user)],
    session: Annotated[Session, Depends(get_session)]
):
    """
    Update a specific task by ID for the authenticated user.
    """
    # Get the user from the database to ensure they exist
    user = session.exec(select(User).where(User.email == current_user.email)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Update the task using the service
    updated_task = update_task(session, task_id, task_update, user.id)
    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return updated_task


from typing import Dict, Any

@router.delete("/tasks/{task_id}", response_model=Dict[str, str])
def delete_task_endpoint(
    task_id: int,
    current_user: Annotated[TokenData, Depends(get_current_user)],
    session: Annotated[Session, Depends(get_session)]
):
    """
    Delete a specific task by ID for the authenticated user.
    """
    # Get the user from the database to ensure they exist
    user = session.exec(select(User).where(User.email == current_user.email)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Delete the task using the service
    deleted = delete_task(session, task_id, user.id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return JSONResponse(content={"message": "Task deleted successfully"}, status_code=200)


@router.patch("/tasks/{task_id}", response_model=TaskRead)
def update_task_status_endpoint(
    task_id: int,
    task_update: TaskUpdateStatus,
    current_user: Annotated[TokenData, Depends(get_current_user)],
    session: Annotated[Session, Depends(get_session)]
):
    """
    Update the completion status of a specific task by ID for the authenticated user.
    """
    # Get the user from the database to ensure they exist
    user = session.exec(select(User).where(User.email == current_user.email)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Update the task status using the service
    updated_task = update_task_status(session, task_id, task_update.completed, user.id)
    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return updated_task