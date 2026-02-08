"""
Task service for database operations with advanced features.
"""
from sqlmodel import Session, select, or_, col
from typing import List, Optional
from datetime import datetime, timedelta
from ..models.task import Task
from ..schemas.task import TaskCreate, TaskUpdate


def get_user_tasks(
    session: Session,
    user_id: int,
    search: Optional[str] = None,
    priority: Optional[str] = None,
    category: Optional[str] = None,
    completed: Optional[bool] = None,
    sort_by: str = "created_at",
    sort_order: str = "desc"
) -> List[Task]:
    """
    Retrieve all tasks for a specific user with search, filter, and sort.
    """
    # Base query
    query = select(Task).where(Task.user_id == user_id)

    # Search filter (case-insensitive search in title and description)
    if search:
        search_pattern = f"%{search}%"
        query = query.where(
            or_(
                Task.title.ilike(search_pattern),
                Task.description.ilike(search_pattern)
            )
        )

    # Priority filter
    if priority and priority != "all":
        query = query.where(Task.priority == priority)

    # Category filter
    if category and category != "all":
        query = query.where(Task.category == category)

    # Completed status filter
    if completed is not None:
        query = query.where(Task.completed == completed)

    # Sorting
    sort_column = {
        "created_at": Task.created_at,
        "due_date": Task.due_date,
        "priority": Task.priority,
        "title": Task.title,
        "updated_at": Task.updated_at
    }.get(sort_by, Task.created_at)

    if sort_order == "asc":
        query = query.order_by(sort_column.asc())
    else:
        query = query.order_by(sort_column.desc())

    tasks = session.exec(query).all()
    return tasks


def get_task_by_id(session: Session, task_id: int, user_id: int) -> Optional[Task]:
    """
    Retrieve a specific task by ID for a specific user.
    """
    task = session.get(Task, task_id)
    if task and task.user_id == user_id:
        return task
    return None


def create_task(session: Session, task_create: TaskCreate, user_id: int) -> Task:
    """
    Create a new task for a specific user with all advanced fields.
    """
    # Calculate next occurrence for recurring tasks
    next_occurrence = None
    if task_create.is_recurring and task_create.due_date:
        next_occurrence = calculate_next_occurrence(
            task_create.due_date,
            task_create.recurrence_pattern,
            task_create.recurrence_interval or 1
        )

    db_task = Task(
        title=task_create.title,
        description=task_create.description,
        completed=task_create.completed,
        user_id=user_id,
        # Intermediate fields
        priority=task_create.priority or "medium",
        tags=task_create.tags,
        category=task_create.category,
        # Advanced fields
        due_date=task_create.due_date,
        due_time=task_create.due_time,
        is_recurring=task_create.is_recurring or False,
        recurrence_pattern=task_create.recurrence_pattern,
        recurrence_interval=task_create.recurrence_interval or 1,
        next_occurrence=next_occurrence
    )
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


def update_task(session: Session, task_id: int, task_update: TaskUpdate, user_id: int) -> Optional[Task]:
    """
    Update a specific task by ID for a specific user.
    """
    db_task = session.get(Task, task_id)
    if not db_task or db_task.user_id != user_id:
        return None

    # Update basic fields
    if task_update.title is not None:
        db_task.title = task_update.title
    if task_update.description is not None:
        db_task.description = task_update.description
    if task_update.completed is not None:
        db_task.completed = task_update.completed

    # Update intermediate fields
    if task_update.priority is not None:
        db_task.priority = task_update.priority
    if task_update.tags is not None:
        db_task.tags = task_update.tags
    if task_update.category is not None:
        db_task.category = task_update.category

    # Update advanced fields
    if task_update.due_date is not None:
        db_task.due_date = task_update.due_date
    if task_update.due_time is not None:
        db_task.due_time = task_update.due_time
    if task_update.is_recurring is not None:
        db_task.is_recurring = task_update.is_recurring
    if task_update.recurrence_pattern is not None:
        db_task.recurrence_pattern = task_update.recurrence_pattern
    if task_update.recurrence_interval is not None:
        db_task.recurrence_interval = task_update.recurrence_interval

    # Recalculate next occurrence if recurring settings changed
    if db_task.is_recurring and db_task.due_date:
        db_task.next_occurrence = calculate_next_occurrence(
            db_task.due_date,
            db_task.recurrence_pattern,
            db_task.recurrence_interval or 1
        )

    db_task.updated_at = datetime.now()

    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


def delete_task(session: Session, task_id: int, user_id: int) -> bool:
    """
    Delete a specific task by ID for a specific user.
    """
    db_task = session.get(Task, task_id)
    if not db_task or db_task.user_id != user_id:
        return False

    session.delete(db_task)
    session.commit()
    return True


def update_task_status(session: Session, task_id: int, completed: bool, user_id: int) -> Optional[Task]:
    """
    Update the completion status of a specific task.
    Handle recurring tasks by creating next occurrence.
    """
    db_task = session.get(Task, task_id)
    if not db_task or db_task.user_id != user_id:
        return None

    # If marking recurring task as complete, create next occurrence
    if completed and db_task.is_recurring and not db_task.completed:
        create_recurring_task_instance(session, db_task, user_id)

    db_task.completed = completed
    db_task.updated_at = datetime.now()

    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


def calculate_next_occurrence(
    due_date: datetime,
    pattern: Optional[str],
    interval: int = 1
) -> Optional[datetime]:
    """
    Calculate the next occurrence date for a recurring task.
    """
    if not pattern or not due_date:
        return None

    if pattern == "daily":
        return due_date + timedelta(days=interval)
    elif pattern == "weekly":
        return due_date + timedelta(weeks=interval)
    elif pattern == "monthly":
        # Add months (approximate - 30 days per month)
        return due_date + timedelta(days=30 * interval)

    return None


def create_recurring_task_instance(session: Session, original_task: Task, user_id: int) -> Task:
    """
    Create a new instance of a recurring task with updated due date.
    """
    if not original_task.is_recurring or not original_task.due_date:
        return original_task

    next_due_date = calculate_next_occurrence(
        original_task.due_date,
        original_task.recurrence_pattern,
        original_task.recurrence_interval or 1
    )

    if not next_due_date:
        return original_task

    # Create new task instance
    new_task = Task(
        title=original_task.title,
        description=original_task.description,
        completed=False,
        user_id=user_id,
        priority=original_task.priority,
        tags=original_task.tags,
        category=original_task.category,
        due_date=next_due_date,
        due_time=original_task.due_time,
        is_recurring=True,
        recurrence_pattern=original_task.recurrence_pattern,
        recurrence_interval=original_task.recurrence_interval,
        next_occurrence=calculate_next_occurrence(
            next_due_date,
            original_task.recurrence_pattern,
            original_task.recurrence_interval or 1
        )
    )

    session.add(new_task)
    session.commit()
    session.refresh(new_task)
    return new_task


def get_upcoming_tasks(session: Session, user_id: int, hours: int = 24) -> List[Task]:
    """
    Get tasks due within the next specified hours.
    Used for notifications.
    """
    now = datetime.now()
    future = now + timedelta(hours=hours)

    tasks = session.exec(
        select(Task).where(
            Task.user_id == user_id,
            Task.completed == False,
            Task.due_date != None,
            Task.due_date >= now,
            Task.due_date <= future
        ).order_by(Task.due_date.asc())
    ).all()

    return tasks


def get_overdue_tasks(session: Session, user_id: int) -> List[Task]:
    """
    Get tasks that are past their due date and not completed.
    """
    now = datetime.now()

    tasks = session.exec(
        select(Task).where(
            Task.user_id == user_id,
            Task.completed == False,
            Task.due_date != None,
            Task.due_date < now
        ).order_by(Task.due_date.asc())
    ).all()

    return tasks


def get_user_tasks_with_display_index(
    session: Session,
    user_id: int,
    search: Optional[str] = None,
    priority: Optional[str] = None,
    category: Optional[str] = None,
    completed: Optional[bool] = None,
    sort_by: str = "created_at",
    sort_order: str = "desc"
):
    """
    Retrieve all tasks for a specific user with display indices for ordinal reference mapping.
    Returns both the tasks with display indices and the mapping information.
    """
    from ..services.mapping_service import mapping_service

    # Get tasks using the existing function
    tasks = get_user_tasks(
        session=session,
        user_id=user_id,
        search=search,
        priority=priority,
        category=category,
        completed=completed,
        sort_by=sort_by,
        sort_order=sort_order
    )

    # Generate display indices for the tasks
    tasks_with_display = mapping_service.get_task_with_display_index(tasks, str(user_id))

    # Generate mapping information
    display_mapping = mapping_service.generate_display_mapping(tasks, str(user_id))

    return {
        "tasks": tasks_with_display,
        "display_mapping": display_mapping
    }
