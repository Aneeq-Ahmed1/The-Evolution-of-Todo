"""
Intent Parser Service for AI Task Display Mapping

This service parses user commands to extract intent and ordinal task references.
It integrates with the ordinal resolver to support natural language task operations.
"""
import re
from typing import Optional, Dict, Any, Tuple
from enum import Enum
from .ordinal_resolver import normalize_ordinal_to_number, validate_ordinal_format


class TaskIntent(Enum):
    """Enumeration of supported task intents"""
    LIST_TASKS = "list_tasks"
    CREATE_TASK = "create_task"
    COMPLETE_TASK = "complete_task"
    UNCOMPLETE_TASK = "uncomplete_task"
    EDIT_TASK = "edit_task"
    DELETE_TASK = "delete_task"
    GET_TASK = "get_task"
    UNKNOWN = "unknown"


class IntentParser:
    """
    Parser for extracting user intent and task references from natural language.

    Supports commands like:
    - "task 1 is complete" -> COMPLETE_TASK, display_index=1
    - "edit task 2" -> EDIT_TASK, display_index=2
    - "delete the first task" -> DELETE_TASK, display_index=1
    - "show me task three" -> GET_TASK, display_index=3
    """

    # Intent patterns (order matters - more specific first)
    INTENT_PATTERNS = {
        TaskIntent.COMPLETE_TASK: [
            r'\b(complete|finish|done|finished|completed)\b.*\btask\b',
            r'\btask\b.*\b(complete|finish|done|finished|completed|is complete|is done|is finished)\b',
            r'\bmark\b.*\b(complete|done|finished)\b',
        ],
        TaskIntent.UNCOMPLETE_TASK: [
            r'\b(uncomplete|incomplete|undo|unfinish|unmark)\b.*\btask\b',
            r'\btask\b.*\b(uncomplete|incomplete|not complete|not done)\b',
            r'\bmark\b.*\b(incomplete|not complete|undone)\b',
        ],
        TaskIntent.EDIT_TASK: [
            r'\b(edit|update|change|modify|rename)\b.*\btask\b',
            r'\btask\b.*\b(edit|update|change|modify|rename)\b',
        ],
        TaskIntent.DELETE_TASK: [
            r'\b(delete|remove|cancel|discard)\b.*\btask\b',
            r'\btask\b.*\b(delete|remove|cancel|discard)\b',
        ],
        TaskIntent.GET_TASK: [
            r'\b(show|display|get|view|see)\b.*\btask\b',
            r'\btask\b.*\binfo\b',
            r'\bwhat\s+is\b.*\btask\b',
        ],
        TaskIntent.LIST_TASKS: [
            r'\b(list|show|display)\b.*\b(tasks|todos|all tasks)\b',
            r'\bwhat\s+(tasks|todos)\b',
            r'\bshow\s+me\b.*\b(tasks|todos)\b',
        ],
        TaskIntent.CREATE_TASK: [
            r'\b(create|add|new|make)\b.*\btask\b',
            r'\btask\b.*\b(create|add|new)\b',
        ],
    }

    def parse(self, user_input: str) -> Dict[str, Any]:
        """
        Parse user input to extract intent and parameters.

        Args:
            user_input: Natural language command from user

        Returns:
            Dictionary with:
                - intent: TaskIntent enum value
                - display_index: int or None
                - confidence: float (0.0 to 1.0)
                - original_text: str

        Examples:
            >>> parser = IntentParser()
            >>> result = parser.parse("task 1 is complete")
            >>> result['intent'] == TaskIntent.COMPLETE_TASK
            True
            >>> result['display_index']
            1
        """
        user_input_lower = user_input.lower().strip()

        # Extract display index first
        display_index = normalize_ordinal_to_number(user_input_lower)

        # Determine intent
        intent = self._determine_intent(user_input_lower)

        # Calculate confidence based on pattern match and display index presence
        confidence = self._calculate_confidence(intent, display_index, user_input_lower)

        return {
            'intent': intent,
            'display_index': display_index,
            'confidence': confidence,
            'original_text': user_input,
            'has_ordinal_reference': display_index is not None
        }

    def _determine_intent(self, text: str) -> TaskIntent:
        """
        Determine the intent from user input text.

        Args:
            text: Lowercased user input

        Returns:
            TaskIntent enum value
        """
        for intent, patterns in self.INTENT_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, text):
                    return intent

        return TaskIntent.UNKNOWN

    def _calculate_confidence(self, intent: TaskIntent, display_index: Optional[int], text: str) -> float:
        """
        Calculate confidence score for the parsed intent.

        Args:
            intent: Detected intent
            display_index: Extracted display index (or None)
            text: Original text

        Returns:
            Confidence score between 0.0 and 1.0
        """
        if intent == TaskIntent.UNKNOWN:
            return 0.0

        confidence = 0.7  # Base confidence for pattern match

        # Boost confidence if ordinal reference is present for task-specific intents
        task_specific_intents = {
            TaskIntent.COMPLETE_TASK,
            TaskIntent.UNCOMPLETE_TASK,
            TaskIntent.EDIT_TASK,
            TaskIntent.DELETE_TASK,
            TaskIntent.GET_TASK
        }

        if intent in task_specific_intents and display_index is not None:
            confidence = 0.95  # High confidence for specific task reference

        # Reduce confidence if ordinal reference is missing for task-specific intents
        if intent in task_specific_intents and display_index is None:
            confidence = 0.5  # Lower confidence without specific task reference

        return confidence

    def parse_with_intent(self, user_input: str) -> Tuple[TaskIntent, Optional[int], float]:
        """
        Convenience method to parse and return intent, display_index, and confidence.

        Args:
            user_input: Natural language command from user

        Returns:
            Tuple of (intent, display_index, confidence)

        Example:
            >>> parser = IntentParser()
            >>> intent, index, conf = parser.parse_with_intent("edit task 2")
            >>> intent == TaskIntent.EDIT_TASK
            True
            >>> index
            2
        """
        result = self.parse(user_input)
        return result['intent'], result['display_index'], result['confidence']

    def supports_ordinal_references(self, intent: TaskIntent) -> bool:
        """
        Check if an intent supports ordinal task references.

        Args:
            intent: TaskIntent to check

        Returns:
            True if intent supports ordinal references, False otherwise
        """
        return intent in {
            TaskIntent.COMPLETE_TASK,
            TaskIntent.UNCOMPLETE_TASK,
            TaskIntent.EDIT_TASK,
            TaskIntent.DELETE_TASK,
            TaskIntent.GET_TASK
        }


# Global intent parser instance
_global_parser = IntentParser()


def get_intent_parser() -> IntentParser:
    """
    Get global intent parser instance.

    Returns:
        Global IntentParser instance
    """
    return _global_parser


def parse_user_command(user_input: str) -> Dict[str, Any]:
    """
    Convenience function to parse user command using global parser.

    Args:
        user_input: Natural language command from user

    Returns:
        Parsed result dictionary

    Example:
        >>> result = parse_user_command("task 1 is complete")
        >>> result['intent']
        <TaskIntent.COMPLETE_TASK: 'complete_task'>
        >>> result['display_index']
        1
    """
    return _global_parser.parse(user_input)
