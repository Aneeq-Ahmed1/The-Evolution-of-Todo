"""
Ordinal Resolver Service for AI Task Display Mapping

This module provides utilities to parse and normalize ordinal references
from natural language commands to integer display indices.

Supports formats like:
- "task 1", "task 2" (numeric)
- "first task", "second task", "third task" (ordinal words)
- "task one", "task two" (number words)
- "1st task", "2nd task", "3rd task" (ordinal suffixes)
"""
import re
from typing import Optional, Union


# Mapping of ordinal words to integers
ORDINAL_WORDS = {
    'first': 1, 'second': 2, 'third': 3, 'fourth': 4, 'fifth': 5,
    'sixth': 6, 'seventh': 7, 'eighth': 8, 'ninth': 9, 'tenth': 10,
    'eleventh': 11, 'twelfth': 12, 'thirteenth': 13, 'fourteenth': 14,
    'fifteenth': 15, 'sixteenth': 16, 'seventeenth': 17, 'eighteenth': 18,
    'nineteenth': 19, 'twentieth': 20
}

# Mapping of number words to integers
NUMBER_WORDS = {
    'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
    'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10,
    'eleven': 11, 'twelve': 12, 'thirteen': 13, 'fourteen': 14,
    'fifteen': 15, 'sixteen': 16, 'seventeen': 17, 'eighteen': 18,
    'nineteen': 19, 'twenty': 20
}


def parse_numeric_task_reference(text: str) -> Optional[int]:
    """
    Parse numeric task references like "task 1", "task 2", "number 3".

    Args:
        text: User input text containing task reference

    Returns:
        Integer display index (1-based) or None if no valid reference found

    Examples:
        >>> parse_numeric_task_reference("task 1 is complete")
        1
        >>> parse_numeric_task_reference("complete task 5")
        5
        >>> parse_numeric_task_reference("task number 3")
        3
    """
    # Pattern: "task <number>" or "number <number>" or "#<number>"
    patterns = [
        r'\btask\s+(\d+)\b',
        r'\bnumber\s+(\d+)\b',
        r'#(\d+)\b',
        r'\b(\d+)(?:st|nd|rd|th)\s+task\b'
    ]

    text_lower = text.lower()
    for pattern in patterns:
        match = re.search(pattern, text_lower)
        if match:
            number = int(match.group(1))
            return number if number > 0 else None

    return None


def parse_ordinal_word_reference(text: str) -> Optional[int]:
    """
    Parse ordinal word references like "first task", "second task", "third task".

    Args:
        text: User input text containing ordinal word reference

    Returns:
        Integer display index (1-based) or None if no valid reference found

    Examples:
        >>> parse_ordinal_word_reference("first task is complete")
        1
        >>> parse_ordinal_word_reference("complete the second task")
        2
        >>> parse_ordinal_word_reference("third task needs attention")
        3
    """
    text_lower = text.lower()

    # Pattern: "<ordinal word> task"
    pattern = r'\b(' + '|'.join(ORDINAL_WORDS.keys()) + r')\s+task\b'
    match = re.search(pattern, text_lower)

    if match:
        ordinal_word = match.group(1)
        return ORDINAL_WORDS[ordinal_word]

    return None


def parse_number_word_reference(text: str) -> Optional[int]:
    """
    Parse number word references like "task one", "task two", "task three".

    Args:
        text: User input text containing number word reference

    Returns:
        Integer display index (1-based) or None if no valid reference found

    Examples:
        >>> parse_number_word_reference("task one is complete")
        1
        >>> parse_number_word_reference("complete task two")
        2
        >>> parse_number_word_reference("task three needs review")
        3
    """
    text_lower = text.lower()

    # Pattern: "task <number word>"
    pattern = r'\btask\s+(' + '|'.join(NUMBER_WORDS.keys()) + r')\b'
    match = re.search(pattern, text_lower)

    if match:
        number_word = match.group(1)
        return NUMBER_WORDS[number_word]

    return None


def normalize_ordinal_to_number(text: str) -> Optional[int]:
    """
    Convert any ordinal format to integer display index.

    Tries all supported formats in order:
    1. Numeric references ("task 1", "task 2")
    2. Ordinal word references ("first task", "second task")
    3. Number word references ("task one", "task two")

    Args:
        text: User input text containing task reference

    Returns:
        Integer display index (1-based) or None if no valid reference found

    Examples:
        >>> normalize_ordinal_to_number("task 1 is complete")
        1
        >>> normalize_ordinal_to_number("first task is complete")
        1
        >>> normalize_ordinal_to_number("task one is complete")
        1
        >>> normalize_ordinal_to_number("complete the 2nd task")
        2
    """
    # Try numeric first (most common)
    result = parse_numeric_task_reference(text)
    if result is not None:
        return result

    # Try ordinal words
    result = parse_ordinal_word_reference(text)
    if result is not None:
        return result

    # Try number words
    result = parse_number_word_reference(text)
    if result is not None:
        return result

    return None


def validate_ordinal_format(text: str) -> bool:
    """
    Check if text contains any recognizable ordinal reference format.

    Args:
        text: User input text

    Returns:
        True if text contains a valid ordinal reference, False otherwise

    Examples:
        >>> validate_ordinal_format("task 1 is complete")
        True
        >>> validate_ordinal_format("first task needs review")
        True
        >>> validate_ordinal_format("just some random text")
        False
    """
    return normalize_ordinal_to_number(text) is not None


def extract_all_ordinal_references(text: str) -> list[int]:
    """
    Extract all ordinal references from text.

    Args:
        text: User input text

    Returns:
        List of integer display indices (1-based) found in text

    Examples:
        >>> extract_all_ordinal_references("task 1 and task 2 are complete")
        [1, 2]
        >>> extract_all_ordinal_references("first task is done, working on second task")
        [1, 2]
    """
    references = []

    # Extract numeric references
    for match in re.finditer(r'\btask\s+(\d+)\b', text.lower()):
        num = int(match.group(1))
        if num > 0:
            references.append(num)

    # Extract ordinal word references
    for ordinal_word, number in ORDINAL_WORDS.items():
        if re.search(rf'\b{ordinal_word}\s+task\b', text.lower()):
            references.append(number)

    # Extract number word references
    for number_word, number in NUMBER_WORDS.items():
        if re.search(rf'\btask\s+{number_word}\b', text.lower()):
            references.append(number)

    # Remove duplicates and sort
    return sorted(list(set(references)))
