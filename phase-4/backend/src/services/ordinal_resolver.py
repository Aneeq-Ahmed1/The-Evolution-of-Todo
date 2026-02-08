"""
Service for resolving ordinal references to task IDs.
Handles patterns like "task 1", "first task", "second task", etc.
"""
from typing import Optional, Dict, List
import re


class OrdinalResolver:
    """
    Service class to handle ordinal reference parsing and resolution.
    Converts ordinal expressions like "task 1", "first task", "second task" to display indices.
    """

    def __init__(self):
        # Define ordinal word to number mappings
        self.ordinal_words = {
            "first": 1, "second": 2, "third": 3, "fourth": 4, "fifth": 5,
            "sixth": 6, "seventh": 7, "eighth": 8, "ninth": 9, "tenth": 10,
            "eleventh": 11, "twelfth": 12, "thirteenth": 13, "fourteenth": 14, "fifteenth": 15,
            "sixteenth": 16, "seventeenth": 17, "eighteenth": 18, "nineteenth": 19, "twentieth": 20,
            "twenty-first": 21, "twenty-second": 22, "twenty-third": 23, "twenty-fourth": 24, "twenty-fifth": 25,
            "twenty-sixth": 26, "twenty-seventh": 27, "twenty-eighth": 28, "twenty-ninth": 29, "thirtieth": 30,
            # Cardinal numbers as words (for patterns like "number one task")
            "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
            "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
            "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15,
            "sixteen": 16, "seventeen": 17, "eighteen": 18, "nineteen": 19, "twenty": 20,
            "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60, "seventy": 70,
            "eighty": 80, "ninety": 90, "hundred": 100
        }

        # Define patterns for ordinal references
        self.patterns = [
            # "task {number}" - e.g., "task 1", "task 2"
            (r"task\s+(\d+)", 1),
            # "number {number} task" - e.g., "number 1 task", "number 2 task"
            (r"number\s+(\d+)\s+task", 1),
            # "{ordinal} task" - e.g., "first task", "second task", "third task"
            (r"(" + "|".join(self.ordinal_words.keys()) + r")\s+task", 1),
            # "task {ordinal}" - e.g., "task one", "task two", "task three"
            (r"task\s+(" + "|".join(self.ordinal_words.keys()) + r")", 1),
            # "{number}st/nd/rd/th task" - e.g., "1st task", "2nd task", "3rd task", "4th task"
            (r"(\d+)(?:st|nd|rd|th)\s+task", 1),
            # "task {number}st/nd/rd/th" - e.g., "task 1st", "task 2nd", "task 3rd"
            (r"task\s+(\d+)(?:st|nd|rd|th)", 1),
            # "{number} task" - e.g., "1 task", "2 task" (though this is less common)
            (r"(\d+)\s+task", 1),
            # "{number} is complete/done" - e.g., "1 is complete", "2 is done"
            (r"(\d+)\s+is\s+(complete|done|finished)", 1),
            # "the {number} task" - e.g., "the 1 task", "the 2 task"
            (r"the\s+(\d+)\s+task", 1),
            # "the {ordinal} task" - e.g., "the first task", "the second task"
            (r"the\s+(" + "|".join(self.ordinal_words.keys()) + r")\s+task", 1),
        ]

    def extract_ordinal_reference(self, message: str) -> Optional[int]:
        """
        Extract a display index from an ordinal reference in the message.

        Args:
            message: The user message to parse

        Returns:
            Display index if found, None otherwise
        """
        message_lower = message.lower().strip()

        for pattern, group_idx in self.patterns:
            match = re.search(pattern, message_lower)
            if match:
                ordinal_text = match.group(group_idx)

                # Convert to number
                try:
                    # If it's already a digit string, convert directly
                    display_index = int(ordinal_text)
                    return display_index
                except ValueError:
                    # If it's an ordinal word, look it up
                    if ordinal_text in self.ordinal_words:
                        display_index = self.ordinal_words[ordinal_text]
                        return display_index

        # If no pattern matched, return None
        return None

    def extract_task_action(self, message: str) -> Optional[str]:
        """
        Extract the intended action from the message.

        Args:
            message: The user message to parse

        Returns:
            Action type ('complete', 'edit', 'delete', 'uncomplete') or None
        """
        message_lower = message.lower().strip()

        # Define action patterns
        if any(word in message_lower for word in ["complete", "done", "finish", "finished"]):
            return "complete"
        elif any(word in message_lower for word in ["edit", "update", "change", "modify", "rename"]):
            return "edit"
        elif any(word in message_lower for word in ["delete", "remove", "cancel"]):
            return "delete"
        elif any(word in message_lower for word in ["uncomplete", "incomplete", "not done", "not finished"]):
            return "uncomplete"

        return None

    def parse_ordinal_command(self, message: str) -> Optional[Dict[str, any]]:
        """
        Parse an ordinal command and return the display index and action.

        Args:
            message: The user message to parse

        Returns:
            Dictionary with 'display_index' and 'action' if found, None otherwise
        """
        display_index = self.extract_ordinal_reference(message)
        if display_index is None:
            return None

        action = self.extract_task_action(message)

        return {
            "display_index": display_index,
            "action": action
        }


# Global instance of the ordinal resolver
ordinal_resolver = OrdinalResolver()