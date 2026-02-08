"""
Todo Agent for AI Task Display Mapping

This agent handles user commands for task management with support for
ordinal task references (e.g., "task 1 is complete", "edit task 2").

The agent integrates:
- Intent Parser: Understands user commands
- Ordinal Resolver: Parses task number references
- Task Resolver: Maps display indices to internal task IDs
- Backend API: Executes task operations
"""
import requests
from typing import Dict, Any, Optional, List
from ..services.intent_parser import (
    get_intent_parser,
    TaskIntent,
    parse_user_command
)
from ..services.ordinal_resolver import normalize_ordinal_to_number
from ..services.task_resolver import get_resolver as get_task_resolver


class TodoAgent:
    """
    AI Agent for task management with ordinal reference support.

    The agent processes natural language commands and executes task operations
    using display indices instead of internal task IDs.
    """

    def __init__(self, api_base_url: str, auth_token: Optional[str] = None):
        """
        Initialize Todo Agent.

        Args:
            api_base_url: Base URL for backend API (e.g., "http://localhost:8000")
            auth_token: JWT authentication token
        """
        self.api_base_url = api_base_url.rstrip('/')
        self.auth_token = auth_token
        self.intent_parser = get_intent_parser()
        self.task_resolver = get_task_resolver()

    def set_auth_token(self, token: str) -> None:
        """Set JWT authentication token."""
        self.auth_token = token

    def _get_headers(self) -> Dict[str, str]:
        """Get HTTP headers with authentication."""
        headers = {"Content-Type": "application/json"}
        if self.auth_token:
            headers["Authorization"] = f"Bearer {self.auth_token}"
        return headers

    def process_command(self, user_input: str) -> Dict[str, Any]:
        """
        Process user command and execute appropriate action.

        Args:
            user_input: Natural language command from user

        Returns:
            Response dictionary with:
                - success: bool
                - message: str
                - data: Optional[Any]
                - intent: str
                - display_index: Optional[int]

        Examples:
            >>> agent = TodoAgent("http://localhost:8000", token="...")
            >>> agent.process_command("task 1 is complete")
            {'success': True, 'message': 'Task completed successfully', ...}

            >>> agent.process_command("edit task 2")
            {'success': True, 'message': 'What would you like to change?', ...}
        """
        # Parse user command
        parsed = parse_user_command(user_input)
        intent = parsed['intent']
        display_index = parsed['display_index']
        confidence = parsed['confidence']

        # Route to appropriate handler based on intent
        if intent == TaskIntent.COMPLETE_TASK:
            return self._handle_complete_task(display_index, user_input)

        elif intent == TaskIntent.UNCOMPLETE_TASK:
            return self._handle_uncomplete_task(display_index, user_input)

        elif intent == TaskIntent.EDIT_TASK:
            return self._handle_edit_task(display_index, user_input)

        elif intent == TaskIntent.DELETE_TASK:
            return self._handle_delete_task(display_index, user_input)

        elif intent == TaskIntent.GET_TASK:
            return self._handle_get_task(display_index, user_input)

        elif intent == TaskIntent.LIST_TASKS:
            return self._handle_list_tasks(user_input)

        elif intent == TaskIntent.CREATE_TASK:
            return self._handle_create_task(user_input)

        else:
            return {
                'success': False,
                'message': "I'm not sure what you'd like me to do. Try commands like 'task 1 is complete' or 'list tasks'.",
                'data': None,
                'intent': intent.value,
                'display_index': display_index,
                'confidence': confidence
            }

    def _handle_complete_task(self, display_index: Optional[int], user_input: str) -> Dict[str, Any]:
        """Handle task completion by display index."""
        if display_index is None:
            return {
                'success': False,
                'message': "Which task would you like to mark as complete? Please specify a task number (e.g., 'task 1 is complete').",
                'data': None,
                'intent': 'complete_task',
                'display_index': None
            }

        # Validate display index with task resolver
        if not self.task_resolver.validate_index_range(display_index):
            error_msg = self.task_resolver.generate_error_message(display_index)
            return {
                'success': False,
                'message': error_msg,
                'data': None,
                'intent': 'complete_task',
                'display_index': display_index
            }

        # Call backend API to toggle completion
        try:
            response = requests.patch(
                f"{self.api_base_url}/tasks/display/{display_index}/completion",
                json={"completed": True},
                headers=self._get_headers()
            )

            if response.status_code == 200:
                task = response.json()
                return {
                    'success': True,
                    'message': f"✓ Task {display_index} marked as complete: {task.get('title', '')}",
                    'data': task,
                    'intent': 'complete_task',
                    'display_index': display_index
                }
            else:
                return {
                    'success': False,
                    'message': f"Failed to complete task: {response.json().get('detail', 'Unknown error')}",
                    'data': None,
                    'intent': 'complete_task',
                    'display_index': display_index
                }

        except Exception as e:
            return {
                'success': False,
                'message': f"Error completing task: {str(e)}",
                'data': None,
                'intent': 'complete_task',
                'display_index': display_index
            }

    def _handle_uncomplete_task(self, display_index: Optional[int], user_input: str) -> Dict[str, Any]:
        """Handle marking task as incomplete by display index."""
        if display_index is None:
            return {
                'success': False,
                'message': "Which task would you like to mark as incomplete? Please specify a task number.",
                'data': None,
                'intent': 'uncomplete_task',
                'display_index': None
            }

        if not self.task_resolver.validate_index_range(display_index):
            error_msg = self.task_resolver.generate_error_message(display_index)
            return {
                'success': False,
                'message': error_msg,
                'data': None,
                'intent': 'uncomplete_task',
                'display_index': display_index
            }

        try:
            response = requests.patch(
                f"{self.api_base_url}/tasks/display/{display_index}/completion",
                json={"completed": False},
                headers=self._get_headers()
            )

            if response.status_code == 200:
                task = response.json()
                return {
                    'success': True,
                    'message': f"Task {display_index} marked as incomplete: {task.get('title', '')}",
                    'data': task,
                    'intent': 'uncomplete_task',
                    'display_index': display_index
                }
            else:
                return {
                    'success': False,
                    'message': f"Failed to uncomplete task: {response.json().get('detail', 'Unknown error')}",
                    'data': None,
                    'intent': 'uncomplete_task',
                    'display_index': display_index
                }

        except Exception as e:
            return {
                'success': False,
                'message': f"Error: {str(e)}",
                'data': None,
                'intent': 'uncomplete_task',
                'display_index': display_index
            }

    def _handle_edit_task(self, display_index: Optional[int], user_input: str) -> Dict[str, Any]:
        """Handle task editing by display index."""
        if display_index is None:
            return {
                'success': False,
                'message': "Which task would you like to edit? Please specify a task number (e.g., 'edit task 2').",
                'data': None,
                'intent': 'edit_task',
                'display_index': None
            }

        if not self.task_resolver.validate_index_range(display_index):
            error_msg = self.task_resolver.generate_error_message(display_index)
            return {
                'success': False,
                'message': error_msg,
                'data': None,
                'intent': 'edit_task',
                'display_index': display_index
            }

        # Get current task details
        try:
            response = requests.get(
                f"{self.api_base_url}/tasks/display/{display_index}",
                headers=self._get_headers()
            )

            if response.status_code == 200:
                task = response.json()
                return {
                    'success': True,
                    'message': f"What would you like to change about task {display_index} ('{task.get('title', '')}')? You can say something like 'change the title to...' or 'update the description to...'",
                    'data': task,
                    'intent': 'edit_task',
                    'display_index': display_index,
                    'awaiting_details': True
                }
            else:
                return {
                    'success': False,
                    'message': f"Task {display_index} not found",
                    'data': None,
                    'intent': 'edit_task',
                    'display_index': display_index
                }

        except Exception as e:
            return {
                'success': False,
                'message': f"Error: {str(e)}",
                'data': None,
                'intent': 'edit_task',
                'display_index': display_index
            }

    def _handle_delete_task(self, display_index: Optional[int], user_input: str) -> Dict[str, Any]:
        """Handle task deletion by display index."""
        if display_index is None:
            return {
                'success': False,
                'message': "Which task would you like to delete? Please specify a task number (e.g., 'delete task 3').",
                'data': None,
                'intent': 'delete_task',
                'display_index': None
            }

        if not self.task_resolver.validate_index_range(display_index):
            error_msg = self.task_resolver.generate_error_message(display_index)
            return {
                'success': False,
                'message': error_msg,
                'data': None,
                'intent': 'delete_task',
                'display_index': display_index
            }

        try:
            response = requests.delete(
                f"{self.api_base_url}/tasks/display/{display_index}",
                headers=self._get_headers()
            )

            if response.status_code == 200:
                return {
                    'success': True,
                    'message': f"✓ Task {display_index} deleted successfully",
                    'data': None,
                    'intent': 'delete_task',
                    'display_index': display_index
                }
            else:
                return {
                    'success': False,
                    'message': f"Failed to delete task: {response.json().get('detail', 'Unknown error')}",
                    'data': None,
                    'intent': 'delete_task',
                    'display_index': display_index
                }

        except Exception as e:
            return {
                'success': False,
                'message': f"Error: {str(e)}",
                'data': None,
                'intent': 'delete_task',
                'display_index': display_index
            }

    def _handle_get_task(self, display_index: Optional[int], user_input: str) -> Dict[str, Any]:
        """Handle retrieving specific task by display index."""
        if display_index is None:
            return {
                'success': False,
                'message': "Which task would you like to see? Please specify a task number.",
                'data': None,
                'intent': 'get_task',
                'display_index': None
            }

        if not self.task_resolver.validate_index_range(display_index):
            error_msg = self.task_resolver.generate_error_message(display_index)
            return {
                'success': False,
                'message': error_msg,
                'data': None,
                'intent': 'get_task',
                'display_index': display_index
            }

        try:
            response = requests.get(
                f"{self.api_base_url}/tasks/display/{display_index}",
                headers=self._get_headers()
            )

            if response.status_code == 200:
                task = response.json()
                status = "✓ Complete" if task.get('completed') else "○ Pending"
                message = f"Task {display_index}: {task.get('title', '')} [{status}]"
                if task.get('description'):
                    message += f"\nDescription: {task['description']}"

                return {
                    'success': True,
                    'message': message,
                    'data': task,
                    'intent': 'get_task',
                    'display_index': display_index
                }
            else:
                return {
                    'success': False,
                    'message': f"Task {display_index} not found",
                    'data': None,
                    'intent': 'get_task',
                    'display_index': display_index
                }

        except Exception as e:
            return {
                'success': False,
                'message': f"Error: {str(e)}",
                'data': None,
                'intent': 'get_task',
                'display_index': display_index
            }

    def _handle_list_tasks(self, user_input: str) -> Dict[str, Any]:
        """Handle listing all tasks."""
        try:
            response = requests.get(
                f"{self.api_base_url}/tasks-with-display",
                headers=self._get_headers()
            )

            if response.status_code == 200:
                data = response.json()
                tasks = data.get('tasks', [])

                if not tasks:
                    return {
                        'success': True,
                        'message': "You don't have any tasks yet. Create one to get started!",
                        'data': {'tasks': [], 'display_mapping': []},
                        'intent': 'list_tasks',
                        'display_index': None
                    }

                # Update task resolver with current mapping
                display_mapping = data.get('display_mapping', [])
                self.task_resolver.set_mapping(display_mapping, user_id="current")

                # Format task list
                task_list = []
                for task in tasks:
                    status = "✓" if task.get('completed') else "○"
                    display_idx = task.get('display_index', '?')
                    task_list.append(f"{display_idx}. {status} {task.get('title', '')}")

                message = f"You have {len(tasks)} tasks:\n" + "\n".join(task_list)

                return {
                    'success': True,
                    'message': message,
                    'data': data,
                    'intent': 'list_tasks',
                    'display_index': None
                }
            else:
                return {
                    'success': False,
                    'message': f"Failed to list tasks: {response.json().get('detail', 'Unknown error')}",
                    'data': None,
                    'intent': 'list_tasks',
                    'display_index': None
                }

        except Exception as e:
            return {
                'success': False,
                'message': f"Error: {str(e)}",
                'data': None,
                'intent': 'list_tasks',
                'display_index': None
            }

    def _handle_create_task(self, user_input: str) -> Dict[str, Any]:
        """Handle task creation (placeholder - needs title extraction)."""
        return {
            'success': False,
            'message': "To create a task, please tell me what you'd like to do. For example: 'add task: buy groceries'",
            'data': None,
            'intent': 'create_task',
            'display_index': None,
            'needs_clarification': True
        }

    def refresh_task_mapping(self, tasks: List[Dict[str, Any]], user_id: str) -> None:
        """
        Refresh the task resolver's display mapping.

        Call this when tasks are added, deleted, or reordered.

        Args:
            tasks: List of task dictionaries with 'display_index' and 'id' fields
            user_id: User identifier
        """
        mapping = [
            {'display_index': task.get('display_index'), 'task_id': task.get('id')}
            for task in tasks
        ]
        self.task_resolver.set_mapping(mapping, user_id)


# Convenience function
def create_agent(api_base_url: str, auth_token: Optional[str] = None) -> TodoAgent:
    """
    Create and return a TodoAgent instance.

    Args:
        api_base_url: Base URL for backend API
        auth_token: Optional JWT authentication token

    Returns:
        Configured TodoAgent instance

    Example:
        >>> agent = create_agent("http://localhost:8000", token="...")
        >>> result = agent.process_command("task 1 is complete")
    """
    return TodoAgent(api_base_url, auth_token)
