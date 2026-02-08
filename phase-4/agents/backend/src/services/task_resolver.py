"""
Task Resolver Service for AI Task Display Mapping

This service resolves display indices to internal task IDs and provides
error handling for invalid references.
"""
import logging
from typing import Optional, Dict, List, Tuple
from .ordinal_resolver import normalize_ordinal_to_number

logger = logging.getLogger(__name__)


class TaskResolver:
    """
    Resolves display indices to task IDs using runtime mapping.

    The resolver maintains a mapping between user-facing display indices (1, 2, 3...)
    and internal task IDs (UUIDs or database IDs).
    """

    def __init__(self):
        """Initialize empty display mapping"""
        self.display_mapping: Dict[int, str | int] = {}
        self.user_id: Optional[str | int] = None

    def set_mapping(self, mapping: List[Dict[str, any]], user_id: str | int) -> None:
        """
        Set the display index to task ID mapping.

        Args:
            mapping: List of {display_index: int, task_id: str|int} dictionaries
            user_id: User identifier for this mapping

        Example:
            resolver.set_mapping([
                {'display_index': 1, 'task_id': 'task-uuid-1'},
                {'display_index': 2, 'task_id': 'task-uuid-2'}
            ], 'user-123')
        """
        self.display_mapping = {
            item['display_index']: item['task_id']
            for item in mapping
        }
        self.user_id = user_id
        logger.info(f"Display mapping updated for user {user_id}: {len(mapping)} tasks")

    def resolve_display_index(self, display_index: int) -> Optional[str | int]:
        """
        Resolve display index to task ID.

        Args:
            display_index: Display index to resolve (1-based)

        Returns:
            Task ID if found, None otherwise

        Example:
            task_id = resolver.resolve_display_index(1)
            # Returns: 'task-uuid-1'
        """
        task_id = self.display_mapping.get(display_index)
        if task_id:
            logger.debug(f"Resolved display_index {display_index} to task_id {task_id}")
        else:
            logger.warning(f"Display_index {display_index} not found in mapping")
        return task_id

    def resolve_ordinal_reference(self, user_input: str) -> Tuple[Optional[int], Optional[str | int]]:
        """
        Parse ordinal reference from user input and resolve to task ID.

        Args:
            user_input: User's natural language command

        Returns:
            Tuple of (display_index, task_id) or (None, None) if not found

        Example:
            display_index, task_id = resolver.resolve_ordinal_reference("task 1 is complete")
            # Returns: (1, 'task-uuid-1')

            display_index, task_id = resolver.resolve_ordinal_reference("first task is complete")
            # Returns: (1, 'task-uuid-1')
        """
        # Extract display index from user input
        display_index = normalize_ordinal_to_number(user_input)

        if display_index is None:
            return (None, None)

        # Resolve to task ID
        task_id = self.resolve_display_index(display_index)

        return (display_index, task_id)

    def validate_index_range(self, display_index: int) -> bool:
        """
        Check if display index exists in current mapping.

        Args:
            display_index: Display index to validate (1-based)

        Returns:
            True if index exists, False otherwise

        Example:
            if resolver.validate_index_range(5):
                # Index 5 is valid
            else:
                # Index 5 is out of range
        """
        return display_index in self.display_mapping

    def get_task_count(self) -> int:
        """
        Get total number of tasks in current mapping.

        Returns:
            Number of tasks

        Example:
            count = resolver.get_task_count()
            # Returns: 5 (if 5 tasks are mapped)
        """
        return len(self.display_mapping)

    def get_all_indices(self) -> List[int]:
        """
        Get all valid display indices.

        Returns:
            Sorted list of display indices

        Example:
            indices = resolver.get_all_indices()
            # Returns: [1, 2, 3, 4, 5]
        """
        return sorted(self.display_mapping.keys())

    def generate_error_message(self, display_index: int) -> str:
        """
        Generate helpful error message for invalid display index.

        Args:
            display_index: Invalid display index that was referenced

        Returns:
            User-friendly error message

        Example:
            error = resolver.generate_error_message(10)
            # Returns: "You only have 5 tasks. Did you mean task 1, 2, 3, 4, or 5?"
        """
        task_count = self.get_task_count()

        if task_count == 0:
            return "You don't have any tasks yet. Create a task first!"

        if display_index < 1:
            return f"Task numbers start from 1. You have {task_count} tasks."

        if display_index == task_count + 1:
            return f"You only have {task_count} tasks. Did you mean task {task_count}?"

        valid_indices = self.get_all_indices()
        if task_count <= 5:
            # List all indices
            indices_str = ', '.join(str(i) for i in valid_indices)
            return f"You only have {task_count} tasks. Did you mean task {indices_str}?"
        else:
            # Show range
            return f"You have {task_count} tasks (numbered 1 to {task_count}). Task {display_index} doesn't exist."

    def get_task_count_message(self) -> str:
        """
        Get message describing current task count.

        Returns:
            Message with task count

        Example:
            message = resolver.get_task_count_message()
            # Returns: "You have 5 tasks"
        """
        task_count = self.get_task_count()

        if task_count == 0:
            return "You don't have any tasks yet"
        elif task_count == 1:
            return "You have 1 task"
        else:
            return f"You have {task_count} tasks"

    def clear_mapping(self) -> None:
        """
        Clear current display mapping.

        Call this when user logs out or session ends.
        """
        self.display_mapping = {}
        self.user_id = None


# Global resolver instance for convenience
_global_resolver = TaskResolver()


def get_resolver() -> TaskResolver:
    """
    Get global task resolver instance.

    Returns:
        Global TaskResolver instance

    Example:
        resolver = get_resolver()
        resolver.set_mapping(mapping, user_id)
    """
    return _global_resolver
