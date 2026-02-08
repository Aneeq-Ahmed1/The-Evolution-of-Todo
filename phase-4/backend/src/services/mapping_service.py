"""
Service for managing display index to task_id mappings for ordinal task references.
"""
from typing import Dict, List, Optional, Tuple
from sqlmodel import Session, select
from datetime import datetime
from ..models.task import Task
from ..schemas.task import TaskReadWithDisplayIndex


class DisplayMappingService:
    """
    Service class to handle display index to task_id mappings.
    This service manages the runtime mapping between display indices (1-based)
    and internal task IDs for ordinal reference functionality.
    """

    def __init__(self):
        self._mappings: Dict[str, Dict[int, str]] = {}  # user_id -> {display_index -> task_id}
        self._mapping_timestamps: Dict[str, datetime] = {}  # user_id -> last_updated

    def generate_display_mapping(self, tasks: List[Task], user_id: str) -> List[Dict[str, any]]:
        """
        Generate display index to task_id mapping for a user's tasks.

        Args:
            tasks: List of tasks for the user
            user_id: User identifier

        Returns:
            List of mapping dictionaries: [{"display_index": int, "task_id": str}, ...]
        """
        mapping = []
        for index, task in enumerate(tasks):
            display_index = index + 1  # 1-based indexing
            mapping_entry = {
                "display_index": display_index,
                "task_id": str(task.id)
            }
            mapping.append(mapping_entry)

        # Store the mapping for this user
        user_mapping = {}
        for item in mapping:
            user_mapping[item["display_index"]] = item["task_id"]

        self._mappings[user_id] = user_mapping
        self._mapping_timestamps[user_id] = datetime.now()

        return mapping

    def get_task_with_display_index(self, tasks: List[Task], user_id: str) -> List[TaskReadWithDisplayIndex]:
        """
        Add display indices to task objects for API responses.

        Args:
            tasks: List of tasks from database
            user_id: User identifier

        Returns:
            List of TaskReadWithDisplayIndex objects with display_index field
        """
        result = []
        for index, task in enumerate(tasks):
            try:
                # Convert task to dict using SQLModel's method
                task_dict = task.model_dump() if hasattr(task, 'model_dump') else task.dict()

                # Add display index to the dict
                task_dict["display_index"] = index + 1  # 1-based indexing

                # Convert dict back to TaskReadWithDisplayIndex Pydantic model
                task_with_display = TaskReadWithDisplayIndex(**task_dict)
                result.append(task_with_display)
            except Exception as e:
                print(f"❌ Error converting task {task.id} to TaskReadWithDisplayIndex: {e}")
                import traceback
                traceback.print_exc()
                raise

        return result

    def resolve_display_index(self, user_id: str, display_index: int) -> Optional[str]:
        """
        Resolve a display index to its corresponding task_id.

        Args:
            user_id: User identifier
            display_index: Display index (1-based)

        Returns:
            Task ID if found, None otherwise
        """
        user_mapping = self._mappings.get(user_id)
        if not user_mapping:
            return None

        return user_mapping.get(display_index)

    def is_mapping_valid(self, user_id: str, tasks: List[Task]) -> bool:
        """
        Check if the current mapping is still valid based on task list.

        Args:
            user_id: User identifier
            tasks: Current list of tasks for the user

        Returns:
            True if mapping is valid, False otherwise
        """
        user_mapping = self._mappings.get(user_id)
        if not user_mapping:
            return False

        # Check if the number of tasks matches the mapping size
        if len(tasks) != len(user_mapping):
            return False

        # Check if all task IDs in the mapping still exist
        current_task_ids = {str(task.id) for task in tasks}
        mapped_task_ids = set(user_mapping.values())

        return current_task_ids == mapped_task_ids

    def refresh_mapping(self, tasks: List[Task], user_id: str) -> Dict[str, any]:
        """
        Refresh the display index mapping for a user.

        Args:
            tasks: Current list of tasks for the user
            user_id: User identifier

        Returns:
            Dictionary with mapping update information
        """
        display_mapping = self.generate_display_mapping(tasks, user_id)

        return {
            "mapping_updated": True,
            "total_mappings": len(display_mapping),
            "display_mapping": display_mapping,
            "refreshed_at": datetime.now().isoformat()
        }

    def remove_mapping(self, user_id: str):
        """
        Remove the mapping for a user (e.g., when user logs out).

        Args:
            user_id: User identifier
        """
        if user_id in self._mappings:
            del self._mappings[user_id]
        if user_id in self._mapping_timestamps:
            del self._mapping_timestamps[user_id]

    def validate_display_index(self, user_id: str, display_index: int, tasks: List[Task]) -> Tuple[bool, Optional[str]]:
        """
        Validate if a display index is valid for the current task list.

        Args:
            user_id: User identifier
            display_index: Display index to validate
            tasks: Current list of tasks for the user

        Returns:
            Tuple of (is_valid, error_message)
        """
        if display_index < 1:
            return False, "Display index must be greater than 0"

        if display_index > len(tasks):
            return False, f"Display index {display_index} is out of range. Only {len(tasks)} tasks available."

        # Auto-heal: If mapping is invalid (e.g. server restart, new session), regenerate it
        if not self.is_mapping_valid(user_id, tasks):
            self.generate_display_mapping(tasks, user_id)

        return True, None

    def clear_user_mapping(self, user_id: str):
        """
        Clear the mapping for a specific user.

        Args:
            user_id: User identifier
        """
        if user_id in self._mappings:
            del self._mappings[user_id]
        if user_id in self._mapping_timestamps:
            del self._mapping_timestamps[user_id]

    def set_mapping(self, user_id: str, display_index: int, task_id: str):
        """
        Set a specific mapping for a user.

        Args:
            user_id: User identifier
            display_index: Display index
            task_id: Task identifier
        """
        if user_id not in self._mappings:
            self._mappings[user_id] = {}
        self._mappings[user_id][display_index] = task_id


# Global instance of the mapping service
mapping_service = DisplayMappingService()