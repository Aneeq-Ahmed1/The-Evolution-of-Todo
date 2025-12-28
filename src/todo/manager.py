"""
TaskManager for the In-Memory Todo Console Application
Manages in-memory storage and operations for tasks
"""

from .models import Task
import json
import os
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import atexit


class TaskManager:
    """
    Manages in-memory collection of Task entities with auto-increment IDs
    and 24-hour expiration functionality. Uses a user-specific data file
    to maintain state between CLI commands while preserving the "in-memory" concept.
    """

    def __init__(self, expiration_hours: int = 24):
        self.expiration_hours = expiration_hours
        # Use a file in the user's home directory to persist data between CLI calls
        home_dir = os.path.expanduser("~")
        self.data_file = os.path.join(home_dir, ".todo_app_data.json")
        self.load_state()

        # Note: File-based persistence is used to maintain state between CLI commands
        # The file will be manually cleaned up by users when needed or by the system periodically

    def _cleanup_on_exit(self):
        """Clean up the temporary data file on exit"""
        try:
            if os.path.exists(self.data_file):
                os.remove(self.data_file)
        except:
            pass  # Ignore cleanup errors

    def cleanup_data_file(self):
        """Manually clean up the data file - for user-initiated cleanup"""
        try:
            if os.path.exists(self.data_file):
                os.remove(self.data_file)
                return True
        except:
            pass  # Ignore cleanup errors
        return False

    def load_state(self):
        """Load tasks from the temporary file if it exists"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.tasks: Dict[int, Task] = {}
                    for task_data in data['tasks']:
                        task = Task(
                            id=task_data['id'],
                            title=task_data['title'],
                            description=task_data.get('description'),
                            completed=task_data.get('completed', False),
                            created_at=datetime.fromisoformat(task_data['created_at']),
                            last_accessed=datetime.fromisoformat(task_data['last_accessed'])
                        )
                        self.tasks[task.id] = task
                    self.next_id = data.get('next_id', 1)
            except:
                # If there's an error loading, start fresh
                self.tasks = {}
                self.next_id = 1
        else:
            self.tasks = {}
            self.next_id = 1

    def save_state(self):
        """Save tasks to the data file"""
        try:
            tasks_data = []
            for task in self.tasks.values():
                task_dict = {
                    'id': task.id,
                    'title': task.title,
                    'description': task.description,
                    'completed': task.completed,
                    'created_at': task.created_at.isoformat(),
                    'last_accessed': task.last_accessed.isoformat()
                }
                tasks_data.append(task_dict)

            data = {
                'tasks': tasks_data,
                'next_id': self.next_id
            }

            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            # If there's an error saving, print the error for debugging
            print(f"Error saving state: {e}", file=sys.stderr)
            pass

    def _cleanup_expired_tasks(self):
        """Remove tasks that have been inactive for more than expiration_hours"""
        current_time = datetime.now()
        expired_ids = []

        for task_id, task in self.tasks.items():
            if current_time - task.last_accessed > timedelta(hours=self.expiration_hours):
                expired_ids.append(task_id)

        for task_id in expired_ids:
            del self.tasks[task_id]

    def _update_task_access_time(self, task_id: int):
        """Update the last_accessed time for a task"""
        if task_id in self.tasks:
            self.tasks[task_id].last_accessed = datetime.now()

    def add_task(self, title: str, description: Optional[str] = None) -> Task:
        """
        Add a new task with validation
        """
        # Clean up expired tasks first
        self._cleanup_expired_tasks()

        # Create task with next available ID
        task = Task(
            id=self.next_id,
            title=title,
            description=description,
            completed=False
        )

        # Validate the task
        task.validate()

        # Add to storage
        self.tasks[self.next_id] = task

        # Increment next ID for future tasks
        self.next_id += 1

        # Save state
        self.save_state()

        return task

    def list_tasks(self) -> List[Task]:
        """
        Return all tasks
        """
        # Clean up expired tasks first
        self._cleanup_expired_tasks()

        # Update access time for all tasks (as they are being accessed)
        for task_id in self.tasks.keys():
            self._update_task_access_time(task_id)

        # Save state
        self.save_state()

        # Return all tasks
        return list(self.tasks.values())

    def get_task(self, task_id: int) -> Optional[Task]:
        """
        Get a specific task by ID
        """
        # Clean up expired tasks first
        self._cleanup_expired_tasks()

        if task_id in self.tasks:
            self._update_task_access_time(task_id)
            return self.tasks[task_id]
        return None

    def update_task(self, task_id: int, new_title: Optional[str] = None,
                   new_description: Optional[str] = None) -> Optional[Task]:
        """
        Update an existing task
        """
        task = self.get_task(task_id)
        if not task:
            return None

        # Update fields if provided
        if new_title is not None:
            task.title = new_title
        if new_description is not None:
            task.description = new_description

        # Validate the updated task
        task.validate()

        # Save state
        self.save_state()

        return task

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by ID
        """
        task = self.get_task(task_id)
        if not task:
            return False

        del self.tasks[task_id]

        # Save state
        self.save_state()

        return True

    def toggle_completion(self, task_id: int, completed: bool) -> bool:
        """
        Toggle task completion status
        """
        task = self.get_task(task_id)
        if not task:
            return False

        task.completed = completed

        # Save state
        self.save_state()

        return True

    def export_tasks(self) -> str:
        """
        Export all tasks to JSON format
        """
        # Clean up expired tasks first
        self._cleanup_expired_tasks()

        # Prepare tasks for JSON serialization
        tasks_data = []
        for task in self.tasks.values():
            task_dict = {
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'completed': task.completed,
                'created_at': task.created_at.isoformat(),
                'last_accessed': task.last_accessed.isoformat()
            }
            tasks_data.append(task_dict)

        # Save state
        self.save_state()

        return json.dumps(tasks_data, indent=2)

    def import_tasks(self, file_path: str):
        """
        Import tasks from a JSON file
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            tasks_data = json.load(f)

        for task_data in tasks_data:
            # Create task from imported data
            task = Task(
                id=task_data['id'],
                title=task_data['title'],
                description=task_data.get('description'),
                completed=task_data.get('completed', False),
                created_at=datetime.fromisoformat(task_data['created_at']),
                last_accessed=datetime.fromisoformat(task_data['last_accessed'])
            )

            # Validate the task before adding
            task.validate()

            # Add to storage
            self.tasks[task.id] = task

            # Update next_id if necessary
            if task.id >= self.next_id:
                self.next_id = task.id + 1

        # Save state
        self.save_state()